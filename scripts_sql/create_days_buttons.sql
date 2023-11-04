CREATE TABLE DAYS_buttons (
    id INT NOT NULL PRIMARY KEY,
    text VARCHAR(32) NOT NULL,
    func VARCHAR(32),
    group_num INT NOT NULL,
    nextGroup INT,
    ordr INT NOT NULL DEFAULT 0,
    parent_id INT,
    accs_lvl INT NOT NULL,
    sts_user VARCHAR(32),
    showif VARCHAR(32)
);
