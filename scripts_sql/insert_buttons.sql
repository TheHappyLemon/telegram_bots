-- 0 level buttons
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (1,  0, 'My Ideas'     	   , 'main_1', 0, 1, NULL, 1, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (2,  0, 'Administrator'	   , 'main_2', 0, 1, NULL, 2, 6);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (3,  0, 'Settings'   	   , 'main_3', 0, 1, NULL, 3, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (4,  0, 'Help'         	   , 'main_4', 0, 0, NULL, 4, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (37, 0, 'Friends'     	   , 'main_5', 0, 1, NULL, 37, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (60, 0, 'User Ideas'   	   , 'main_6', 0, 1, NULL, 60, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (80, 9, 'Films', 'main_7', 0, 1, NULL, 80, 7);

-- Modify button buttons accs_lvl,                                       	                                  0,                  
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (5 , 0, 'List Ideas'  	   , 'idea_1', 1, 0, 1, 5 , 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (6 , 0, 'Create Idea' 	   , 'idea_2', 1, 0, 1, 6 , 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (7 , 0, 'Modify Idea' 	   , 'idea_3', 1, 1, 1, 7 , 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (9 , 0, 'Help'  		   , 'idea_5', 1, 0, 1, 9 , 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (10, 0, 'Back'        	   , 'back_1', 1, 0, 1, 10, 5);
-- LookUp button buttons accs_lvl,                                                                            0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (11, 10, 'Users'       	   , 'look_1' , 2, 0, 2, 11, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (12, 10, 'Ideas'       	   , 'look_2' , 2, 0, 2, 12, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (13, 10, 'Friends'     	   , 'look_3' , 2, 0, 2, 13, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (14, 10, 'Helps'       	   , 'look_4' , 2, 0, 2, 14, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (15, 10, 'Images'      	   , 'look_5' , 2, 0, 2, 15, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (16, 10, 'Buttons'     	   , 'look_6' , 2, 0, 2, 16, 6);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (17, 10, 'Button_inf'  	   , 'look_7' , 2, 0, 2, 17, 7);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (58, 10, 'Fr_requests'  	   , 'look_8' , 2, 0, 2, 58, 8);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (59, 10, 'Idea_inf'  	   	   , 'look_9' , 2, 0, 2, 59, 9);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (72, 10, 'Feedback'  	   	   , 'look_10', 2, 0, 2, 72, 10);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (73, 0,  'List my feedback'   , 'look_11', 2, 0, 2, 73, 11);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (71, 0,  'Leave feedback'     , 'look_12', 2, 0, 2, 71, 12);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (49, 0,  'Help'  	       	   , 'look_13', 2, 0, 2, 49, 13);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (19, 0,  'Back'        	   , 'back_2' , 2, 0, 2, 19, 14);
-- Account button button accs_lvl,s                                                                           0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (20, 0, 'Display Info'     , 'my_1'  , 3, 0, 3, 20, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (21, 0, 'Change Name'      , 'my_2'  , 3, 0, 3, 21, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (62, 0, 'Set output mode'  , 'my_5'  , 3, 0, 3, 62, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (63, 0, 'Set filter'       , 'my_6'  , 3, 0, 3, 63, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (67, 0, 'Set order'        , 'my_7'  , 3, 0, 3, 67, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (69, 0, 'Set currency'     , 'my_10'  , 3, 0, 3, 69, 6);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (66, 0, 'Show filters'     , 'my_4'  , 3, 0, 3, 66, 7);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (68, 0, 'Show orders'      , 'my_8'  , 3, 0, 3, 68, 8);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (70, 0, 'Show currencies'  , 'my_9'  , 3, 0, 3, 70, 9);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (22, 0, 'Help' 		       , 'my_3'  , 3, 0, 3, 22, 10);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (23, 0, 'Back' 		       , 'back_3', 3, 0, 3, 23, 11);
-- Modify button buttons accs_lvl,                                                                            0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (24, 0, 'Change name'    	 , 'modify_1' , 4, 0, 7, 24, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (25, 0, 'Change description' , 'modify_2', 4, 0, 7, 25, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (26, 0, 'Change price'   	 , 'modify_3' , 4, 0, 7, 26, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (27, 0, 'Change source'      , 'modify_4', 4, 0, 7, 27, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (28, 0, 'Change access'   	 , 'modify_5' , 4, 1, 7, 28, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (50, 0, 'Manage images'   	 , 'modify_6' , 4, 1, 7, 50, 7);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (57, 0, 'Print idea'    	 , 'modify_7' , 4, 0, 7, 57, 8);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (8 , 0, 'Delete Idea' 	     , 'modify_8' , 4, 0, 7, 8 , 9);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (29, 0, 'Help' 		  	 , 'modify_9' , 4, 0, 7, 29, 10);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (30, 0, 'Back'   	   		 , 'back_4'   , 4, 0, 7, 30, 11);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (74, 0, 'Change currency' 	 , 'modify_10', 4, 0, 7, 74, 6);
-- access button buttons accs_lvl,                                                                            0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (31, 0, 'Set privacy'        , 'acces_1', 5, 0, 28, 31, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (32, 0, 'Hide from'          , 'acces_2', 5, 0, 28, 32, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (36, 0, 'Who can see'        , 'acces_4', 5, 0, 28, 36, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (33, 0, 'Help'               , 'acces_3', 5, 0, 28, 33, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (34, 0, 'Back'   	         , 'back_5' , 5, 0, 28, 34, 5);
-- Friends button button accs_lvl,s                                                                           0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (38, 0, 'Display friends'    , 'friends_1' , 6, 0, 37, 38, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (39, 0, 'Add friend'   	     , 'friends_2' , 6, 0, 37, 39, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (40, 0, 'Remove friend'      , 'friends_3' , 6, 0, 37, 40, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (41, 0, 'Help'   	         , 'friends_4' , 6, 0, 37, 41, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (42, 0, 'Back'   	         , 'back_6'    , 6, 0, 37, 42, 6);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (43, 0, 'My Requests'        , 'friends_5' , 6, 1, 37, 43, 4);
-- Request button button accs_lvl,s                                                                           0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (44, 0, 'Display requests'   , 'requests_1' , 7, 0, 43, 44, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (45, 0, 'Accept request'     , 'requests_2' , 7, 0, 43, 45, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (46, 0, 'Decline request'    , 'requests_3' , 7, 0, 43, 46, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (47, 0, 'Help'    			 , 'requests_4' , 7, 0, 43, 47, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (48, 0, 'Back'   	         , 'back_7'     , 7, 0, 43, 48, 5);
-- Image button buttons  accs_lvl,                                                                            0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (51, 0, 'List images'        , 'image_1', 8, 0, 50, 51, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (52, 0, 'See image'          , 'image_2', 8, 0, 50, 52, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (53, 0, 'Add image'     	 , 'image_4', 8, 0, 50, 53, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (54, 0, 'Delete image'       , 'image_5', 8, 0, 50, 54, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (55, 0, 'Help'               , 'image_6', 8, 0, 50, 55, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (56, 0, 'Back'   	         , 'back_8' , 8, 0, 50, 56, 6);
-- Users idea button but accs_lvl,tons                                                                        0,
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (61, 0, 'List Ideas'	 , 'usr_idea_1', 9, 0, 60, 61, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (75, 0, 'Choose idea'	 , 'usr_idea_2', 9, 1, 60, 75, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (64, 0, 'Help'          , 'usr_idea_3', 9, 0, 60, 64, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (65, 0, 'Back'   	     , 'back_9'    , 9, 0, 60, 65, 4);
-- Pick idea button
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (76, 0, 'List images', 'usr_img_1', 10, 0, 75, 76, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (77, 0, 'See image'  , 'usr_img_2', 10, 0, 75, 77, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (78, 0, 'Help'       , 'usr_img_3', 10, 0, 75, 78, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (79, 0, 'Back'   	  , 'back_10'  , 10, 0, 75, 79, 4);
-- Films buttons
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (81, 0, 'List all movies', 'movie_1', 11, 0, 80, 81, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (82, 0, 'Pick random', 'movie_2', 11, 0, 80, 82, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (83, 0, 'Add movie', 'movie_3', 11, 0, 80, 83, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (84, 0, 'Modify movie', 'movie_4', 11, 1, 80, 84, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (85, 0, 'Back', 'back_11', 11, 0, 80, 85, 5);
-- Modify Movie buttons
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (93, 0, 'Print moive', 'movie_chg_1', 12, 0, 84, 93, 1);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (86, 0, 'Modify name', 'movie_chg_2', 12, 0, 84, 86, 2);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (87, 0, 'Modify category', 'movie_chg_3', 12, 0, 84, 87, 3);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (88, 0, 'Modify length', 'movie_chg_4', 12, 0, 84, 88, 4);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (89, 0, 'Modify source', 'movie_chg_5', 12, 0, 84, 89, 5);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (90, 0, 'Change note', 'movie_chg_6', 12, 0, 84, 90, 6);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (91, 0, 'Edit note', 'movie_chg_7', 12, 0, 84, 91, 7);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (94, 0, 'Seen', 'movie_chg_8', 12, 0, 84, 94, 8);
INSERT INTO BUTTONS (ID, accs_lvl, DATA, btn_name, keyboardId, isParent, parentId, btn_inf, ordr) VALUES (92, 0, 'Back', 'back_12', 12, 0, 84, 92, 9);
