from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Anclajes semánticos del modelo OCEAN universalizados para cualquier tipo de perfil
ANCHORS = {
    "Apertura a la experiencia": "Soy una persona creativa, curiosa y de mente abierta. Me gusta explorar nuevas ideas, el arte, la innovación y vivir experiencias poco convencionales.",
    "Responsabilidad": "Soy una persona organizada, responsable y disciplinada. Me enfoco en mis objetivos, valoro el orden, la constancia y el trabajo bien hecho.",
    "Extraversión": "Soy una persona sociable, extrovertida y llena de energía. Disfruto interactuar con otros, participar en actividades grupales y expresarme abiertamente.",
    "Amabilidad": "Soy una persona empática, amable y cooperativa. Me preocupo genuinamente por los demás, busco la armonía, el respeto y ayudar a mi entorno.",
    "Neuroticismo": "A veces experimento emociones intensas, estrés o ansiedad. Soy sensible a mi entorno, reflexiono mucho sobre mis preocupaciones y puedo ser emocionalmente vulnerable."
}

def analyze_big_five(profile_data: dict) -> dict:
    # 1. Construir el corpus concatenando bio y textos de los videos
    corpus_parts = [profile_data.get("bio", "")]
    for post in profile_data.get("recent_posts", []):
        corpus_parts.append(post.get("text", ""))
    
    full_text = " ".join(corpus_parts).strip()
    word_count = len(full_text.split())
    
    # 2. Umbral de validación estricto
    if word_count < 50:
        return {
            "status": "Rechazado",
            "reason": f"Corpus insuficiente ({word_count} palabras). Se requieren mínimo 50.",
            "scores": None
        }
    
    # 3. Vectorización con Hugging Face
    print(f"\n[NLP] Analizando personalidad (Corpus: {word_count} palabras)...")
    # Carga el modelo ligero y eficiente de sentence-transformers
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    user_embedding = model.encode([full_text])
    
    # 4. Cálculo de Similitud del Coseno
    results = {}
    for trait, anchor_text in ANCHORS.items():
        anchor_embedding = model.encode([anchor_text])
        similarity = cosine_similarity(user_embedding, anchor_embedding)[0][0]
        
        # Convertimos la similitud matemática a un porcentaje legible
        score_pct = max(0, min(100, round(float(similarity) * 100, 2)))
        results[trait] = f"{score_pct}%"
        
    return {
        "status": "Completado",
        "word_count": word_count,
        "scores": results
    }