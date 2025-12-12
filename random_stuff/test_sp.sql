CREATE PROCEDURE dyno_test(IN input_test_id INT)
BEGIN
    WITH ts_selected_test AS (
        SELECT begin_of_test, end_of_test
        FROM scadalts.test_info
        WHERE test_id = input_test_id
    ), point_values AS (
    SELECT
        pv.ts,
        pv.pointValue,
        dp.pointName
    FROM scadalts.pointValues pv
    JOIN ts_selected_test tlt
        ON pv.ts BETWEEN tlt.begin_of_test and tlt.end_of_test
    JOIN scadalts.dataPoints dp
        ON pv.dataPointId = dp.id
        AND LOWER(dp.pointName) LIKE '%meta%'
    ), final AS (
    SELECT
        ts,
        MAX(CASE
            WHEN pointName = 'Meta NTC1' THEN pointValue
        END) AS meta_ntc1,
        MAX(CASE
            WHEN pointName = 'Meta NTC3' THEN pointValue
        END) AS meta_ntc3,
        MAX(CASE
            WHEN pointName = 'Meta NTC5' THEN pointValue
        END) AS meta_ntc5,
        MAX(CASE
            WHEN pointName = 'Meta Peso_1' THEN pointValue
        END) AS meta_peso_1,
        MAX(CASE
            WHEN pointName = 'Meta Corriente_1' THEN pointValue
        END) AS meta_corriente_1,
        MAX(CASE
            WHEN pointName = 'Meta Corriente_2' THEN pointValue
        END) AS meta_corriente_2,
        MAX(CASE
            WHEN pointName = 'Meta NTC2' THEN pointValue
        END) AS meta_ntc2,
        MAX(CASE
            WHEN pointName = 'Meta NTC6' THEN pointValue
        END) AS meta_ntc6,
        MAX(CASE
            WHEN pointName = 'Meta LV25P_1' THEN pointValue
        END) AS meta_lv25p_1,
        MAX(CASE
            WHEN pointName = 'Meta LV25P_2' THEN pointValue
        END) AS meta_lv25p_2,
        MAX(CASE
            WHEN pointName = 'Meta Encoder' THEN pointValue
        END) AS meta_encoder,
        MAX(CASE
            WHEN pointName = 'Meta NTC4' THEN pointValue
        END) AS meta_ntc4,
        MAX(CASE
            WHEN pointName = 'Meta Peso_2' THEN pointValue
        END) AS meta_peso_2
    FROM point_values
    GROUP BY ts
    )
    SELECT
        FROM_UNIXTIME(ts/1000) AS timestmp,
        meta_ntc1,
        meta_ntc3,
        meta_ntc5,
        meta_peso_1,
        meta_corriente_1,
        meta_corriente_2,
        meta_ntc2,
        meta_ntc6,
        meta_lv25p_1,
        meta_lv25p_2,
        meta_encoder,
        meta_ntc4,
        meta_peso_2
    FROM final
END;