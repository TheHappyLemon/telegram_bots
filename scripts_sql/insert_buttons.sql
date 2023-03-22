-- 0 level buttons
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (1, 'Idea'         , 'main_1', 0, 1, NULL);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (2, 'Help'         , 'main_2', 0, 0, NULL);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (3, 'Lookup Tables', 'main_3', 0, 1, NULL);
-- Modify button buttons
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (4, 'Create Idea'  , 'idea_1', 1, 0, 1);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (5, 'Modify Idea'  , 'idea_2', 1, 0, 1);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (6, 'Delete Idea'  , 'idea_3', 1, 0, 1);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (7, 'Acces to Idea', 'idea_4', 1, 0, 1);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (8, 'Back'         , 'back_1', 1, 0, 1);
-- LookUp button buttons
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (9,  'Users'   , 'look_1', 2, 0, 3);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (10, 'Ideas'   , 'look_2', 2, 0, 3);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (11, 'Friends' , 'look_3', 2, 0, 3);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (12, 'Helps'   , 'look_4', 2, 0, 3);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (13, 'Images'  , 'look_5', 2, 0, 3);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (14, 'Buttons' , 'look_6', 2, 0, 3);
INSERT INTO Buttons (ID, DATA, btn_name, keyboardId, isParent, parentId) VALUES (15, 'Back'    , 'back_2', 2, 0, 3);
