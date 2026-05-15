# Puedes tener esto en un archivo separado como experiencias_estaticas.py
experiencias_manuales = [
    {
        "empresa": "Jurispeed",
        "fecha": "(Mar 2026 - Actualidad)",
        "posicion": "Fullstack AI Engineer / Developer",
        "negocio": "LegalTech; Inteligencia Artificial aplicada al Derecho; Automatización de procesos judiciales.",
        "alcance": (
            "Apoyo técnico en el ciclo de vida de datos para un ecosistema de IA legal. "
            "Diseño e implementación de un motor de ingesta masiva (ETL) en Python para la "
            "indexación de más de 600k sentencias judiciales en una arquitectura RAG. "
            "Desarrollo evolutivo de un chatbot especializado utilizando Vue 3 y FastAPI, "
            "optimizando la recuperación semántica de documentos y la interfaz de usuario "
            "para abogados. Implementación de sistemas de scraping distribuido para la "
            "extracción y limpieza de datos provenientes de portales del Poder Judicial."
        ),
        "stack": "Python (FastAPI), Vue 3, Pinia, TypeScript, Tailwind CSS v4, DynamoDB, Redis, RAG Architecture",
        "cicd": "Git, GitHub, Docker, SSH Tunneling, pnpm, Clerk (Auth/RBAC)",
        "datasources": "Lexintel API (Vector DB), Scrapy/Playwright, REST API, AWS DynamoDB"
    },
    {
        "empresa": "Blast-Up",
        "fecha": "(Mar 2026 - Actualidad)",
        "posicion": "Lead Fullstack Developer",
        "negocio": "Minería Digital y Simulación Geomecánica; Soluciones SaaS para Ingeniería de Tronadura.",
        "alcance": (
            "Liderazgo técnico en el ecosistema digital Blast-Up, desarrollando un simulador de vibraciones en tiempo real "
            "que permite a ingenieros de minas visualizar datos críticos de forma profesional y accesible. "
            "Arquitectura e implementación de visualizaciones 3D complejas con React Three Fiber y mapeo geoespacial "
            "interactivo mediante Leaflet. Desarrollo integral de una plataforma de gestión de certificados y "
            "landing pages de alto rendimiento, integrando seguridad avanzada con Next-Auth y persistencia de datos "
            "robusta con Prisma y PostgreSQL. Optimización de recursos mediante automatización de procesamiento de imágenes "
            "y despliegue de infraestructura en AWS."
        ),
        "stack": "Next.js 16 (React 19), TypeScript, Three.js (React Three Fiber), Tailwind CSS 4, Prisma, PostgreSQL, Zustand, Framer Motion",
        "cicd": "AWS SDK (S3), Vitest (Unit Testing), Prisma Migrations, Scripts de optimización (Node.js)",
        "datasources": "REST API, S3 Presigned URLs, GeoJSON, PostgreSQL"
    },
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