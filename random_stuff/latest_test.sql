-- scadalts.latest_test source

CREATE OR REPLACE VIEW `latest_test` AS 
WITH `point_values` AS (
    SELECT
        `pv`.`ts` AS `ts`,
        `pv`.`pointValue` AS `pointValue`,
        `dp`.`pointName` AS `pointName`
    FROM
        (`pointValues` `pv`
    JOIN `dataPoints` `dp` ON
        (((`pv`.`dataPointId` = `dp`.`id`)
            AND (lower(`dp`.`pointName`) LIKE '%meta%'))))
    ORDER BY
        `pv`.`ts`,
        `pv`.`id`
),
`final` AS (
    SELECT
        `point_values`.`ts` AS `ts`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta NTC1') THEN `point_values`.`pointValue` END)) AS `meta_ntc1`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta NTC3') THEN `point_values`.`pointValue` END)) AS `meta_ntc3`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta NTC5') THEN `point_values`.`pointValue` END)) AS `meta_ntc5`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta Peso_1') THEN `point_values`.`pointValue` END)) AS `meta_peso_1`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta Corriente_1') THEN `point_values`.`pointValue` END)) AS `meta_corriente_1`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta Corriente_2') THEN `point_values`.`pointValue` END)) AS `meta_corriente_2`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta NTC2') THEN `point_values`.`pointValue` END)) AS `meta_ntc2`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta NTC6') THEN `point_values`.`pointValue` END)) AS `meta_ntc6`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta LV25P_1') THEN `point_values`.`pointValue` END)) AS `meta_lv25p_1`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta LV25P_2') THEN `point_values`.`pointValue` END)) AS `meta_lv25p_2`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta Encoder') THEN `point_values`.`pointValue` END)) AS `meta_encoder`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta NTC4') THEN `point_values`.`pointValue` END)) AS `meta_ntc4`,
        max((CASE WHEN (`point_values`.`pointName` = 'Meta Peso_2') THEN `point_values`.`pointValue` END)) AS `meta_peso_2`
    FROM
        `point_values`
    GROUP BY
        `point_values`.`ts`
)
SELECT
    from_unixtime((`final`.`ts` / 1000)) AS `timestmp`,
    `final`.`meta_ntc1` AS `meta_ntc1`,
    `final`.`meta_ntc3` AS `meta_ntc3`,
    `final`.`meta_ntc5` AS `meta_ntc5`,
    `final`.`meta_peso_1` AS `meta_peso_1`,
    `final`.`meta_corriente_1` AS `meta_corriente_1`,
    `final`.`meta_corriente_2` AS `meta_corriente_2`,
    `final`.`meta_ntc2` AS `meta_ntc2`,
    `final`.`meta_ntc6` AS `meta_ntc6`,
    `final`.`meta_lv25p_1` AS `meta_lv25p_1`,
    `final`.`meta_lv25p_2` AS `meta_lv25p_2`,
    `final`.`meta_encoder` AS `meta_encoder`,
    `final`.`meta_ntc4` AS `meta_ntc4`,
    `final`.`meta_peso_2` AS `meta_peso_2`
FROM
    `final`;