-- migrate:up
CREATE TABLE "user"
(
   id integer generated always as identity primary key,
   username varchar(255) not null,
   password varchar(255) not null,
   first_name varchar(255) not null,
   last_name varchar(255) not null,
   email varchar(255) not null,
   country varchar(255) not null,
   user_type varchar(255) not null,
   phone_number varchar(13) not null,
   created_at timestamp not null default CURRENT_TIMESTAMP

);

-- migrate:down
DROP TABLE "user"