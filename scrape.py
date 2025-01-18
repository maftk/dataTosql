from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
from google.cloud import storage
import os

PROJECT_ID = os.environ["PROJECT_ID"]

def gs_save(df):
    file_path = "info.csv"
    csv_str = df.to_csv(index=False)

    bucket_name = f"{PROJECT_ID}-trade"
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        bucket.create()
    blob = bucket.blob(file_path)
    blob.upload_from_string(csv_str, "text/csv")
    print(f"DataFrameをGCSに保存しました: gs://{bucket_name}/{file_path}")

def scrape_data_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()  # または p.firefox.launch(), p.webkit.launch()
        page = browser.new_page()

        headers = [
            'id',    # No.
            'code',   # コード
            'company',  # 会社名
            'market', # 市場
            'current', # 株価
            'compared', # 前日比
            'percent',   # 単位
            'unit', # 前日
            'purchase', # 現在
            'deviation', # 前日比 (重複)
            'PER', # クォンツ スコア
            'PBR', # 割安度 スコア
        ]
        try:
            data_path = "https://jp.kabumap.com/servlets/kabumap/Action?SRC=stockRanking/base&ind=unit&exch=T1&d=d"
            page.goto(data_path)
            data = []
            for c in range(10):
                # ページネーションの要素をクリック
                pagination_links = page.locator('#KM_TABLEINDEX0 .KM_TABLEINDEX_FIGURE')
                awaiting_navigation = page.wait_for_load_state() # ナビゲーション完了を待つ
                pagination_links.nth(c).click()
                awaiting_navigation

                # テーブルの行を取得
                records = page.locator('#KM_TABLECONTENT0 tr').all()
                for record in records:
                    td_elements = record.locator('td').all()
                    tds = [td.text_content() for td in td_elements]
                    print(tds)
                    if tds:
                        data.append(tds)

            df = pd.DataFrame(data=data, columns=headers)
            df['current'] = df['current'].str.replace(',', '').astype(float).astype(int)
            df["date"] = datetime.now().strftime("%Y-%m-%d")
            gs_save(df)
            # df.to_csv(CSV_PATH, index=False)
            if df is not None:
                print("スクレイピング完了")

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None

        finally:
            browser.close()

if __name__ == "__main__":
    df = scrape_data_playwright()
