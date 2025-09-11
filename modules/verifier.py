# modules/verifier.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# Load environment variables from .env file
load_dotenv()

def verify_image_content(image_url: str, components: dict) -> dict:
    """
    Uses Gemini Pro Vision to verify if components are in an image.
    """
    print(f"Verifying content for image with Gemini Vision: {image_url}...")
    
    verification_results = {
        "image_url": image_url,
        "matched_components": {}
    }

    try:
        # UPDATED: Changed model name to the newer, multimodal version
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=os.getenv("GEMINI_API_KEY"))

        for component in components['components']:
            detail = component['detail']
            prompt_text = f"Analyze the provided image and answer with only the word 'yes' or 'no': Does this image contain a {detail}?"
            
            message = HumanMessage(
                content=[
                    {"type": "text", "text": prompt_text},
                    {"type": "image_url", "image_url": image_url} 
                ]
            )
            response = model.invoke([message])
            answer = response.content.strip().lower()
            verification_results["matched_components"][detail] = "yes" in answer

        return verification_results
    except Exception as e:
        print(f"Could not verify image {image_url}. Error: {e}")
        for component in components['components']:
            verification_results["matched_components"][component['detail']] = False
        return verification_results