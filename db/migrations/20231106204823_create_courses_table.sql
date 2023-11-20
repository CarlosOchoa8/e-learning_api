-- migrate:up
CREATE TABLE "course"
(
   id integer generated always as identity primary key,
   name varchar(255) not null,
   teacher varchar(255),
   description varchar(255) not null

);


-- migrate:down
DROP TABLE "course"