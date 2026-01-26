# Puedes tener esto en un archivo separado como experiencias_estaticas.py
experiencias_manuales = [
    {
        "empresa": "Fundación Bienestar Animal",
        "fecha": "(Sep 2025 - Actualidad)",
        "posicion": "Desarrollador Frontend",
        "negocio": "Fundaciones y corporaciones; Asociaciones culturales o recreativas.",
        "alcance": (
            "Responsable de la modernización de la plataforma digital de la fundación. "
            "Diseño y desarrollo de interfaces de usuario escalables utilizando Next.js y Tailwind CSS, "
            "asegurando un enfoque Mobile-First. Implementación de componentes modulares bajo "
            "el patrón Atomic Design y consumo de APIs REST/GraphQL."
        ),
        "stack": "Next.js, React, TypeScript, Tailwind CSS, HTML5, CSS3, Atomic Design",
        "cicd": "Git, GitHub, Figma (Diseño UI/UX)",
        "datasources": "REST API, GraphQL"
    },
    {
        "empresa": "FIE",
        "fecha": "(Nov 2025 - Actualidad)",
        "posicion": "Desarrollador Fullstack",
        "negocio": "Automatización de procesos contables y rendición de cuentas para el sector educativo (Supereduc).",
        "alcance": (
            "Desarrollo integral (End-to-End) de 'FIE', plataforma para la automatización de la acreditación de gastos ante la Supereduc. "
            "Lideré el diseño de la arquitectura Fullstack utilizando FastAPI y Next.js, implementando un pipeline de procesamiento de documentos financieros. "
            "Desarrollé un motor de extracción de datos mediante OCR (Groq API / Tesseract) para la captura automática de RUT, montos y fechas desde facturas y boletas. "
            "Implementé un algoritmo de clasificación contable semántica basado en el Manual de Cuentas 2025, automatizando la asignación de códigos y validación de rendibilidad para programas SEP, PIE y Mantenimiento. "
            "Orquestación de servicios mediante Docker y gestión de almacenamiento persistente en AWS Buckets, con capacidad de exportación multiformato (JSON, CSV, PDF)."
        ),
        "stack": "Python (FastAPI), Docker, Next.js, TypeScript, PostgreSQL, AWS Buckets",
        "cicd": "Git, GitHub, Docker Compose",
        "datasources": "PostgreSQL (Relational Data), AWS S3 Buckets (Document Storage, Groq/Tesseract (OCR Data Extraction), Manual de Cuentas Supereduc 2025 (Reference Data)"
    },
    # Aquí puedes agregar más fácilmente copiando el bloque anterior
]