from playwright.sync_api import sync_playwright
from google.cloud import storage, bigquery
from datetime import datetime
import pandas as pd
import numpy as np
import os

PROJECT_ID = os.environ["PROJECT_ID"]
bq = bigquery.Client()
gs = storage.Client()

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
def csv_to_bq() -> None:
    uri = f"gs://{PROJECT_ID}-trade/info.csv"

    table_id = f"{PROJECT_ID}.trade.kabumap"


    job_config = bigquery.LoadJobConfig(
        autodetect=True,  # またはスキーマを手動で指定
        source_format=bigquery.SourceFormat.CSV,
        write_disposition=bigquery.WriteDisposition.WRITE_APPEND,  # 追記を指定
    )

    job = bq.load_table_from_uri(uri, table_id, job_config=job_config)

    job.result()

    print(f"Appended csv rows to {table_id}")

    return None


def gs_save(df: str) -> None:
    bucket = gs.bucket(f"{PROJECT_ID}-trade")
    if not bucket.exists():
        bucket.create()
    blob = bucket.blob("info.csv")
    blob.upload_from_string(df, "text/csv")
    del df
    print(f"DataFrameをGCSに保存しました: gs://{PROJECT_ID}-trade/info.csv")
    csv_to_bq()
    return None

def records_csv(df: object) -> str:
    df['current'] = df['current'].str.replace(',', '').astype(float).astype(int)
    df["date"] = datetime.now().strftime("%Y-%m-%d")
    df = df.replace('NA', np.nan).fillna(0.0)
    return df.to_csv(index=False)

def scrape_data_playwright():
    with sync_playwright() as p:
        browser = p.chromium.launch()  # または p.firefox.launch(), p.webkit.launch()
        page = browser.new_page()

        try:
            page.goto(
                "https://jp.kabumap.com/servlets/kabumap/Action?SRC=stockRanking/base&ind=unit&exch=T1&d=d"
            )
            for c in range(10):
                # ページネーションの要素をクリック
                pagination_links = page.locator('#KM_TABLEINDEX0 .KM_TABLEINDEX_FIGURE')
                page.wait_for_load_state() # ナビゲーション完了を待つ
                pagination_links.nth(c).click()
                del pagination_links
                page.wait_for_load_state()
                # テーブルの行を取得
                records = page.locator('#KM_TABLECONTENT0 tr').all()
                print(type(records))
                for record in records:
                    yield [td.text_content() for td in record.locator("td").all()]
                    del record
                del records
            print("スクレイピング完了")

        except Exception as e:
            print(f"エラーが発生しました: {e}")
            return None

        finally:
            browser.close()

def main():
    gs_save(
        records_df(
            pd.DataFrame(
                [x for x in scrape_data_playwright() if x],
                columns=headers
            )
        )
    )

if __name__ == "__main__":
    main()
