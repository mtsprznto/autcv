
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))


from utils.utils import chunk_text
from ia.connect import get_groq_client
import json

import re


def seleccionar_proyectos(proyectos: list, propuesta: str = "No especificada") -> str:
    """
    Analiza una lista completa de proyectos y genera una selección recomendada
    para mostrar en el CV según la propuesta dada.
    """
    client = get_groq_client("GROQ_API_KEY_1")
    model_name = os.getenv("MODEL_1") 
    if not model_name:
        raise EnvironmentError("❌ MODEL_1 no está definido en las variables de entorno.")
    # Serializar proyectos a texto
    proyectos_json = json.dumps(proyectos, ensure_ascii=False, indent=2)

    chunks = chunk_text(proyectos_json, max_tokens=2000)
    proyectos_seleccionados = []


    for i, chunk in enumerate(chunks, start=1):
        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un asistente técnico especializado en selección de proyectos para currículums. "
                    "Tu tarea es analizar una propuesta laboral y devolver una lista en formato JSON con los proyectos más relevantes "
                    "para mostrar en el CV. Usa exclusivamente el formato original que se te proporciona, sin modificar los campos ni agregar nuevos. "
                    "Tu única salida debe ser un array JSON con los objetos seleccionados, sin explicaciones ni texto adicional."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Propuesta laboral:\n{propuesta}\n\n"
                    f"Chunk {i} de proyectos:\n{chunk}\n\n"
                    "Selecciona los más relevantes para incluir en el CV y devuélvelos en formato JSON."
                )
            }
        ]

        try:
            chat_completion = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            raw_output = chat_completion.choices[0].message.content.strip()
            seleccion_chunk = json.loads(raw_output)
            proyectos_seleccionados.extend(seleccion_chunk)
        except Exception as e:
            print(f"❌ Error al procesar chunk {i}: {e}")

    return proyectos_seleccionados



def generar_experiencia_desde_readme(propuesta: str, proyectos: list) -> list:
    """
    Genera experiencias profesionales adaptadas al CV usando los README
    y alineadas con la propuesta laboral.
    """
    client = get_groq_client("GROQ_API_KEY_2")

    model_name = os.getenv("MODEL_2") 
    if not model_name:
        raise EnvironmentError("❌ MODEL_2 no está definido en las variables de entorno.")
    experiencias_adaptadas = []


    # Procesar cada proyecto individualmente para no superar el límite de tokens
    for proyecto in proyectos:
        proyecto_json = json.dumps(proyecto, ensure_ascii=False, indent=2)

        messages = [
            {
                "role": "system",
                "content": (
                    "Eres un experto en redacción de currículums técnicos. "
                    "Tu tarea es leer el README de cada proyecto y generar una experiencia profesional adaptada al CV, alineada con la propuesta laboral. "
                    "Extrae palabras clave relevantes y redacta una descripción profesional, clara y orientada al impacto. "
                    "Tu única salida debe ser SOLO un objeto JSON válido. No escribas nada antes ni después."
                    "Devuelve un array JSON con los siguientes campos por cada experiencia:\n"
                    " - empresa: nombre de la empresa o proyecto\n"
                    " - fecha: rango de tiempo (ej. May 2024 - Ago 2024)\n"
                    " - titulo: cargo desempeñado\n"
                    " - posicion: rol específico (ej. SRE, Frontend Developer)\n"
                    " - business: sector o tipo de negocio\n"
                    " - experiencia_cv: descripción clara y orientada al impacto\n"
                    " - stack: lista de tecnologías usadas\n"
                    " - cicd: herramientas de CI/CD\n"
                    " - observabilidad: herramientas de monitoreo/observabilidad\n"
                    " - vcs: sistema de control de versiones\n"
                    " - datasources: bases de datos o fuentes de datos\n"
                    " - keywords_detectadas: palabras clave relevantes\n\n"
                    "No incluyas explicaciones ni texto adicional fuera del JSON."
                    "Ten en cuenta lo siguiente:\n"
                    "- Agregar logros medibles en cada experiencia.\n"
                    "- Incluir responsabilidades específicas y resultados.\n"
                    "- Detallar duración y contexto de cada rol.\n"
                    "- Relacionar experiencia con habilidades clave.\n"
                    "- Buscar incluir experiencia formal o voluntariados.\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"Propuesta laboral:\n{propuesta}\n\n"
                    f"Proyecto con README:\n{proyecto_json}\n\n"
                    "Devuélveme el objeto JSON con la experiencia adaptada para el CV."
                )
            }
        ]

        try:
            chat_completion = client.chat.completions.create(
                model=model_name,
                messages=messages
            )
            raw_output = chat_completion.choices[0].message.content.strip()
            match = re.search(r"```json\s*(\[.*?\]|\{.*?\})\s*```", raw_output, re.DOTALL)

            if match:
                json_str = match.group(1).strip()
            else:
                # Si no hay delimitadores, intenta parsear directamente
                json_str = raw_output.strip()
                json_str = json_str.strip("`")
            if not json_str:
                print(f"⚠️ Salida vacía para proyecto {proyecto.get('empresa','?')}")
                continue


            try:
                experiencia = json.loads(json_str)
                if isinstance(experiencia, list):
                    experiencias_adaptadas.extend(experiencia)  # añadir todos los objetos
                elif isinstance(experiencia, dict):
                    experiencias_adaptadas.append(experiencia)
                else:
                    print("⚠️ Tipo inesperado:", type(experiencia))
            except json.JSONDecodeError as e:
                print(f"❌ JSON malformado para proyecto {proyecto.get('empresa','?')}: {e}")
                print("Contenido recibido:", repr(json_str))
                continue
        except Exception as e:
            print(f"❌ Error al procesar proyecto {proyecto.get('empresa','?')}: {e}")

    return experiencias_adaptadas



