-- migrate:up
CREATE TABLE "lesson"
(
   id integer generated always as identity primary key,
   name varchar(255) not null,
   content TEXT not null,
   description varchar(255) not null,
   course_id integer not null,

   CONSTRAINT fk_course FOREIGN KEY(course_id) REFERENCES "course"(id) ON DELETE CASCADE
);


-- migrate:down
DROP TABLE "lesson"