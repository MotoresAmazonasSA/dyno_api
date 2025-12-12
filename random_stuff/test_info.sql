CREATE OR REPLACE VIEW test_info AS
WITH test_numbering AS (
SELECT
	pv.ts,
	pv.pointValue,
	ROW_NUMBER() over(PARTITION BY pv.pointValue ORDER BY pv.ts desc) AS test_id
FROM scadalts.pointValues pv
JOIN scadalts.dataPoints dp
	ON pv.dataPointId = dp.id
	AND dp.pointName = 'is_test_running'
), test_final AS (
SELECT
	test_id,
	MAX(CASE
			WHEN pointValue = 0 THEN ts
	END
	) AS end_of_test,
	MAX(CASE
			WHEN pointValue = 1 THEN ts
	END
	) AS begin_of_test	
FROM test_numbering
GROUP BY test_id
)
SELECT 
	row_number() over(ORDER BY test_id desc) AS test_id,
	end_of_test,
	begin_of_test
FROM test_final
WHERE begin_of_test IS NOT NULL;