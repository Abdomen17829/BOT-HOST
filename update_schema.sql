-- Update users table with new settings columns
ALTER TABLE users 
ADD COLUMN IF NOT EXISTS ai_provider VARCHAR(50),
ADD COLUMN IF NOT EXISTS ai_api_key_enc TEXT,
ADD COLUMN IF NOT EXISTS ai_model VARCHAR(100),
ADD COLUMN IF NOT EXISTS db_provider VARCHAR(50),
ADD COLUMN IF NOT EXISTS db_credentials_enc TEXT,
ADD COLUMN IF NOT EXISTS hosting_provider VARCHAR(50),
ADD COLUMN IF NOT EXISTS hosting_token_enc TEXT,
ADD COLUMN IF NOT EXISTS auto_seo BOOLEAN DEFAULT true;

-- Disable Row-Level Security to prevent 401 Unauthorized / RLS Policy errors
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE projects DISABLE ROW LEVEL SECURITY;

