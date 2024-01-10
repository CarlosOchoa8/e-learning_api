-- migrate:up
CREATE TABLE "user_course"
(
    id integer generated always as identity primary key,
    user_id integer not null,
    course_id integer not null,
    started_at timestamp not null default CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES "user"(id) ON DELETE CASCADE,
    CONSTRAINT fk_course_id FOREIGN KEY (course_id) REFERENCES "course"(id) ON DELETE CASCADE

);
-- migrate:down
DROP TABLE "user_course"