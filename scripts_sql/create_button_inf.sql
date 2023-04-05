CREATE TABLE BUTTON_INF (
    ID INT NOT NULL AUTO_INCREMENT,
    btn_id INT NOT NULL,
    label VARCHAR(255),
    command VARCHAR(512),
    status_inp VARCHAR(255),
    status_out VARCHAR(255),
    onlyData TINYINT,
    PRIMARY KEY (ID),
    FOREIGN KEY (btn_id) REFERENCES BUTTONS(ID)
);

-- label to print above buttons. Always is
-- command, what command should do. Select - execute, other - print it and set user status to status
-- onlyData for SELECT commands. if yes -> dont print column names
-- status_inp - when bot receives message, check this status and handle input
-- status_out - when bot receives query from DB he check what params should he replace from this field
