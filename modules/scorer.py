# modules/scorer.py

def score_and_rank_images(verified_images: list[dict], original_components: dict) -> list[dict]:
    """
    Scores and ranks images based on verified components and their priorities.
    """
    print("Scoring and ranking images...")
    
    # Create a mapping from component detail to its priority for easy lookup
    priority_map = {comp['detail']: comp['priority'] for comp in original_components['components']}
    
    scored_results = []
    for image_data in verified_images:
        score = 0
        for component_detail, is_present in image_data['matched_components'].items():
            if is_present:
                score += priority_map.get(component_detail, 0)
        
        scored_results.append({
            "image_url": image_data['image_url'],
            "score": score,
            "matched_components": image_data['matched_components']
        })
        
    # Rank images by score in descending order
    ranked_results = sorted(scored_results, key=lambda x: x['score'], reverse=True)
    return ranked_results