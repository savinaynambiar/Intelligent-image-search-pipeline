# main.py

# Import the functions from your modules
from modules.deconstructor import deconstruct_prompt
from modules.search import search_for_images
from modules.verifier import verify_image_content
from modules.scorer import score_and_rank_images
import time

def run_pipeline(prompt: str):
    """
    Executes the full image search and ranking pipeline.
    """
    print("--- Starting Pipeline ---")
    
    deconstructed_components = deconstruct_prompt(prompt)
    if not deconstructed_components or not deconstructed_components.get('components'):
        print("Could not deconstruct prompt. Exiting.")
        return
    
    candidate_urls = search_for_images(deconstructed_components)
    if not candidate_urls:
        print("No images found for the prompt. Exiting.")
        return
        
    verified_images_data = []
    # MODIFICATION: Loop over only the first 3 images to conserve API quota
    for url in candidate_urls[:3]:
        verified_data = verify_image_content(url, deconstructed_components)
        verified_images_data.append(verified_data)
        time.sleep(1) 
        
    final_ranked_list = score_and_rank_images(verified_images_data, deconstructed_components)
    
    print("\n--- Final Ranked Results ---")
    if not final_ranked_list:
        print("No suitable images were found after scoring.")
    else:
        for result in final_ranked_list:
            print(f"URL: {result['image_url']}, Score: {result['score']}")
            print(f"   Matches: {result['matched_components']}")
        
    print("\n--- Pipeline Finished ---")


if __name__ == "__main__":
    test_prompts = [
        "Elon Musk standing in a grass field holding an umbrella with a circus in the background",
        "A golden retriever wearing sunglasses riding a skateboard on a beach at sunset",
        "An astronaut playing chess with a robot on top of a mountain",
        "A Victorian-era woman using a modern smartphone in a library"
    ]

    for i, p in enumerate(test_prompts):
        print(f"\n==================== RUNNING TEST {i+1}/{len(test_prompts)} ====================")
        print(f"PROMPT: '{p}'")
        run_pipeline(p)
        time.sleep(10)