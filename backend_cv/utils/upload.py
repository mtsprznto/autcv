
# -------------------------
# UPLOADS
from io import BytesIO
import os
import httpx
from cv.pdf import PDF


def _load_env():
    """Carga las variables de entorno desde .env"""
    from dotenv import load_dotenv
    load_dotenv(override=True)


def _should_use_supabase() -> bool:
    """Determina si se debe usar Supabase Storage."""
    _load_env()
    force = os.getenv("FORCE_SUPABASE", "").strip().lower()
    print(f"🔍 [DEBUG] FORCE_SUPABASE='{force}'")
    
    if force == "true":
        print("🔄 [MODO] Forzado a Supabase (FORCE_SUPABASE=true)")
        return True
    
    url = os.getenv("URL_FRONTEND", "")
    is_local = "localhost" in url or "127.0.0.1" in url or url == ""
    print(f"🔍 [DEBUG] URL_FRONTEND='{url}' → is_local={is_local}")
    return not is_local


async def _supabase_upload(bucket: str, filename: str, pdf_bytes: bytes, api_key: str, supabase_url: str) -> str:
    """Sube archivo a Supabase Storage vía REST API y retorna URL firmada."""
    upload_url = f"{supabase_url}/storage/v1/object/{bucket}/{filename}"
    
    async with httpx.AsyncClient() as client:
        # 1. Subir archivo (upsert)
        resp = await client.post(
            upload_url,
            content=pdf_bytes,
            headers={
                "apikey": api_key,
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/pdf",
                "x-upsert": "true",
            },
            timeout=30,
        )
        if resp.status_code not in (200, 201):
            raise Exception(f"Upload failed ({resp.status_code}): {resp.text}")

        # 2. Generar URL firmada (365 días)
        sign_url = f"{supabase_url}/storage/v1/object/sign/{bucket}/{filename}"
        resp_sign = await client.post(
            sign_url,
            json={"expiresIn": 365 * 24 * 60 * 60},  # 365 días
            headers={
                "apikey": api_key,
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=10,
        )
        if resp_sign.status_code != 200:
            raise Exception(f"Sign failed ({resp_sign.status_code}): {resp_sign.text}")

        signed_path = resp_sign.json().get("signedURL", "")
        full_url = f"{supabase_url}{signed_path}" if signed_path.startswith("/") else signed_path
        return full_url


async def subir_cv(pdf: PDF, nombre_archivo: str) -> str:
    pdf_bytes = bytes(pdf.output())

    # --- MODO LOCAL: guardar en disco ---
    if not _should_use_supabase():
        local_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, nombre_archivo)
        with open(local_path, "wb") as f:
            f.write(pdf_bytes)
        local_url = f"http://127.0.0.1:8000/output/{nombre_archivo}"
        print(f"✅ PDF guardado en disco: {local_path}")
        print(f"🔗 URL local: {local_url}")
        return local_url

    # --- MODO SUPABASE: subir vía REST API ---
    supabase_url = os.getenv("SUPABASE_URL")
    api_key = os.getenv("SUPABASE_SERVICE_KEY")
    bucket = os.getenv("SUPABASE_BUCKET", "cv-pdfs")

    # Validar que las env vars existan
    if not supabase_url or not api_key:
        print(f"❌ Faltan SUPABASE_URL o SUPABASE_SERVICE_KEY en Vercel")
        print(f"   SUPABASE_URL={'✅' if supabase_url else '❌'}")
        print(f"   SUPABASE_SERVICE_KEY={'✅' if api_key else '❌'}")
        return None

    try:
        print(f"📤 [UPLOAD] Subiendo a Supabase bucket='{bucket}' archivo='{nombre_archivo}'...")
        public_url = await _supabase_upload(bucket, nombre_archivo, pdf_bytes, api_key, supabase_url)
        print(f"✅ PDF subido a Supabase: {public_url}")
        return public_url

    except Exception as e:
        print(f"❌ Error al subir a Supabase: {type(e).__name__}: {e}")
        return None

# -------------------------
