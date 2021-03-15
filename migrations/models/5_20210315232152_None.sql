-- upgrade --
CREATE TABLE IF NOT EXISTS "user" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "domain" VARCHAR(511) NOT NULL,
    "hashed_password" VARCHAR(511),
    "created" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP /* Created datetime */,
    CONSTRAINT "uid_user_email_f91910" UNIQUE ("email", "domain")
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
