CREATE OR REPLACE VIEW `latest_test` AS
WITH general_numbers AS (
	SELECT 0 AS n
	UNION all
	SELECT 1 AS n
	UNION all
	SELECT 2 AS n
	UNION all
	SELECT 3 AS n
	UNION all
	SELECT 4 AS n
	UNION all
	SELECT 5 AS n
	UNION all
	SELECT 6 AS n
	UNION all
	SELECT 7 AS n
	UNION all
	SELECT 8 AS n
	UNION all
	SELECT 9 AS n
)
SELECT
	((gn3.n * 100) + (gn2.n * 10) + gn1.n) + 1 AS numeric_series,
	RAND() * 10 AS meta_corriente_1,
	(RAND()*200)+200 AS meta_lv25p_1,
	RAND() * 50 AS meta_peso_2,
	(RAND() * 2500) + 500 AS meta_encoder
FROM general_numbers gn1
CROSS JOIN general_numbers gn2
CROSS JOIN general_numbers gn3
ORDER BY 1;