def responder_propuesta(proyectos: list, pregunta: str)-> str:
    """
    Recibe preguntas sobre propuesta laboral y responde en base a los proyectos que se entregan
    """
    client = get_groq_client()
    
    año_inicio_programacion = "2024"
    
    
    messages = [
        {
            "role": "system",
            "content": (
                "Eres un asistente técnico especializado en construir respuestas laborales personalizadas para postulantes en Latinoamérica. "
                "Tu tarea es analizar preguntas relacionadas a propuestas laborales y responder en primera persona, como si el postulante estuviera hablando directamente. "
                "Tenés que basarte en los proyectos entregados por el usuario, considerando su historial técnico, las tecnologías utilizadas y la duración de cada trabajo. "
                "Adaptá el lenguaje al contexto profesional de Chile y países hispanohablantes, incluyendo rangos salariales si aplica. "
                "La respuesta debe ser concreta, profesional y personalizada. Evitá generalidades, introducciones innecesarias o respuestas genéricas. "
                f"El usuario comenzó a programar en {año_inicio_programacion}. Considera esto para estimar su nivel de experiencia, responsabilidad técnica y expectativa salarial."
            )
        },
        {
            "role": "user",
            "content": (
                f"Pregunta:\n{pregunta}\n\n"
                f"Lista de proyectos (estructura original):\n{json.dumps(proyectos, ensure_ascii=False, indent=2)}\n\n"
                "Redactá la respuesta como si yo mismo la estuviera diciendo. "
                "Tené en cuenta mi experiencia técnica, el nivel que tengo hoy, y adaptá el tono a un contexto profesional chileno actual. "
                f"Tengo {2025 - int(año_inicio_programacion)} años de experiencia. Basate en eso para sugerir rangos salariales y responsabilidades acordes a un perfil junior o semi-senior. "
                "Si la pregunta está relacionada con remuneración, entregá una estimación mensual líquida realista en CLP."
            )
        }
    ]

    try:
        chat_completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # adaptá a tu modelo disponible
            messages=messages
        )
        raw_output = chat_completion.choices[0].message.content.strip()
        
        return raw_output
    except Exception as e:
        print(f"❌ Error al generar CV adaptado [responder_propuesta]: {e}")
        return "No se pudo adaptar el CV correctamente."
