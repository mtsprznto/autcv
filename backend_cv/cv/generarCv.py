

from datetime import datetime
from dotenv import load_dotenv
from cv.pdf import PDF
from utils.utils import limpiar_texto_u
from utils.upload import subir_cv



load_dotenv()



async def generar_cv(
    proyectos_github: list, 
    experiencias_manuales: list, 
    proyectos_destacados: list,
    nombre_archivo: str
):
    """
    Genera un CV optimizado para ATS (Applicant Tracking Systems).
    
    Estructura:
    1. Resumen profesional (con keywords de la propuesta)
    2. Experiencia Profesional (SOLO experiencias manuales verificadas)
    3. Proyectos Destacados (portafolio técnico de GitHub)
    4. Educación
    5. Certificaciones
    """
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=28)

    anio_actual = datetime.now().year
    # Diccionario con el AÑO DE INICIO de cada tecnología
    anios_inicio = {
        "Python": 2024,
        "JavaScript": 2024,
        "FastAPI": 2024,
        "Docker": 2025,
        "Kubernetes": 2025,
        "Terraform": 2025,
        "React": 2025,
        "MySQL": 2024,
        "PostgreSQL": 2024,
        "Cloudflare": 2025,
        "TypeScript": 2024,
        "Node.js": 2024,
        "Next.js": 2025,
        "AWS": 2025,
        "Redis": 2025,
        "MongoDB": 2024,
    }
    pdf.tecnologias_experiencia = {
        tecnologia: anio_actual - anio_inicio 
        for tecnologia, anio_inicio in anios_inicio.items()
    }
    for tec, exp in pdf.tecnologias_experiencia.items():
        if exp == 0:
            pdf.tecnologias_experiencia[tec] = "Reciente"

    pdf.contacto = {
        "profesion": "Ingeniería en Ejecución en Informática",
        "email": "contacto@mtsprz.org",
        "telefono": "+56 975475781"
    }
    pdf.add_page()

    # -------------------------
    # RESUMEN PROFESIONAL (ATS-optimized)
    # -------------------------
    resumen = (
        "Desarrollador de software Fullstack con experiencia comprobada en Python, FastAPI, "
        "JavaScript/TypeScript, React, Next.js y bases de datos SQL/NoSQL. "
        "Especializado en arquitecturas API RESTful, microservicios, contenerización con Docker "
        "e infraestructura cloud (AWS). Experiencia en proyectos de automatización, procesamiento "
        "de datos, integración de sistemas y desarrollo de plataformas SaaS. "
        "Enfocado en código limpio, testing automatizado y prácticas DevOps."
    )
    pdf.section_title("Resumen")
    pdf.set_fill_color(43, 108, 176)
    pdf.rect(pdf.l_margin, pdf.get_y(), 2, 12, style="F")
    pdf.set_x(pdf.l_margin + 4)
    pdf.set_font("Roboto", "", 9)
    pdf.set_text_color(60, 60, 60)
    pdf.multi_cell(0, 5, resumen, align="L")
    pdf.set_text_color(0, 0, 0)
    pdf.ln(5)

    # -------------------------
    # EXPERIENCIA PROFESIONAL (Solo experiencias manuales verificadas)
    # -------------------------
    pdf.section_title("Experiencia Profesional")
    
    for exp in experiencias_manuales:
        _render_experiencia_manual(pdf, exp)
        pdf.ln(1)
    
    # -------------------------
    # PROYECTOS DESTACADOS (Portafolio técnico - NO experiencias laborales)
    # -------------------------
    if proyectos_destacados:
        pdf.section_title("Proyectos Destacados")
        pdf.set_font("Roboto", "", 8)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 4, "Proyectos personales y contribuciones técnicas relevantes", ln=True)
        pdf.set_text_color(0, 0, 0)
        pdf.ln(2)
        
        for proyecto in proyectos_destacados:
            _render_proyecto_destacado(pdf, proyecto)
            pdf.ln(1)

    # -------------------------
    # EDUCACIÓN
    # -------------------------
    pdf.section_title("Educación")
    pdf.render_education_entry("AIEP", "2026 - 2028", "Ingeniería de Ejecución en Informática, mención Desarrollo de Sistemas")
    pdf.render_education_entry("AIEP", "2024 - 2026", "Programación y Análisis de Sistemas")

    # -------------------------
    # CERTIFICACIONES
    # -------------------------
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


def _render_experiencia_manual(pdf: PDF, datos: dict) -> bool:
    """Renderiza una experiencia laboral manual (verificada)."""
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


def _render_proyecto_destacado(pdf: PDF, proyecto: dict) -> bool:
    """Renderiza un proyecto destacado del portafolio (NO experiencia laboral)."""
    nombre = proyecto.get("nombre", "Proyecto")
    descripcion = proyecto.get("descripcion", "")
    tecnologias = proyecto.get("tecnologias", [])
    
    # Formatear tecnologías
    if isinstance(tecnologias, list):
        tech_str = ", ".join(tecnologias)
    else:
        tech_str = str(tecnologias)
    
    # Nombre del proyecto
    pdf.set_font("Roboto", "B", 9)
    pdf.set_text_color(43, 108, 176)
    pdf.cell(0, 5, nombre, ln=True)
    
    # Tecnologías
    if tech_str:
        pdf.set_font("Roboto", "", 8)
        pdf.set_text_color(80, 80, 80)
        pdf.cell(0, 4, f"Tecnologías: {tech_str}", ln=True)
    
    # Descripción
    if descripcion:
        pdf.set_font("Roboto", "", 8)
        pdf.set_text_color(60, 60, 60)
        pdf.multi_cell(0, 4, limpiar_texto_u(descripcion))
    
    pdf.set_text_color(0, 0, 0)
    return True
