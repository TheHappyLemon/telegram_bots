CREATE TABLE BUTTONS (
    ID INT NOT NULL,
    DATA VARCHAR(255) NOT NULL,
    btn_name VARCHAR(255) NOT NULL,
    keyboardId INT NOT NULL,
    isParent TINYINT NOT NULL,
    parentId INT,
    label VARCHAR(255),
    command VARCHAR(255),
    PRIMARY KEY (ID, DATA),
    FOREIGN KEY (parentId) REFERENCES BUTTONS(ID)
);

-- isParent -> yes -> label
-- isParent -> no  -> command
