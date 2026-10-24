import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from tavily import TavilyClient
from langchain.tools import tool

load_dotenv()

tavily = TavilyClient(
    api_key = os.getenv("TAVILY_API_KEY")
    )

@tool
def web_search(query: str)-> str:
    """Does the search on the web and gets information."""
    results = tavily.search(query=query,max_results=5)

    out = []

    for r in results.get("results", []):
        out.append(
            f"Title: {r.get('title', 'N/A')}\n"
            f"URL: {r.get('url', 'N/A')}\n"
            f"Snippet: {r.get('content', '')[:300]}\n"
        )

    return "\n-------\n".join(out) or "No search results found."

@tool
def scrape_url(url: str)-> str:
    """Scrapes and return clean text from given url"""
    try:
        resp = requests.get(url, timeout=11, headers={"User-Agent": "Mozilla/5.0"})
        resp.raise_for_status()

        soup = BeautifulSoup(resp.text,"html.parser")

        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()

        return soup.get_text(separator = " ", strip = True)[:3000]
            
    except requests.RequestException as e:
        return f"Could not fetch the URL: {e}"
    
    except Exception as e:
        return f"Could not scrape the URL: {e}"
