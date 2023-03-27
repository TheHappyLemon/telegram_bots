-- 0 level buttons
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (1, 'Idea'         	   , 'main_1', 0, 1, NULL, 1, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (2, 'Lookup Tables'	   , 'main_2', 0, 1, NULL, 2, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (3, 'My account'   	   , 'main_3', 0, 1, NULL, 3, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (4, 'Help'         	   , 'main_4', 0, 0, NULL, 4, 4);
-- Modify button buttons                                       	                                                   
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (5 , 'List Ideas'  	   , 'idea_1', 1, 0, 1, 5 , 5);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (6 , 'Create Idea' 	   , 'idea_2', 1, 0, 1, 6 , 6);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (7 , 'Modify Idea' 	   , 'idea_3', 1, 1, 1, 7 , 7);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (8 , 'Delete Idea' 	   , 'idea_4', 1, 0, 1, 8 , 8);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (9 , 'Help'  		   , 'idea_5', 1, 0, 1, 9 , 9);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (10, 'Back'        	   , 'back_1', 1, 0, 1, 10, 10);
-- LookUp button buttons                                                        
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (11, 'Users'       	   , 'look_1', 2, 0, 2, 11, 11);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (12, 'Ideas'       	   , 'look_2', 2, 0, 2, 12, 12);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (13, 'Friends'     	   , 'look_3', 2, 0, 2, 13, 13);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (14, 'Helps'       	   , 'look_4', 2, 0, 2, 14, 14);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (15, 'Images'      	   , 'look_5', 2, 0, 2, 15, 15);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (16, 'Buttons'     	   , 'look_6', 2, 0, 2, 16, 16);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (17, 'Button_inf'  	   , 'look_7', 2, 0, 2, 17, 17);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (18, 'Help'  	       , 'idea_8', 2, 0, 2, 18, 18);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (19, 'Back'        	   , 'back_2', 2, 0, 2, 19, 19);
-- Account button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (20, 'Display Info'     , 'my_1'  , 3, 0, 3, 20, 20);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (21, 'Change Name'      , 'my_2'  , 3, 0, 3, 21, 21);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (22, 'Help' 		       , 'my_3'  , 3, 0, 3, 22, 22);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (23, 'Back' 		       , 'back_3', 3, 0, 3, 23, 23);
-- Modify button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (24, 'Change name'    	 , 'modify_1', 4, 0, 7, 24, 24);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (25, 'Change description' , 'modify_2', 4, 0, 7, 25, 25);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (26, 'Change price'   	 , 'modify_3', 4, 0, 7, 26, 26);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (27, 'Change origin'      , 'modify_4', 4, 0, 7, 27, 27);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (28, 'Change acces'   	 , 'modify_5', 4, 1, 7, 28, 28);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (29, 'Help' 		  	     , 'modify_6', 4, 0, 7, 29, 29);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (30, 'Back'   	   		 , 'back_4'  , 4, 0, 7, 30, 30);
-- Acces button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (31, 'Set privacy'        , 'acces_1', 5, 0, 28, 31, 31);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (32, 'Add friend'         , 'acces_2', 5, 0, 28, 32, 32);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (33, 'Remove friend'      , 'acces_3', 5, 0, 28, 33, 33);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (34, 'Help'               , 'acces_4', 5, 0, 28, 34, 34);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (35, 'Back'   	   	     , 'back_5' , 5, 0, 28, 35, 35);
