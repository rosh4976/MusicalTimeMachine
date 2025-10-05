import requests
from bs4 import BeautifulSoup

def get_billboard_hot_100(year: str):
    """
    Scrape Billboard Hot 100 songs for the last week of the given year.
    
    Args:
        year (str): Year in YYYY format (e.g., "2010")
    
    Returns:
        list: Top 50 song titles (strings)
    """
   
    url = f"https://www.billboard.com/charts/hot-100/{year}-12-31"
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    
    if response.status_code != 200:
        print(f"⚠️ Failed to fetch Billboard data for {year}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

   
    songs = [s.get_text(strip=True) for s in soup.select("li ul li h3")]

    return songs[:50]  
