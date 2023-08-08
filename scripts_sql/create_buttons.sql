CREATE TABLE BUTTONS (
    ID INT NOT NULL,
    DATA VARCHAR(255) NOT NULL,
    btn_name VARCHAR(255) NOT NULL,
    keyboardId INT NOT NULL,
    isParent TINYINT NOT NULL,
    parentId INT,
    btn_inf  INT,
    ordr INT,
    accs_lvl INT,
    PRIMARY KEY (ID, btn_name),
    FOREIGN KEY (parentId) REFERENCES BUTTONS(ID)
);

-- isParent -> yes -> label
-- isParent -> no  -> command
