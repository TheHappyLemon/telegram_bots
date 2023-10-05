CREATE TABLE DAYS_messages (
    chat_id BIGINT NOT NULL,
    msg_id INT NOT NULL,
    PRIMARY KEY (chat_id, msg_id),
    FOREIGN KEY (chat_id) REFERENCES USERS (tg_id) ON DELETE CASCADE
);
