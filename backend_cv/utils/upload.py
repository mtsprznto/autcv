

# -------------------------
# UPLOADS
from io import BytesIO
import os
from cv.pdf import PDF


def _load_env():
    """Carga las variables de entorno desde .env"""
    from dotenv import load_dotenv
    load_dotenv(override=True)


def _should_use_supabase() -> bool:
    """Determina si se debe usar Supabase Storage.
    - FORCE_SUPABASE=true → siempre Supabase (para pruebas en local)
    - Si no, detecta por URL_FRONTEND (localhost = modo disco)"""
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


def _get_supabase_client():
    """Crea un cliente de Supabase con la service_role key."""
    from supabase import create_client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    print(f"🔍 [DEBUG] SUPABASE_URL='{url}'")
    print(f"🔍 [DEBUG] SUPABASE_SERVICE_KEY={'✅ presente' if key else '❌ faltante'}")
    if not url or not key:
        raise ValueError("Faltan SUPABASE_URL o SUPABASE_SERVICE_KEY en .env")
    return create_client(url, key)


async def subir_cv(pdf: PDF, nombre_archivo: str) -> str:
    pdf_bytes = bytes(pdf.output())  # bytearray → bytes para Supabase

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

    # --- MODO SUPABASE: subir a Storage ---
    try:
        supabase = _get_supabase_client()
        bucket = os.getenv("SUPABASE_BUCKET", "cv-pdfs")
        print(f"📤 [UPLOAD] Subiendo a Supabase bucket='{bucket}' archivo='{nombre_archivo}'...")

        res = supabase.storage.from_(bucket).upload(
            path=nombre_archivo,
            file=pdf_bytes,
            file_options={"content-type": "application/pdf", "upsert": "true"}
        )

        # Generar URL firmada válida por 365 días (bucket privado)
        signed_res = supabase.storage.from_(bucket).create_signed_url(
            path=nombre_archivo,
            expires_in=365 * 24 * 60 * 60  # 365 días en segundos
        )
        signed_path = signed_res["signedURL"]
        supabase_url = os.getenv("SUPABASE_URL")
        public_url = f"{supabase_url}{signed_path}" if signed_path.startswith("/") else signed_path
        print(f"✅ PDF subido a Supabase: {public_url}")
        return public_url

    except Exception as e:
        print(f"❌ Error al subir a Supabase: {type(e).__name__}: {e}")
        # Fallback: guardar en disco si falla Supabase
        local_dir = os.path.join(os.path.dirname(__file__), "..", "output")
        os.makedirs(local_dir, exist_ok=True)
        local_path = os.path.join(local_dir, nombre_archivo)
        with open(local_path, "wb") as f:
            f.write(pdf_bytes)
        print(f"⚠️ Fallback: PDF guardado en disco: {local_path}")
        return f"http://127.0.0.1:8000/output/{nombre_archivo}"

# -------------------------
