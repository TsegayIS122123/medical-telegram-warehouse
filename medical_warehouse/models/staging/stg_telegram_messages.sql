{{ config(materialized='view') }}

with source_data as (
    select
        message_id,
        channel_name,
        message_date::timestamp as message_date,
        message_text,
        views,
        forwards,
        has_media,
        image_path
    from raw.telegram_messages
)

select *
from source_data
