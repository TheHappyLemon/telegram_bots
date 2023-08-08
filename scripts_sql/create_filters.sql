-- sname - short name
-- fname - full name forr output
CREATE TABLE IDEA_FILTERS (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    sname VARCHAR(255) NOT NULL,
    fname VARCHAR(255) NOT NULL
);

INSERT INTO IDEA_FILTERS (sname, fname) VALUES('price'   , 'Price');
INSERT INTO IDEA_FILTERS (sname, fname) VALUES('name'    , 'Name');
INSERT INTO IDEA_FILTERS (sname, fname) VALUES('descr'   , 'Description');
INSERT INTO IDEA_FILTERS (sname, fname) VALUES('origin'  , 'Origin');
INSERT INTO IDEA_FILTERS (sname, fname) VALUES('isPublic', 'Acces');
