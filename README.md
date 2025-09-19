# AI Image Search Pipeline

This project is a functional, end-to-end pipeline built to solve the Vidrush coding interview task. It takes a highly specific, complex text description and finds the best possible existing image matches from the web, even when a perfect match is unlikely to exist.

---

### **Approach and Architecture**

[cite_start]The core challenge is to "intelligently compromise" when a perfect image cannot be found[cite: 6]. [cite_start]To solve this, I designed a modular, multi-step pipeline orchestrated with LangChain, which follows the principle of "Separation of Concerns"[cite: 25].

The pipeline operates in four distinct stages:

1.  **Deconstruction:** The initial complex prompt is sent to a powerful Large Language Model (Google's Gemini). The model's task is to act as an expert assistant and break the sentence down into its core components in a structured JSON format. Each component is also assigned a numerical priority (e.g., the primary subject is more important than a background element). [cite_start]This directly addresses the need to "break down complex requirements"[cite: 22].

2.  **Search:** The highest-priority components from the deconstruction phase are used to generate a concise, targeted search query. This query is then sent to the Google Custom Search API to retrieve a small pool of the most relevant candidate images from the web.

3.  **Verification:** This is the key to handling partial matches. Each candidate image is analyzed by a multimodal vision model (Gemini Pro Vision). For every single component identified in Step 1, the vision model is asked a direct question (e.g., "Does this image contain an umbrella?") and must return a "yes" or "no" answer.

4.  **Scoring & Ranking:** The verification results are fed into a scoring system. Each image's score is calculated based on the priorities of the components it contains. An image that contains a high-priority subject will score higher than an image that only contains a low-priority background element. The final list of images is then ranked by this score and presented to the user. [cite_start]This fulfills the requirement to "implement a scoring system that weighs different aspects of the description"[cite: 26].

[cite_start]The entire pipeline includes robust error handling to gracefully manage potential API failures, such as rate limits, without crashing[cite: 41].

---

### **API Keys Needed**

As per the task instructions, the pipeline requires the following API keys to function. These should be placed in a `.env` file in the root of the project.

* `GEMINI_API_KEY`: For the Google Gemini (Language and Vision) model.
* `GOOGLE_API_KEY`: For the Google Cloud Custom Search service.
* `GOOGLE_CSE_ID`: The ID for the specific Programmable Search Engine configuration.

---

### **Setup and Configuration Instructions**

1.  **Prerequisites:** Python 3.8+
2.  **Download:** Download and unzip the source code into a local directory.
3.  **Navigate:** Open a terminal and navigate into the project's root directory.
    ```bash
    cd path/to/vidrush_task
    ```
4.  **Create Virtual Environment:**
    ```bash
    python -m venv venv
    ```
5.  **Activate Environment:**
    * On Windows: `.\venv\Scripts\activate`
    * On macOS/Linux: `source venv/bin/activate`
6.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
7.  **Configure API Keys:**
    * Create a file named `.env` in the root directory.
    * Copy the following content into it and replace the placeholders with your actual keys:
        ```
        GEMINI_API_KEY="your_ai_studio_key_here"
        GOOGLE_API_KEY="your_google_cloud_key_here"
        GOOGLE_CSE_ID="your_programmable_search_engine_id_here"
        ```
8.  **Run the Pipeline:**
    * The script is configured to run all four test prompts from the task description.
    ```bash
    python main.py
    ```

### Note on API Rate Limiting
This application uses free-tier APIs, which have strict rate limits (e.g., requests per minute and per day). The script includes `time.sleep()` calls and error handling to manage this, but if the daily quota is exhausted, API calls will fail. The error handling is designed to allow the program to complete gracefully in this event, typically resulting in a score of 0 for the affected items.
