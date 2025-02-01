#standardSQL
CREATE OR REPLACE TABLE trade.codes_everyday (
  execution_date DATE,
  unique_codes INT64,
  codes_with_days INT64
)

