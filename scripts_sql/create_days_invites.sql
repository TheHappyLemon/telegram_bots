CREATE TABLE DAYS_invites (
    id INT NOT NULL AUTO_INCREMENT,
    usr_from BIGINT,
    usr_to BIGINT,
    day_id INT,
    sts VARCHAR(16) DEFAULT 'new',
    type VARCHAR(16),
    PRIMARY KEY (id),
    UNIQUE (usr_from, usr_to, day_id, sts, type),
    FOREIGN KEY (usr_from) REFERENCES USERS(tg_id) ON DELETE CASCADE,
    FOREIGN KEY (usr_to) REFERENCES USERS(tg_id) ON DELETE CASCADE,
    FOREIGN KEY (day_id) REFERENCES DAYS(id) ON DELETE CASCADE
);
