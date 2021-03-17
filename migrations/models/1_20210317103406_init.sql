-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL,
    "domain" VARCHAR(511) NOT NULL,
    "hashed_password" VARCHAR(511),
    "created" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "uid_user_email_f91910" UNIQUE ("email", "domain")
);
COMMENT ON COLUMN "user"."created" IS 'Created datetime';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSONB NOT NULL
);
