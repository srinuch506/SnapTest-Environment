-- Update database to add mobile column
USE codegnantest;

-- Add mobile column to test table if it doesn't exist
ALTER TABLE test ADD COLUMN mobile VARCHAR(15) DEFAULT NULL AFTER batch;

-- Update existing records to have empty mobile field
UPDATE test SET mobile = '' WHERE mobile IS NULL;

-- Show the updated table structure
DESCRIBE test; 