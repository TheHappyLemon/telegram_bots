
CREATE TABLE FEEDBACK (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    data VARCHAR(4096) NOT NULL,
    user_id BIGINT NOT NULL,
    whn DATETIME NOT NULL,
    sts INT NOT NULL DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES USERS (tg_id)
);

-- sts
-- 0 - new
-- 9 - deleted
-- 1 - seen
-- 2 - woorking on
-- 3 - rejected
-- 4 - done

