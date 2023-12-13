CREATE TABLE DAYS_notifications (
    id INT NOT NULL AUTO_INCREMENT,
    day_id INT NOT NULL,
    when_date VARCHAR(16) NOT NULL,
    when_time VARCHAR(7) NOT NULL,
    PRIMARY KEY (id),
    UNIQUE (day_id, when_date, when_time),
    FOREIGN KEY (day_id) REFERENCES DAYS(id)
);

-- for some reason when there is on cascade delete option in foreign key
-- on insert days trigger can not create this record

-- options:
-- 0 day
-- 1 day
-- 2 day
-- 3 day 
-- 1 week
-- 2 week
-- 1 month
