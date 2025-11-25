-- Migration: OAuth-Spalten zur users-Tabelle hinzufügen
-- Dieses Script muss auf der Render-Datenbank ausgeführt werden

-- Prüfen und hinzufügen von oauth_provider
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'users' AND column_name = 'oauth_provider') THEN
        ALTER TABLE users ADD COLUMN oauth_provider VARCHAR(50);
        RAISE NOTICE 'Spalte oauth_provider hinzugefügt';
    ELSE
        RAISE NOTICE 'Spalte oauth_provider existiert bereits';
    END IF;
END $$;

-- Prüfen und hinzufügen von oauth_id
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                   WHERE table_name = 'users' AND column_name = 'oauth_id') THEN
        ALTER TABLE users ADD COLUMN oauth_id VARCHAR(200);
        RAISE NOTICE 'Spalte oauth_id hinzugefügt';
    ELSE
        RAISE NOTICE 'Spalte oauth_id existiert bereits';
    END IF;
END $$;

-- Unique Constraint für OAuth hinzufügen (falls nicht vorhanden)
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'unique_oauth_user') THEN
        ALTER TABLE users ADD CONSTRAINT unique_oauth_user UNIQUE (oauth_provider, oauth_id);
        RAISE NOTICE 'Constraint unique_oauth_user hinzugefügt';
    ELSE
        RAISE NOTICE 'Constraint unique_oauth_user existiert bereits';
    END IF;
EXCEPTION WHEN OTHERS THEN
    RAISE NOTICE 'Constraint konnte nicht hinzugefügt werden (möglicherweise bereits vorhanden)';
END $$;

-- Überprüfen der Struktur
SELECT column_name, data_type, character_maximum_length 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;
