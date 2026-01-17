-- Test to ensure view counts are non-negative
select 
    message_id,
    channel_name,
    views
from {{ ref('stg_telegram_messages') }}
where views < 0
