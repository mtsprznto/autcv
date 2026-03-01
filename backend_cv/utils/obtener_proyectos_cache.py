from cachetools import TTLCache

from utils.obtener_proyectos_actualizados import obtener_proyectos_actualizados

# Guardamos la lista por 1 hora (3600s)
proyectos_cache = TTLCache(maxsize=1, ttl=3600)

async def obtener_proyectos_con_cache(username):
    if "lista" in proyectos_cache:
        print("🚀 [CACHE] Usando lista de proyectos guardada")
        return proyectos_cache["lista"]
    
    proyectos = await obtener_proyectos_actualizados(username)
    proyectos_cache["lista"] = proyectos
    return proyectos