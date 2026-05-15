

from datetime import datetime
from dotenv import load_dotenv
from cv.pdf import PDF
from cv.static_exp import experiencias_manuales
from utils.utils import limpiar_texto_u
from utils.upload import subir_cv



load_dotenv()



async def generar_cv(proyectos_destacados: list,experiencias_cv:list , nombre_archivo: str):
    """Genera un CV en PDF con la información de contacto, educación, proyectos y tecnologías."""
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=28)

    anio_actual = datetime.now().year
    # 2. Diccionario con el AÑO DE INICIO de cada tecnología
    anios_inicio = {
        "Python": 2024,      # Empezaste en 2022
        "JavaScript": 2024,  # Empezaste en 2023
        "FastAPI": 2024,
        "Docker": 2025,
        "Kubernetes": 2025,
        "Terraform": 2025,
        "React": 2025,
        "MySQL": 2024,
        "PostgreSQL": 2024,
        "Cloudflare": 2025,
    }
    pdf.tecnologias_experiencia = {
        tecnologia: anio_actual - anio_inicio 
        for tecnologia, anio_inicio in anios_inicio.items()
    }
    for tec, exp in pdf.tecnologias_experiencia.items():
        if exp == 0:
            pdf.tecnologias_experiencia[tec] = "Reciente" # o < 1

    pdf.contacto = {
        "profesion": "Ingeniería en Ejecución en Informática",
        "email": "contacto@mtsprz.org",
        "telefono": "+56 975475781"
    }
    pdf.add_page()

    # -------------------------
    # Summary
    resumen = (
    "Desarrollador de software con experiencia en Python, JavaScript, Next.js, Vue.js, SQL. "
    "Apasionado por crear soluciones eficientes, seguras y optimizadas, con enfoque en interfaces "
    "y mejores prácticas. Busco aportar en entornos dinámicos e innovadores."
    )
    pdf.section_title("Resumen")
    # Barra de acento izquierda
    pdf.set_fill_color(43, 108, 176)
    pdf.rect(pdf.l_margin, pdf.get_y(), 2, 12, style="F")
    pdf.set_x(pdf.l_margin + 4)
    pdf.set_font("Roboto", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 5, resumen, align="L")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # -------------------------
    pdf.section_title("Experiencia")
    # -------------------------
    # Consultancy "real"
    
    for exp in experiencias_manuales:
        generar_consultancy_real(pdf, exp)
        pdf.ln(1)
    
    # -------------------------
    # Generado IA
    # Consultancy (Experiencias) con fpdf2 Tables
    
    for exp in experiencias_cv:
        def _join(val):
            if isinstance(val, list):
                return ", ".join([limpiar_texto_u(str(v)) for v in val])
            return limpiar_texto_u(str(val)) if val else ""

        pdf.render_experience(
            empresa=limpiar_texto_u(exp.get("empresa", "")),
            fecha=limpiar_texto_u(exp.get("fecha", "")),
            titulo=limpiar_texto_u(exp.get("titulo", "").strip()),
            business=limpiar_texto_u(exp.get("business", "")),
            scope=limpiar_texto_u(exp.get("experiencia_cv", "").strip()),
            stack=_join(exp.get("stack", [])),
            cicd=_join(exp.get("cicd", [])),
            datasources=_join(exp.get("datasources", [])),
        )


    # -------------------------
    # Proyectos
    # pdf.section_title("Proyectos")
    # for proyecto in proyectos_destacados:
    #     pdf.render_proyecto(proyecto)

    # -------------------------
    # Educación
    pdf.section_title("Antecedentes / Educación")
    pdf.render_education_entry("AIEP", "2026 - 2028", "Ingeniería de Ejecución en Informática, mención Desarrollo de Sistemas")
    pdf.render_education_entry("AIEP", "2024 - 2026", "Programación y Análisis de Sistemas")

    # -------------------------
    # Certificaciones
    pdf.section_title("Certificaciones")
    pdf.render_education_entry("CISCO", "2025", "Introduction to Cybersecurity")
    pdf.render_education_entry("Cognitive Class", "2024", "Data Analysis with Python")
    pdf.render_education_entry("Cognitive Class", "2024", "SQL and Relational Databases 101")
    pdf.render_education_entry("Anthropic", "2025", "Claude Code in Action")
    pdf.render_education_entry("Platzi", "2024", "Base de Datos con SQL")
    pdf.render_education_entry("Platzi", "2024", "Python")

    pdf.ln(3)
    # -------------------------
    resp = await subir_cv(pdf, nombre_archivo)
    return resp


def generar_consultancy_real(pdf: PDF, datos: dict) -> bool:
    pdf.render_experience(
        empresa=datos.get("empresa", ""),
        fecha=datos.get("fecha", ""),
        titulo=datos.get("posicion", ""),
        business=datos.get("negocio", ""),
        scope=datos.get("alcance", ""),
        stack=datos.get("stack", ""),
        cicd=datos.get("cicd", ""),
        datasources=datos.get("datasources", ""),
    )
    return True


