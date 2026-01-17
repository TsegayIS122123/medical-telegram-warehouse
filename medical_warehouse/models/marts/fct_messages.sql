{{ config(materialized='table') }}

with messages as (
    select
        message_id,
        channel_name,
        message_date::date as message_date,
        message_text,
        views as view_count,
        forwards as forward_count,
        has_media,
        image_path
    from {{ ref('stg_telegram_messages') }}
)

select
    m.message_id,
    dc.channel_key,
    to_char(m.message_date, 'YYYYMMDD')::integer as date_key,
    m.message_text,
    length(m.message_text) as message_length,
    m.view_count,
    m.forward_count,
    case when m.image_path is not null then true else false end as has_image
from messages m
left join {{ ref('dim_channels') }} dc on m.channel_name = dc.channel_name
