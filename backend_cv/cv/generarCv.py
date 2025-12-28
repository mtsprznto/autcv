

from dotenv import load_dotenv
import os
from cv.pdf import PDF
from utils.utils import extraer_lenguajes_unicos, agrupar_lenguajes_por_categoria
from io import BytesIO


import httpx

load_dotenv()



async def subir_cv_a_frontend(buffer: BytesIO, nombre_archivo: str) -> str:
    url_frontend_api = f"{os.getenv('URL_FRONTEND')}/api/upload/blob"  # Usa dominio final, no localhost
    async with httpx.AsyncClient() as client:
        files = {"file": (nombre_archivo, buffer, "application/pdf")}
        response = await client.post(url_frontend_api, files=files)
        if response.status_code == 200:
            print("✅ PDF subido al blob:", response.json()["url"])
            return response.json()["url"]
        else:
            print("❌ Error al subir PDF:", response.text)
            return None



async def generar_cv(proyectos_destacados: list,experiencias_cv:list , nombre_archivo: str):
    """Genera un CV en PDF con la información de contacto, educación, proyectos y tecnologías."""
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=30)
    pdf.tecnologias_experiencia = {
        "Python": 2,
        "JavaScript": 1,
        "FastAPI": 2,
        "Docker": 2,
        "Kubernetes": 1,
        "Terraform": 1,
        "React": 2,
        "MySQL": 2,
        "PostgreSQL": 2,
        "Cloudflare": 2,
    }
    pdf.contacto = {
        "profesion": "Ingeniería en Ejecución en Informática",
        "email": "contacto@mtsprz.org",
        "telefono": "+56 975475781"
    }
    pdf.add_page()

    # -------------------------
    # Datos Personales
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Personal Data", ln=True)
    pdf.set_font("Helvetica", size=10)
    pdf.multi_cell(0, 6,
        f"Name: Matias Pérez Nauto\n"
        f"Phone: +56 975475781\n"
        f"Email: contacto@mtsprz.org\n"
        f"Profession: Ingenieria en Ejecución en Informática\n"
    )
    pdf.ln(5)

    # -------------------------
    # Summary
    resumen = (
    "Desarrollador de software con experiencia en Python, JavaScript, Next.js, PHP, SQL. "
    "Apasionado por crear soluciones eficientes, seguras y optimizadas, con enfoque en interfaces "
    "y mejores prácticas. Busco aportar en entornos dinámicos e innovadores."
    )

    pdf.section_title("Summary")

    pdf.set_font("Helvetica", size=5)           
    pdf.set_text_color(100, 100, 100)           
    pdf.multi_cell(0, 8, resumen, align="L")    
    pdf.set_text_color(0, 0, 0)                 
    pdf.ln(5)

    # -------------------------
    # Consultancy (Experiencias)
    pdf.section_title("Consultancy")
    print(f"Experiencia CV: {experiencias_cv}")
    for exp in experiencias_cv:
        # Encabezado principal
        empresa = exp.get("empresa", "")
        fecha = exp.get("fecha", "")
        stack = ", ".join(exp.get("stack", []))
        pdf.texto_doble_alineado(
            izquierda=f"{empresa} ({fecha})",
            derecha=f"Stack: {stack}"
        )

        # Campos principales
        pdf.paragraph(f"Position: {exp.get('titulo', exp.get('posicion', '')).strip()}")
        pdf.paragraph(f"Business: {exp.get('business', '')}")
        pdf.paragraph(f"Scope: {exp.get('scope', exp.get('experiencia_cv', '')).strip()}")

        # Subsecciones limpias
        if exp.get("cicd"):
            cicd = ", ".join(exp["cicd"]) if isinstance(exp["cicd"], list) else exp["cicd"]
            pdf.sub_paragraph(f"CI/CD: {cicd}")
        if exp.get("observabilidad"):
            obs = ", ".join(exp["observabilidad"]) if isinstance(exp["observabilidad"], list) else exp["observabilidad"]
            pdf.sub_paragraph(f"Observability: {obs}")
        if exp.get("vcs"):
            vcs = ", ".join(exp["vcs"]) if isinstance(exp["vcs"], list) else exp["vcs"]
            pdf.sub_paragraph(f"VCS: {vcs}")
        if exp.get("datasources"):
            ds = ", ".join(exp["datasources"]) if isinstance(exp["datasources"], list) else exp["datasources"]
            pdf.sub_paragraph(f"Data Sources: {ds}")

        pdf.ln(3)


    # -------------------------
    # Proyectos
    # pdf.section_title("Proyectos")
    # for proyecto in proyectos_destacados:
    #     pdf.render_proyecto(proyecto)

    # -------------------------
    # Educación
    pdf.section_title("Background / Education")
    pdf.texto_doble_alineado(
        izquierda="AIEP, 2024 - 2026",
        derecha="Puerto Varas, Chile"
    )
    pdf.paragraph("Programación y Análisis de Sistemas")
    pdf.ln(1)
    pdf.texto_doble_alineado(
        izquierda="AIEP, 2026 - 2027",
        derecha="Puerto Varas, Chile"
    )
    pdf.paragraph("Ingeniería de Ejecución en Informática, mención Desarrollo de Sistemas")
    pdf.ln(3)

    # -------------------------

    # PDF en memoria con BytesIO
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    buffer = BytesIO(pdf_bytes)
    buffer.seek(0)      # Posicionamos al inicio para lectura

    # Enviamos a frontend (Next.js)
    url_frontend_api = f"{os.getenv('URL_FRONTEND')}/api/upload/blob"  # Usa dominio final, no localhost
    async with httpx.AsyncClient() as client:
        files = {"file": (nombre_archivo, buffer, "application/pdf")}
        response = await client.post(url_frontend_api, files=files)
        if response.status_code == 200:
            print("✅ PDF subido al blob:", response.json()["url"])
            return response.json()["url"]
        else:
            print("❌ Error al subir PDF:", response.text)
            return None
