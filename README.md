# AI SEO Content Analyzer

A beginner-friendly Python tool that analyzes blog or website content and suggests simple SEO improvements using an LLM. The project works offline (mock mode) so you can try it without an API key.

## Project overview (in simple words)
This tiny project reads a text file containing your article or page content, calculates basic SEO metrics (word count, keyword frequency, readability checks), and then asks an AI (or uses a mock response) to give suggestions to improve SEO. It's intended for marketers, content writers, and developers starting with AI-driven SEO tools.

## SEO problems D2C (Direct-to-Consumer) brands often face
- Low organic traffic due to poor keyword targeting
- Content that's too long or too short and not structured with headings
- Missing or weak meta descriptions and unclear page titles
- Poor readability for broad audiences (too many long sentences)
- Lack of internal/external links and clear calls-to-action

## How the analyzer works (step-by-step)
1. The script reads content from `sample_content.txt` (or another text file you provide).
2. It tokenizes the text and counts words and sentences.
3. It computes a simple keyword frequency list excluding common stopwords.
4. It runs simple rules-based readability checks:
   - Average sentence length
   - Number of long sentences ( > 20 words)
   - A simple difficulty estimate (Easy / Moderate / Hard)
5. It builds a short summary of these metrics and sends a prompt to an LLM (OpenAI by default) asking for SEO suggestions.
6. If an API key is not available or `--mock` is used, the script prints a helpful mock set of suggestions so you can run the project offline.
7. The script prints the metrics and the AI suggestions to the console.

## Tools & technologies used
- Python 3.8+
- Optional: OpenAI Python client (for connecting to GPT models)
- Plain text files for input and output
- No web server or database — simple local script

## Files in this project
- `analyzer.py` — main script (already added)
- `sample_content.txt` — example blog content to analyze
- `requirements.txt` — Python dependencies
- `README.md` — this file

## How to run the project locally
1. Clone the repo:
   - git clone https://github.com/Neha06-tech/ai-seo-content-analyzer.git
   - cd ai-seo-content-analyzer

2. (Optional) Create and activate a virtual environment:
   - python -m venv venv
   - source venv/bin/activate  # macOS/Linux
   - venv\Scripts\activate     # Windows PowerShell

3. Install dependencies:
   - pip install -r requirements.txt
   - Note: If you don't plan to use OpenAI, you can skip installing the `openai` package or use `--mock` (no API key needed).

4. Run the analyzer with the included example:
   - python analyzer.py
   - or use mock mode (no API key required): python analyzer.py --mock
   - To analyze a different file: python analyzer.py --file path/to/yourfile.txt

5. To use OpenAI's API (optional):
   - Set your API key in the environment: export OPENAI_API_KEY="your_key_here" (macOS/Linux) or setx OPENAI_API_KEY "your_key_here" (Windows)
   - Optionally set the model: export OPENAI_MODEL="gpt-4" (or leave default)
   - Then run without `--mock`.

## Example SEO suggestions (what the AI might output)
- Use a clear H1 that includes your main keyword.
- Add a short meta description (140–160 characters) containing the keyword.
- Use the top 3 keywords naturally in the first 100 words.
- Break long paragraphs into smaller paragraphs (2–3 sentences each).
- Add subheadings (H2/H3) to organize content and include related keywords.
- Include internal links to related pages and at least one external reference.

## Notes for beginners
- The keyword detection here is simplistic (word frequency excluding common stopwords). For production, use more advanced NLP techniques (lemmatization, phrase extraction).
- The mock mode is helpful to understand the workflow without incurring API calls.
- This project is designed to be extended: add meta tag suggestions, SERP snippet previews, or integrate with a CMS.
