# modules/search.py
import os
from dotenv import load_dotenv
from googleapiclient.discovery import build

# Load environment variables from .env file
load_dotenv()

def search_for_images(components: dict) -> list[str]:
    """
    Takes deconstructed components and searches for images using the Google Custom Search API.
    """
    print("Searching for images with Google Search API...")
    
    if not components or not components.get('components'):
        return []
    
    # Create a search query from the top 2-3 components based on priority
    sorted_components = sorted(components['components'], key=lambda x: x['priority'], reverse=True)
    query = " ".join([comp['detail'] for comp in sorted_components[:2]])
    print(f"Generated search query: '{query}'")

    try:
        # Build the custom search service
        service = build("customsearch", "v1", developerKey=os.getenv("GOOGLE_API_KEY"))
        
        # Execute the search
        res = service.cse().list(
            q=query,
            cx=os.getenv("GOOGLE_CSE_ID"),
            searchType='image',
            num=5  # Get the top 5 image results
        ).execute()

        # Extract the image links, filtering out any potential non-string items
        items = res.get('items', [])
        image_urls = [item['link'] for item in items if 'link' in item and isinstance(item['link'], str)]
        return image_urls
    except Exception as e:
        print(f"An error occurred during image search: {e}")
        return []