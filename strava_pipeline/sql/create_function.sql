CREATE
OR REPLACE FUNCTION get_summary (start_date_bound DATE, end_date_bound DATE) RETURNS TABLE (
    activity_type TEXT,
    count BIGINT,
    distance NUMERIC,
    moving_time TEXT
) LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    WITH RoundedDistances AS (
        SELECT
            CASE
                WHEN a.sport_type = 'Ride' THEN 'Outdoor'
                WHEN a.sport_type = 'VirtualRide' THEN 'Indoor'
                ELSE 'Other'
            END AS activity_type,
            COUNT(*)::BIGINT AS count,
            ROUND(SUM(a.distance)::NUMERIC, 2) AS distance,
            SUM(a.moving_time) AS total_moving_time
        FROM activities a
        WHERE a.start_date >= start_date_bound
          AND a.start_date <= end_date_bound
        GROUP BY a.sport_type
    )

    SELECT
        rd.activity_type,
        rd.count,
        rd.distance,
        TO_CHAR(
            INTERVAL '1 second' * rd.total_moving_time,
            'HH24:MI:SS'
        ) AS moving_time
    FROM RoundedDistances rd

    UNION ALL

    SELECT
        'Total' AS activity_type,
        SUM(rd.count)::BIGINT AS count,
        ROUND(SUM(rd.distance)::NUMERIC, 2) AS distance,
        TO_CHAR(
            INTERVAL '1 second' * SUM(rd.total_moving_time),
            'HH24:MI:SS'
        ) AS moving_time
    FROM RoundedDistances rd

    ORDER BY activity_type;
END;
$$;