-- 0 level buttons
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (1,  'Idea'         	   , 'main_1', 0, 1, NULL, 1, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (2,  'Administrator'	   , 'main_2', 0, 1, NULL, 2, 5);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (3,  'Settings'   	   , 'main_3', 0, 1, NULL, 3, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (4,  'Help'         	   , 'main_4', 0, 0, NULL, 4, 4);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (37, 'Friends'     	   , 'main_5', 0, 1, NULL, 37, 3);
-- Modify button buttons                                       	                                                   
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (5 , 'List Ideas'  	   , 'idea_1', 1, 0, 1, 5 , 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (6 , 'Create Idea' 	   , 'idea_2', 1, 0, 1, 6 , 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (7 , 'Modify Idea' 	   , 'idea_3', 1, 1, 1, 7 , 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (8 , 'Delete Idea' 	   , 'idea_4', 1, 0, 1, 8 , 4);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (9 , 'Help'  		   , 'idea_5', 1, 0, 1, 9 , 5);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (10, 'Back'        	   , 'back_1', 1, 0, 1, 10, 6);
-- LookUp button buttons                                                        
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (11, 'Users'       	   , 'look_1', 2, 0, 2, 11, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (12, 'Ideas'       	   , 'look_2', 2, 0, 2, 12, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (13, 'Friends'     	   , 'look_3', 2, 0, 2, 13, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (14, 'Helps'       	   , 'look_4', 2, 0, 2, 14, 4);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (15, 'Images'      	   , 'look_5', 2, 0, 2, 15, 5);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (16, 'Buttons'     	   , 'look_6', 2, 0, 2, 16, 6);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (17, 'Button_inf'  	   , 'look_7', 2, 0, 2, 17, 7);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (18, 'HELP'  	       , 'idea_8', 2, 0, 2, 18, 8);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (49, 'Help'  	       , 'idea_9', 2, 0, 2, 49, 9);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (19, 'Back'        	   , 'back_2', 2, 0, 2, 19, 10);
-- Account button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (20, 'Display Info'     , 'my_1'  , 3, 0, 3, 20, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (21, 'Change Name'      , 'my_2'  , 3, 0, 3, 21, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (22, 'Help' 		       , 'my_3'  , 3, 0, 3, 22, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (23, 'Back' 		       , 'back_3', 3, 0, 3, 23, 4);
-- Modify button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (24, 'Change name'    	 , 'modify_1', 4, 0, 7, 24, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (25, 'Change description' , 'modify_2', 4, 0, 7, 25, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (26, 'Change price'   	 , 'modify_3', 4, 0, 7, 26, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (27, 'Change origin'      , 'modify_4', 4, 0, 7, 27, 4);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (28, 'Change acces'   	 , 'modify_5', 4, 1, 7, 28, 5);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (29, 'Help' 		  	     , 'modify_6', 4, 0, 7, 29, 6);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (30, 'Back'   	   		 , 'back_4'  , 4, 0, 7, 30, 7);
-- Acces button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (31, 'Set privacy'        , 'acces_1', 5, 0, 28, 31, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (32, 'Hide from'          , 'acces_2', 5, 0, 28, 32, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (36, 'Who can see'        , 'acces_4', 5, 0, 28, 36, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (33, 'Help'               , 'acces_3', 5, 0, 28, 33, 4);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (34, 'Back'   	         , 'back_5' , 5, 0, 28, 34, 5);
-- Friends button buttons                                                                 
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (38, 'Display friends'    , 'friends_1' , 6, 0, 37, 38, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (39, 'Add friend'   	     , 'friends_2' , 6, 0, 37, 39, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (40, 'Remove friend'      , 'friends_3' , 6, 0, 37, 40, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (41, 'Help'   	         , 'friends_4' , 6, 0, 37, 41, 5);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (42, 'Back'   	         , 'back_6'    , 6, 0, 37, 42, 6);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (43, 'My Requests'        , 'friends_5' , 6, 1, 37, 43, 4);
-- Request button buttons
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (44, 'Display requests'   , 'requests_1' , 7, 0, 43, 44, 1);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (45, 'Accept request'     , 'requests_2' , 7, 0, 43, 45, 2);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (46, 'Decline request'    , 'requests_3' , 7, 0, 43, 46, 3);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (47, 'Help'    			 , 'requests_4' , 7, 0, 43, 47, 4);
INSERT INTO BUTTONS (ID, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (48, 'Back'   	         , 'back_7'     , 7, 0, 43, 48, 5);
