import os
from config import GEMINI_API_KEY
from services.ai_factory import generate_seo_with_provider


async def analyze_seo(directory_path: str, project_name: str, settings: dict) -> dict:
    """Analyze the first .html found. Returns defaults if none found."""
    html_path = os.path.join(directory_path, "index.html")
    if not os.path.exists(html_path):
        for root, _, files in os.walk(directory_path):
            for f in files:
                if f.endswith(".html") or f.endswith(".htm"):
                    html_path = os.path.join(root, f)
                    break
            if os.path.exists(html_path):
                break

    if not os.path.exists(html_path):
        return {
            "score": 50,
            "report": f"⚠️ No HTML file found in `{project_name}`.",
            "title": project_name,
            "description": "",
            "keywords": "",
        }

    with open(html_path, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    ai_key = settings.get("ai_api_key")
    if not ai_key:
        ai_key = GEMINI_API_KEY

    if not ai_key:
        score = 50
        return {
            "score": score,
            "report": "No AI key configured. Set one in Settings to get SEO analysis.",
            "title": project_name,
            "description": "",
            "keywords": "",
        }

    ai_provider = settings.get("ai_provider") or "Gemini"
    ai_model = settings.get("ai_model") or "gemini-2.5-flash"

    seo_data = await generate_seo_with_provider(
        ai_provider, ai_model, ai_key, html_content, project_name
    )

    score = seo_data.get("seo_score", 50)
    title = seo_data.get("title", "")
    description = seo_data.get("description", "")
    keywords = seo_data.get("keywords", "")
    og_title = seo_data.get("og_title", "")

    report_lines = [
        f"📈 *SEO Analysis Report — {project_name}*",
        f"🏆 Score: *{score}/100*",
        "",
        f"📌 *Suggested Title:*\n`{title}`",
        f"📝 *Suggested Description:*\n`{description}`",
        f"🔑 *Suggested Keywords:*\n`{keywords}`",
        f"📣 *OG Title:*\n`{og_title}`",
    ]

    seo_data["report"] = "\n".join(report_lines)
    seo_data["score"] = score
    return seo_data
