from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.utils import formatear_proyecto, combinar_repos, agregar_proyecto

def procesar_repositorios(repositories: list, github, username: str) -> list:
    if not repositories:
        print("❌ No hay repositorios para procesar.")
        return []

    print(f"\nFound {len(repositories)} repositories:")
    print("-" * 80)

    sorted_repos = sorted(repositories, key=lambda x: x['updated_at'], reverse=True)

    proyectos_cv = [formatear_proyecto(r) for r in sorted_repos]

    # Los datos de "about" ya están en el objeto de la lista — sin HTTP extra
    proyectos_about = [
        {
            "nombre": r.get("name"),
            "descripcion": r.get("description"),
            "sitio_web": r.get("homepage"),
            "topics": r.get("topics", []),
            "url": r.get("html_url"),
            "lenguaje": r.get("language"),
            "actualizado": r.get("updated_at")
        }
        for r in sorted_repos
    ]

    # Paralelizar fetch de lenguajes (único endpoint adicional necesario)
    nombres = [r.get("name") for r in sorted_repos]
    proyectos_lenguajes = [{}] * len(sorted_repos)
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(github.get_languages_for_repo, username, name): i
            for i, name in enumerate(nombres)
        }
        for future in as_completed(futures):
            idx = futures[future]
            try:
                proyectos_lenguajes[idx] = future.result()
            except Exception:
                proyectos_lenguajes[idx] = {}

    proyectos_combinados = combinar_repos(proyectos_cv, proyectos_about, proyectos_lenguajes)

    proyectos_agregados = []
    for idx, proyecto in enumerate(proyectos_combinados):
        print(f"Proyecto {idx}: {proyecto['repositorio']}")
        proyectos_agregados.append(agregar_proyecto(proyecto))

    return proyectos_agregados
