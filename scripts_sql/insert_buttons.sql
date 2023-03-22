-- 0 level buttons
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (1, 'Idea'         , 'main_1', 0, 1, 'Choose an option:', NULL, NULL);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (2, 'Help'         , 'main_2', 0, 0, 'Choose an option:', 'SELECT DATA FROM HELP', NULL);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (3, 'Lookup Tables', 'main_3', 0, 1, 'Choose an option:', NULL, NULL);
-- Modify button buttons                                              command,
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (4, 'Create Idea'  , 'idea_1', 1, 0, 'Idea options:', NULL, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (5, 'Modify Idea'  , 'idea_2', 1, 0, 'Idea options:', NULL, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (6, 'Delete Idea'  , 'idea_3', 1, 0, 'Idea options:', NULL, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (7, 'Acces to Idea', 'idea_4', 1, 0, 'Idea options:', NULL, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (8, 'Back'         , 'back_1', 1, 0, 'Idea options:', NULL, 1);
-- LookUp button buttons                                              command,
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (9,  'Users'   , 'look_1', 2, 0, 'Lookup options:', 'SELECT * FROM USERS'  , 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (10, 'Ideas'   , 'look_2', 2, 0, 'Lookup options:', 'SELECT * FROM IDEAS'  , 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (11, 'Friends' , 'look_3', 2, 0, 'Lookup options:', 'SELECT * FROM FRIENDS', 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (12, 'Helps'   , 'look_4', 2, 0, 'Lookup options:', 'SELECT * FROM HELP'  , 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (13, 'Images'  , 'look_5', 2, 0, 'Lookup options:', 'SELECT * FROM IMAGES' , 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (14, 'Buttons' , 'look_6', 2, 0, 'Lookup options:', 'SELECT * FROM BUTTONS', 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, label, command, parentId) VALUES (15, 'Back'    , 'back_2', 2, 0, 'Lookup options:', NULL, 3);
