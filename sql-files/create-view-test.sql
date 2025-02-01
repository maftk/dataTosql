#standardSQL
CREATE OR REPLACE VIEW trade.codes_everyday
AS
WITH
  count_days_ever AS (
    SELECT COUNT(DISTINCT date) days FROM trade.kabumap
  ),
  days_summary_ever AS (
    SELECT stock_code FROM trade.kabumap
    GROUP BY
      stock_code
    HAVING
      COUNT(date) = (SELECT days FROM count_days_ever)
  ),
  unique_codes_table AS (
    SELECT COUNT(DISTINCT stock_code) unique_codes FROM trade.kabumap
  )
SELECT
  CURRENT_DATE(),
  (SELECT unique_codes FROM unique_codes_table) AS unique_codes,
  COUNT(dse.stock_code) AS codes_with_days
FROM
  days_summary_ever AS dse;
