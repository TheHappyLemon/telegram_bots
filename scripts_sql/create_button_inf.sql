CREATE TABLE BUTTON_INF (
    ID INT NOT NULL AUTO_INCREMENT,
    btn_id INT NOT NULL,
    label VARCHAR(255),
    command VARCHAR(255),
    status  VARCHAR(255),
    onlyData TINYINT,
    PRIMARY KEY (ID),
    FOREIGN KEY (btn_id) REFERENCES BUTTONS(ID)
);

-- label to print above buttons. Always is
-- command, what command should do. Select - execute, other - print it and set user status to status
-- onlyData for SELECT commands. if yes -> dont print column names
