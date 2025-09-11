# modules/deconstructor.py
import os
import json
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
# UPDATED: We are now using the more powerful JsonOutputParser
from langchain_core.output_parsers import JsonOutputParser

# Load environment variables from .env file
load_dotenv()

PROMPT_TEMPLATE = """
You are an expert AI assistant for a documentary film company called Vidrush. Your task is to analyze a descriptive sentence from a script and deconstruct it into its core components.

The user will provide a sentence. Break it down into a JSON object containing a list of "components".
For each component, provide:
1. "entity": A category like "Primary Subject", "Primary Setting", "Action", "Held Object", or "Background Element".
2. "detail": The specific detail from the sentence.
3. "priority": A numerical score from 1 (least important) to 10 (most important/non-negotiable). The Primary Subject should almost always be 10.

Analyze the following sentence:
"{user_prompt}"

Output ONLY the JSON object. Do not include any other text or markdown formatting like ```json.
"""

def deconstruct_prompt(prompt: str) -> dict:
    """
    Takes a complex prompt and breaks it down into structured components using the Gemini API.
    """
    print(f"Deconstructing prompt with Gemini: '{prompt}'...")

    try:
        model = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest", google_api_key=os.getenv("GEMINI_API_KEY"))
        
        # UPDATED: Instantiate the JsonOutputParser
        parser = JsonOutputParser()

        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)

        # The chain now automatically parses the JSON output
        chain = prompt_template | model | parser

        # Invoke the chain. The result will be a dictionary, not a string.
        response = chain.invoke({"user_prompt": prompt})
        return response
        
    except Exception as e:
        print(f"An error occurred while calling the Gemini API in deconstructor: {e}")
        return {"components": []}