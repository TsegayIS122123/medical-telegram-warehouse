-- scripts/create_db.sql
-- Create database for medical telegram warehouse
CREATE DATABASE medical_warehouse;

-- Connect to the new database
\c medical_warehouse;

-- Create raw schema as per instructions
CREATE SCHEMA raw;

-- Create the table
CREATE TABLE raw.telegram_messages (
    id SERIAL PRIMARY KEY,
    message_id INTEGER NOT NULL,
    channel_name VARCHAR(255) NOT NULL,
    message_date TIMESTAMP,
    message_text TEXT,
    has_media BOOLEAN DEFAULT FALSE,
    image_path TEXT,
    views INTEGER DEFAULT 0,
    forwards INTEGER DEFAULT 0,
    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create unique constraint
CREATE UNIQUE INDEX idx_unique_message 
ON raw.telegram_messages (message_id, channel_name);

-- Show what we created
SELECT '✅ Database medical_warehouse created successfully!' as status;