CREATE TABLE USERS (
    tg_id BIGINT NOT NULL,
    name VARCHAR(255) NOT NULL,
    sts_chat VARCHAR(255) DEFAULT 'IDLE',
    sts_acnt INT DEFAULT 0,
    PRIMARY KEY (tg_id)
);


