import aiohttp
import asyncio
from google import genai
import json

async def detect_provider_and_fetch_models(api_key: str):
    if api_key.startswith("sk-or-"):
        provider = "OpenRouter"
        url = "https://openrouter.ai/api/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [m['id'] for m in data.get('data', [])]
                    common = [m for m in models if "gpt-4" in m or "claude" in m or "gemini" in m][:10]
                    if not common:
                        common = models[:10]
                    return provider, common
                else:
                    raise Exception("Invalid OpenRouter API Key")
    elif api_key.startswith("sk-"):
        provider = "OpenAI"
        url = "https://api.openai.com/v1/models"
        headers = {"Authorization": f"Bearer {api_key}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    models = [m['id'] for m in data.get('data', [])]
                    common = [m for m in models if "gpt-4" in m or "gpt-3.5" in m]
                    return provider, common
                else:
                    raise Exception("Invalid OpenAI API Key")
    else:
        provider = "Gemini"
        try:
            client = genai.Client(api_key=api_key)
            models = client.models.list_models()
            available = [m.name.replace('models/', '') for m in models if 'generateContent' in m.supported_generation_methods]
            common = [m for m in available if "flash" in m or "pro" in m][:10]
            if not common:
                common = ["gemini-2.5-flash", "gemini-1.5-pro"]
            return provider, common
        except Exception as e:
            raise Exception("Invalid Gemini API Key or Connection Error")

async def generate_seo_with_provider(provider: str, model: str, api_key: str, html_content: str, project_name: str) -> dict:
    prompt = f"""
    You are an Elite Technical SEO Architect. Your objective is to analyze the following HTML source code of a website named "{project_name}" and generate highly optimized, production-ready SEO tags.
    Focus on high-volume, relevant keywords and compelling meta descriptions that maximize CTR (Click-Through Rate).
    
    You MUST output ONLY a valid JSON object. Do not wrap it in markdown blockquotes or add any extra text.
    The JSON object MUST contain exactly these keys:
    - "title": A highly optimized <title> text (max 60 chars).
    - "description": A compelling <meta name="description"> text (max 160 chars).
    - "keywords": A comma-separated string of 10-15 high-value SEO keywords.
    - "og_title": An engaging Open Graph title for social sharing.
    - "og_description": An engaging Open Graph description.
    - "seo_score": An estimated integer score (0-100) rating the raw HTML content's SEO potential.
    
    HTML Content snippet (first 3000 chars):
    {html_content[:3000]}
    """
    
    try:
        text = ""
        if provider == "Gemini":
            client = genai.Client(api_key=api_key)
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, lambda: client.models.generate_content(
                    model=model, contents=prompt,
                )
            )
            text = response.text.strip()
            
        elif provider in ["OpenAI", "OpenRouter"]:
            url = "https://api.openai.com/v1/chat/completions" if provider == "OpenAI" else "https://openrouter.ai/api/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            if provider == "OpenRouter":
                headers["HTTP-Referer"] = "https://t.me/"
                headers["X-Title"] = "Telegram SEO Bot"
                
            payload = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
            }
            if provider == "OpenAI":
                payload["response_format"] = {"type": "json_object"}
                
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        data = await response.json()
                        text = data['choices'][0]['message']['content'].strip()
                    else:
                        error_text = await response.text()
                        print(f"API Error {response.status}: {error_text}")
                        raise Exception("Failed to generate SEO")
        else:
            raise Exception("Unknown provider")

        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
            
        data = json.loads(text)
        return data
    except Exception as e:
        print(f"Error generating SEO: {e}")
        return {
            "title": project_name,
            "description": f"Welcome to {project_name}",
            "keywords": project_name,
            "og_title": project_name,
            "og_description": f"Welcome to {project_name}",
            "seo_score": 50
        }
