CREATE TABLE HELP (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    data VARCHAR(2048) NOT NULL,
    keyboardId INT,
    btn_id INT,
    FOREIGN KEY(btn_id) REFERENCES BUTTONS(ID)
);
