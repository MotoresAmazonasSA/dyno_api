CREATE PROCEDURE scadalts.dyno_test(IN input_test_id INT)
BEGIN
    SELECT
        FROM_UNIXTIME(final.ts/1000) AS timestmp,
        final.meta_ntc1,
        final.meta_ntc3,
        final.meta_ntc5,
        final.meta_peso_1,
        final.meta_corriente_1,
        final.meta_corriente_2,
        final.meta_ntc2,
        final.meta_ntc6,
        final.meta_lv25p_1,
        final.meta_lv25p_2,
        final.meta_encoder,
        final.meta_ntc4,
        final.meta_peso_2
    FROM (
        SELECT
            pv.ts,
            MAX(CASE WHEN dp.pointName = 'Meta NTC1' THEN pv.pointValue END) AS meta_ntc1,
            MAX(CASE WHEN dp.pointName = 'Meta NTC3' THEN pv.pointValue END) AS meta_ntc3,
            MAX(CASE WHEN dp.pointName = 'Meta NTC5' THEN pv.pointValue END) AS meta_ntc5,
            MAX(CASE WHEN dp.pointName = 'Meta Peso_1' THEN pv.pointValue END) AS meta_peso_1,
            MAX(CASE WHEN dp.pointName = 'Meta Corriente_1' THEN pv.pointValue END) AS meta_corriente_1,
            MAX(CASE WHEN dp.pointName = 'Meta Corriente_2' THEN pv.pointValue END) AS meta_corriente_2,
            MAX(CASE WHEN dp.pointName = 'Meta NTC2' THEN pv.pointValue END) AS meta_ntc2,
            MAX(CASE WHEN dp.pointName = 'Meta NTC6' THEN pv.pointValue END) AS meta_ntc6,
            MAX(CASE WHEN dp.pointName = 'Meta LV25P_1' THEN pv.pointValue END) AS meta_lv25p_1,
            MAX(CASE WHEN dp.pointName = 'Meta LV25P_2' THEN pv.pointValue END) AS meta_lv25p_2,
            MAX(CASE WHEN dp.pointName = 'Meta Encoder' THEN pv.pointValue END) AS meta_encoder,
            MAX(CASE WHEN dp.pointName = 'Meta NTC4' THEN pv.pointValue END) AS meta_ntc4,
            MAX(CASE WHEN dp.pointName = 'Meta Peso_2' THEN pv.pointValue END) AS meta_peso_2
        FROM scadalts.pointValues pv
        JOIN scadalts.test_info tlt
            ON pv.ts BETWEEN tlt.begin_of_test AND tlt.end_of_test
            AND tlt.test_id = input_test_id
        JOIN scadalts.dataPoints dp
            ON pv.dataPointId = dp.id
            AND LOWER(dp.pointName) LIKE '%meta%'
        GROUP BY pv.ts
    ) final;
END