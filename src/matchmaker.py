def parse_score(score_str):
    """Convierte el string '45.5%' a un flotante 45.5"""
    try:
        return float(score_str.replace('%', ''))
    except (ValueError, AttributeError):
        return 0.0

def generate_strategy(user1_scores, user2_scores):
    """Evalúa los perfiles Big Five y genera una estrategia de conquista."""
    strategy = ["🎯 ESTRATEGIA DE CONQUISTA:\n"]
    
    # Análisis de Extraversión (Nivel de energía social)
    ext_1 = parse_score(user1_scores.get('Extraversión', '0%'))
    ext_2 = parse_score(user2_scores.get('Extraversión', '0%'))
    
    if ext_2 > 60:
        if ext_1 < 40:
            strategy.append("- Dinámica Social: Tu objetivo es altamente extrovertido. Invítale a lugares animados o eventos sociales, pero establece límites para no agotar tu propia batería social.")
        else:
            strategy.append("- Dinámica Social: Ambos tienen mucha energía. Citas en grupo, conciertos o actividades al aire libre serán un éxito asegurado.")
    elif ext_2 < 40:
        strategy.append("- Dinámica Social: Tu objetivo valora su espacio y tranquilidad. Evita las multitudes; opta por cafés tranquilos, librerías o museos.")

    # Análisis de Apertura a la experiencia (Nivel de innovación)
    ope_2 = parse_score(user2_scores.get('Apertura a la experiencia', '0%'))
    
    if ope_2 > 50:
        strategy.append("- Planes y Citas: Tiene una mente abierta. Sorpréndele con comida exótica, arte abstracto o planes espontáneos y poco convencionales.")
    else:
        strategy.append("- Planes y Citas: Prefiere lo familiar y estructurado. Ve a lo seguro: lugares clásicos, rutinas conocidas y evita los cambios de planes de última hora.")

    # Puedes agregar más reglas para Responsabilidad, Amabilidad y Neuroticismo...

    return "\n".join(strategy)