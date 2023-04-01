CREATE TABLE IDEAS (
    ID INT NOT NULL AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    isPublic BOOL NOT NULL DEFAULT 1,
    name VARCHAR(255) NOT NULL,
    descr VARCHAR(4096),
    price DOUBLE,
    origin VARCHAR(255),
    sts INT DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (user_id) REFERENCES USERS(tg_id),
    INDEX ind_price (price)
);
