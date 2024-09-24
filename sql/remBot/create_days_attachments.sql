CREATE TABLE DAYS_attachments (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    day_id INT,
    tg_file_id VARCHAR(256),
    tg_file_unique_id VARCHAR(256),
    system_path VARCHAR(256),
    real_name VARCHAR(256),
    UNIQUE (day_id, system_path),
    FOREIGN KEY (day_id) REFERENCES DAYS(id) ON DELETE SET NULL
);
