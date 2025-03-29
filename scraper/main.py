import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_jobs(url, exclude_keywords):
    results = []

    # デモ用に最大3ページ（適宜調整）
    MAX_PAGE = 3

    for page in range(1, MAX_PAGE + 1):
        response = requests.get(f"{url}?pg={page}", headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })

        if response.status_code != 200:
            print(f"ページ {page} の取得に失敗しました。")
            break

        soup = BeautifulSoup(response.text, "html.parser")
        cards = soup.find_all("section", class_="p-result_card")

        if not cards:
            break

        for card in cards:
            title_elem = card.find("h2", class_="p-result_title--ver2")
            company_elem = card.find("p", class_="p-result_company")
            employ_elem = card.find("li", class_="p-result_employType")

            title = title_elem.get_text(strip=True) if title_elem else ""
            company = company_elem.get_text(strip=True) if company_elem else ""
            employ_type = employ_elem.get_text(strip=True) if employ_elem else ""

            combined = f"{title} {company} {employ_type}"
            if any(keyword in combined for keyword in exclude_keywords):
                continue

            results.append({
                "タイトル": title,
                "会社名": company,
                "雇用形態": employ_type
            })

    return pd.DataFrame(results)

