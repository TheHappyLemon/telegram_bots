CREATE TABLE CURRENCIES (
  descr VARCHAR(255) NOT NULL,
  code VARCHAR(3) NOT NULL,
  sign VARCHAR(10) NOT NULL,
  PRIMARY KEY (code, sign)
);
