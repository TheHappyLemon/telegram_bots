CREATE TABLE Buttons (
    ID INT NOT NULL,
    DATA VARCHAR(255) NOT NULL,
    btn_name VARCHAR(255) NOT NULL,
    keyboardId INT NOT NULL,
    isParent TINYINT NOT NULL,
    parentId INT,
    PRIMARY KEY (ID, DATA),
    FOREIGN KEY (parentId) REFERENCES Buttons(ID)
);
