import json
import time
import traceback
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from cv.generarCv import generar_cv


from models.PropuestaInput import PropuestaInput
from models.PreguntaInput import PreguntaInput

from utils.obtener_proyectos_cache import obtener_proyectos_con_cache
from utils.obtener_proyectos_actualizados import obtener_proyectos_actualizados, anadir_readme_proyectos_seleccionados
from utils.utils import limpiar_texto_u, preparar_readme_para_modelo

from ia.preguntar import generar_experiencia_desde_readme_async, seleccionar_proyectos, responder_propuesta, generar_experiencia_desde_readme

from cv.static_exp import experiencias_manuales



app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://autcv.vercel.app",
        "http://localhost:3001",
        "http://localhost:3000",
        "https://autcv.mtsprz.org"
    ],         # Puedes usar ["*"] si querés permitir todo (no recomendado para producción)
    allow_credentials=True,
    allow_methods=["*"],                    # ["GET", "POST", ...] si querés limitar
    allow_headers=["*"],                    # ["Content-Type", "Authorization", ...]
    expose_headers=["*"]
)

# Servir archivos estáticos desde output/ (solo en local)
output_dir = os.path.join(os.path.dirname(__file__), "output")
if os.path.exists(output_dir):
    app.mount("/output", StaticFiles(directory=output_dir), name="output")




username: str = "mtsprznto"

"""
GET
"""
@app.get("/")
def read_root():
    return {"Backend": "AUTCV"}


@app.get("/repos-actualizados")
async def obtener_repos():
    """
    Obtiene los proyectos actualizados de GitHub para un usuario específico.
    """
    # proyectos_pre
    
    proyectos = await obtener_proyectos_actualizados(username)

    return JSONResponse(content=proyectos)


"""
POST
"""
@app.post("/propuesta")
async def recibir_propuesta(payload: PropuestaInput):
    """
    Recibe una propuesta laboral y devuelve una lista de proyectos seleccionados.
    """
    inicio_total = time.perf_counter()

    try:
        # ====================================================================
        # ====================================================================
        # ====================================================================
        t0 = time.perf_counter()
        
        # proyectos seleccionados
        # aqui viene groq
        #proyectos = await obtener_proyectos_actualizados(username)
        proyectos =  await obtener_proyectos_con_cache(username)
        print(f"⏱️ Obtener proyectos: {time.perf_counter() - t0:.2f}s | Total: {len(proyectos)}")
        # ====================================================================
        # ====================================================================
        # ====================================================================
        t1 = time.perf_counter()
        # aqui se genera con groq (IA)
        proyectos_seleccionados = seleccionar_proyectos(proyectos, payload.normalizada())
        print(f"⏱️ Selección (IA): {time.perf_counter() - t1:.2f}s | Seleccionados: {len(proyectos_seleccionados)}")
        

        # Aplanar proyectos seleccionados
        proyectos_seleccionados_flat = [p[0] if isinstance(p, list) else p for p in proyectos_seleccionados]
        # ====================================================================
        # ====================================================================
        # ====================================================================
        t2 = time.perf_counter()
        #obtener readme raw
        proyectos_seleccionados_readme = await anadir_readme_proyectos_seleccionados(username, proyectos_seleccionados_flat)
        print(f"⏱️ Fetch Readmes: {time.perf_counter() - t2:.2f}s")


        for proyecto in proyectos_seleccionados_readme:
            proyecto["readme_raw"] = preparar_readme_para_modelo(proyecto["readme_raw"])

        # ====================================================================
        # ====================================================================
        # ====================================================================
        t3 = time.perf_counter()

        # Generar descripciones de PROYECTOS DESTACADOS (no experiencias laborales)
        proyectos_ia_raw = await generar_experiencia_desde_readme_async(
            payload.normalizada(), 
            proyectos_seleccionados_readme
        )

        # Empresas manuales que NUNCA deben aparecer como proyectos IA
        empresas_manuales = {exp["empresa"].lower().strip() for exp in experiencias_manuales}

        proyectos_destacados = []  # Solo para sección "Proyectos Destacados" del CV

        for proyecto, exp_raw in zip(proyectos_seleccionados_readme, proyectos_ia_raw):
            if exp_raw:
                # Limpieza de caracteres unicode
                exp_limpia = {k: limpiar_texto_u(v) if isinstance(v, str) else v for k, v in exp_raw.items()}
                
                # FILTRO CRÍTICO: descartar si parece experiencia laboral inventada
                proyecto_nombre = exp_limpia.get("proyecto", "").lower().strip()
                empresa_nombre = exp_limpia.get("empresa", "").lower().strip()
                
                # No incluir si el nombre coincide con una empresa manual
                if proyecto_nombre in empresas_manuales or empresa_nombre in empresas_manuales:
                    print(f"⏭️ [FILTRADA] Duplica empresa manual: {exp_limpia.get('proyecto') or exp_limpia.get('empresa')}")
                    continue
                
                # Guardar como proyecto destacado (NO como experiencia laboral)
                proyectos_destacados.append({
                    "nombre": proyecto.get("name", exp_limpia.get("proyecto", "Proyecto")),
                    "tecnologias": exp_limpia.get("tecnologias", exp_limpia.get("stack", [])),
                    "descripcion": exp_limpia.get("descripcion", exp_limpia.get("experiencia_cv", "")),
                    "relevancia": exp_limpia.get("relevancia", ""),
                })
                
                print(f"✅ [PROYECTO] Destacado: {proyecto.get('name')}")
            else:
                print(f"⚠️ [DEBUG] Falló generación para: {proyecto.get('name')}")

        print(f"⏱️ Generar proyectos (IA Paralela): {time.perf_counter() - t3:.2f}s")
        
        # ====================================================================
        # ====================================================================
        # ====================================================================
        t4 = time.perf_counter()
        # Pasar experiencias manuales + proyectos destacados (separados)
        url_pdf = await generar_cv(
            proyectos_seleccionados_flat, 
            experiencias_manuales,  # Solo las manuales como experiencia laboral
            proyectos_destacados,   # Proyectos IA como destacados
            "CV_Matias_Perez_Nauto.pdf"
        )
        print(f"⏱️ PDF Generación + Upload: {time.perf_counter() - t4:.2f}s")

        tiempo_final = time.perf_counter() - inicio_total
        print(f"✅ PROCESO COMPLETADO en {tiempo_final:.2f}s")


        return JSONResponse(content={
            "cv_url": url_pdf
        })
    except Exception as e:
        print(f"❌ ERROR INTERNO tras {time.perf_counter() - inicio_total:.2f}s: {str(e)}")
        print(traceback.format_exc())
        return JSONResponse(status_code=500, content={"error": "Fallo interno en propuesta"})



@app.post("/responder")
async def recibir_pregunta(payload: PreguntaInput):
    """
    Recibe preguntas sobre propuesta laboral y devuelve una respueta adecuada a la propuesta laboral.
    """
    try:
        #print(payload.pregunta)
        proyectos = await obtener_proyectos_actualizados(username)
        respuestas = responder_propuesta(proyectos=proyectos, pregunta=payload.pregunta)

        return JSONResponse(content={
            "respuestas": respuestas
        })
        
        
    except Exception as e:
        print("❌ ERROR INTERNO:", str(e))
        return JSONResponse(status_code=500, content={"error": "Fallo interno en responder"})