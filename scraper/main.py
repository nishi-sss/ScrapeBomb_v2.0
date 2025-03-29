from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_jobs(url, exclude_keywords):
    # ブラウザ設定
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()

    # 人間っぽいUser-Agentに偽装（Bot対策）
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    )
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # 必要なら表示バージョンに切り替えOK

    # Chromeドライバー起動
    driver = webdriver.Chrome(service=service, options=options)

    results = []
    page = 1

    # ページ制限（デモ用1ページだけ。提出用ではここだけ変更すれば拡張OK！）
    MAX_PAGE = 1

    while page <= MAX_PAGE:
        driver.get(f"{url}?pg={page}")
        time.sleep(3)  # 読み込み待機（人間ぽく）

        soup = BeautifulSoup(driver.page_source, "html.parser")
        cards = soup.find_all("section", class_="p-result_card")

        if not cards:
            break  # データがなければ終了！

        for card in cards:
            # タイトル取得（煽り文句全部入り）
            title_elem = card.find("h2", attrs={"class": lambda x: x and "p-result_title" in x})
            company_elem = card.find("p", attrs={"class": lambda x: x and "p-result_company" in x})
            employ_elem = card.find("li", attrs={"class": lambda x: x and "p-result_employType" in x})

            # それぞれの要素をテキスト化
            title = title_elem.get_text(strip=True) if title_elem else ""
            company = company_elem.get_text(strip=True) if company_elem else ""
            employ_type = employ_elem.get_text(strip=True) if employ_elem else ""

            # フィルタ用の全文結合（←ここに全部ぶち込んで検索）
            combined_text = f"{title} {company} {employ_type}"

            if any(keyword in combined_text for keyword in exclude_keywords):
                continue  # 除外ワードにヒットしたらスキップ

            # 結果に追加
            results.append({
                "タイトル": title,
                "会社名": company,
                "雇用形態": employ_type
            })

        page += 1  # 次ページへ

    # 終了処理
    driver.quit()
    return pd.DataFrame(results)

