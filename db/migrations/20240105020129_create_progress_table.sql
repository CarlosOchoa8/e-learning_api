-- migrate:up
CREATE TABLE "progress"
(
   id integer generated always as identity primary key,
   user_id integer not null,
   lesson_id integer not null,
   lesson_completed boolean not null,

    CONSTRAINT fk_lesson_id FOREIGN KEY(lesson_id) REFERENCES "lesson"(id) ON DELETE CASCADE,
    CONSTRAINT fk_user_id FOREIGN KEY(user_id) REFERENCES "user"(id) ON DELETE CASCADE
);

-- migrate:down
DROP TABLE "progress"

