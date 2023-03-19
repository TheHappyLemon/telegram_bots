CREATE TABLE USERS (
    ID INT NOT NULL AUTO_INCREMENT,
    tg_id INT NOT NULL,
    name VARCHAR(255),
    sts INT DEFAULT 0,
    PRIMARY KEY (ID),
    INDEX tg_id_index (tg_id)
);


