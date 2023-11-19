-- migrate:up
CREATE TABLE "lesson_file"
(
   id integer generated always as identity primary key,
   name varchar(255) not null,
   file varchar,
   description varchar(255) not null,
   lesson_id integer not null,

   CONSTRAINT fk_lesson FOREIGN KEY(lesson_id) REFERENCES "lesson"(id) ON DELETE CASCADE
);


-- migrate:down
DROP TABLE "lesson_file"