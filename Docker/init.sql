DO
$do$
BEGIN
   IF NOT EXISTS (
      SELECT FROM pg_database WHERE datname = 'regdbot'
   ) THEN
      CREATE DATABASE regdbot;
   END IF;
END
$do$;
GRANT ALL PRIVILEGES ON DATABASE regdbot TO postgres;