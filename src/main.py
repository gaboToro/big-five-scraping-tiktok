import os
import json
import asyncio

from src.session_manager import generate_session, COOKIE_PATH
from src.profile_scraper import get_profile_info
from src.post_scraper import get_recent_posts
from src.nlp_analyzer import analyze_big_five
from src.matchmaker import generate_strategy

async def run_matchmaker_pipeline(user1, user2):
    """Orquesta la extracción asíncrona de ambos usuarios y calcula la compatibilidad."""
    print(f"\n[1/3] Procesando el perfil de {user1}...")
    # Agregamos 'await' porque run_pipeline es asíncrono
    data_user1 = await run_pipeline(user1) 
    
    print(f"\n[2/3] Procesando el perfil de {user2}...")
    # Agregamos 'await' aquí también
    data_user2 = await run_pipeline(user2)
    
    print("\n[3/3] Calculando estrategia de conquista (Matchmaker)...")
    strategy = generate_strategy(
        data_user1.get("big_five_analysis", {}).get("scores", {}),
        data_user2.get("big_five_analysis", {}).get("scores", {})
    )
    
    # Consolidar el reporte de la pareja
    match_report = {
        "user1_profile": data_user1,
        "user2_profile": data_user2,
        "strategy": strategy
    }
    
    os.makedirs("reports", exist_ok=True)
    filepath = f"reports/match_{user1.replace('@', '')}_{user2.replace('@', '')}.json"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(match_report, f, indent=4, ensure_ascii=False)
        
    print(f"\n✅ ¡Matchmaker completado! Reporte guardado en: {filepath}")
    return filepath

async def run_pipeline(username: str):
    clean_username = username if username.startswith("@") else f"@{username}"
    
    print("=" * 50)
    print(f" Iniciando extracción para {clean_username}")
    print("=" * 50)

    if not os.path.exists(COOKIE_PATH):
        print("\n[PREPARACIÓN] No se encontraron cookies guardadas. Generando sesión...")
        await generate_session()
    else:
        print(f"\n[PREPARACIÓN] Reutilizando sesión existente...")

    print(f"\n[1/3] Extrayendo datos del perfil...")
    try:
        profile_data = await get_profile_info(clean_username)
    except Exception as e:
        print(f"[ERROR] Falló la extracción del perfil: {e}")
        return None

    print("\n[2/3] Extrayendo métricas de publicaciones...")
    try:
        posts = await get_recent_posts(clean_username, limit=7)
        profile_data["recent_posts"] = posts
    except Exception as e:
        print(f"[ERROR] Falló la extracción de publicaciones: {e}")
        profile_data["recent_posts"] = []

    print("\n[3/3] Evaluando perfil psicológico (Big Five)...")
    try:
        big_five_results = analyze_big_five(profile_data)
        profile_data["big_five_analysis"] = big_five_results
    except Exception as e:
        print(f"[ERROR] Falló el análisis NLP: {e}")
        profile_data["big_five_analysis"] = {"status": "Error", "reason": str(e)}

    os.makedirs("reports", exist_ok=True)
    clean_name = clean_username.replace('@', '')
    output_filename = f"reports/report_{clean_name}.json"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(profile_data, f, indent=4, ensure_ascii=False)

    print(f"✅ PROCESO FINALIZADO. Datos guardados en: {output_filename}")
    return output_filename # Retornamos la ruta para que la GUI la lea

# Mantenemos el bloque por si quieres ejecutarlo desde consola para pruebas
if __name__ == "__main__":
    test_user = input("Ingresa el username de TikTok: ")
    asyncio.run(run_pipeline(test_user))