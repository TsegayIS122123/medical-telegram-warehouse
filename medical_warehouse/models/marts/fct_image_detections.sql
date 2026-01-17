-- models/marts/fct_image_detections.sql
{{ config(materialized='table', schema='public_marts') }}

WITH image_detections AS (
    SELECT
        y.message_id,
        c.channel_key,
        d.date_key,
        y.detected_class,
        y.confidence_score,
        y.image_category,
        y.detection_count,
        y.detected_at
    FROM raw.yolo_detections y
    LEFT JOIN {{ ref('dim_channels') }} c 
        ON y.channel_name = c.channel_name
    LEFT JOIN {{ ref('fct_messages') }} f 
        ON y.message_id = f.message_id
    LEFT JOIN {{ ref('dim_dates') }} d 
        ON f.date_key = d.date_key
    WHERE y.image_category IS NOT NULL
)

SELECT * FROM image_detections