from playwright.sync_api import sync_playwright
import pandas as pd
from datetime import datetime
from google.cloud import storage, bigquery
import os

PROJECT_ID = os.environ["PROJECT_ID"]

def csv_to_bq():
    uri = f"gs://{PROJECT_ID}-trade/info.csv"

    table_id = f"{PROJECT_ID}.trade.kabucopy"

    client = bigquery.Client()

    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # またはスキーマを手動で指定
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # 追記を指定
    )

    job = client.load_table_from_uri(uri, table_id, job_config=job_config)

    job.result()

    print(f"Appended csv rows to {table_id}")


def gs_save(df):
    file_path = "info.csv"
    bucket_name = f"{PROJECT_ID}-trade"
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        bucket.create()
    blob = bucket.blob(file_path)
    blob.upload_from_string(df, "text/csv")
    del df
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
            # data = []
            for c in range(10):
                # ページネーションの要素をクリック
                pagination_links = page.locator('#KM_TABLEINDEX0 .KM_TABLEINDEX_FIGURE')
                awaiting_navigation = page.wait_for_load_state() # ナビゲーション完了を待つ
                pagination_links.nth(c).click()
                del pagination_links
                awaiting_navigation
                del awaiting_navigation
                # テーブルの行を取得
                records = page.locator('#KM_TABLECONTENT0 tr').all()
                data = []
                for record in records:
                    td_elements = record.locator('td').all()
                    del record

                    tds = [td.text_content() for td in td_elements]
                    print(tds)
                    if tds:
                        data.append(tds)
                        del tds

                del records

                df = pd.DataFrame(data=data, columns=headers)
                del data
                df['current'] = df['current'].str.replace(',', '').astype(float).astype(int)
                df["date"] = datetime.now().strftime("%Y-%m-%d")
                yield df.to_csv(index=False)
            # df.to_csv(CSV_PATH, index=False)
            print("スクレイピング完了")

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None

        finally:
            browser.close()

if __name__ == "__main__":
    csv_to_bq()
    # for x in scrape_data_playwright():
    #     gs_save(x)
    #     del x
