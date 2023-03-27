CREATE TABLE IDEAS (
    ID INT NOT NULL AUTO_INCREMENT,
    user_id INT NOT NULL,
    isPublic BOOL NOT NULL DEFAULT 0,
    name VARCHAR(255) NOT NULL,
    descr VARCHAR(4096),
    price DOUBLE,
    origin VARCHAR(255),
    sts INT DEFAULT 0,
    PRIMARY KEY (ID),
    FOREIGN KEY (user_id) REFERENCES USERS(ID),
    INDEX ind_price (price)
);
