CREATE TABLE FILMS (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(128) NOT NULL,
    category VARCHAR(128),
    length VARCHAR(128),
    link VARCHAR(255),
    user_notes VARCHAR(4096),
    PRIMARY KEY (id)
);
