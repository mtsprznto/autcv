

from dotenv import load_dotenv
import os
from cv.pdf import PDF
from utils.utils import clean_text, limpiar_texto_u
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
    pdf.set_font("Roboto", "B", 12)
    pdf.cell(0, 10, "Personal Data", ln=True)
    pdf.set_font("Roboto","", size=10)
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
    pdf.set_font("Roboto", "B", 12)
    pdf.section_title("Summary")
    pdf.set_font("Roboto","", size=10)        
    pdf.set_text_color(100, 100, 100)           
    pdf.multi_cell(0, 6, resumen, align="L")    
    pdf.set_text_color(0, 0, 0)                 
    pdf.ln(5)

    # -------------------------
    # -------------------------
    # Consultancy (Experiencias) con fpdf2 Tables
    pdf.set_font("Roboto", "B", 12)
    pdf.section_title("Consultancy")
    pdf.set_font("Roboto","", size=10)
    for exp in experiencias_cv:
        empresa = limpiar_texto_u(exp.get("empresa", ""))
        fecha = limpiar_texto_u(exp.get("fecha", ""))
        titulo = limpiar_texto_u(exp.get("titulo", "").strip())
        business = limpiar_texto_u(exp.get("business", ""))
        scope = limpiar_texto_u(exp.get("experiencia_cv", "").strip())


        # Calculamos el ancho útil de la página
        # Creamos una tabla sin bordes para el layout de 2 columnas
        # col_widths es el porcentaje de ancho (50% y 50%)
        with pdf.table(
            col_widths=(50, 50),
            borders_layout="NONE", 
            line_height=5,
        ) as table:
            row = table.row()
            # Celda Izquierda
            left_content = (
                f"{empresa} ({fecha})\n"
                f"Position: {titulo}\n"
                f"Business: {business}\n"
                f"Scope: {scope}"
            )

            row.cell(left_content, v_align="T")

            # Celda Derecha
            stack = ", ".join([limpiar_texto_u(s) for s in exp.get("stack", [])])
            right_content = f"Stack: {stack}\n"

            if exp.get("cicd"):
                val = exp["cicd"]
                right_content += f"CI/CD: {', '.join(val) if isinstance(val, list) else limpiar_texto_u(val)}\n"
            if exp.get("datasources"):
                val = exp["datasources"]
                right_content += f"Data Sources: {', '.join(val) if isinstance(val, list) else limpiar_texto_u(val)}"


            row.cell(right_content, v_align="T")

        pdf.ln(5) # Espacio entre experiencias


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
        derecha=""
    )
    pdf.paragraph("Programación y Análisis de Sistemas")
    pdf.ln(1)
    pdf.texto_doble_alineado(
        izquierda="AIEP, 2026 - 2027",
        derecha=""
    )
    pdf.paragraph("Ingeniería de Ejecución en Informática, mención Desarrollo de Sistemas")
    pdf.ln(3)

    # -------------------------

    # PDF en memoria con BytesIO
    pdf_bytes = pdf.output()
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
