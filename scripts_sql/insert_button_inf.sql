-- 0 LEVEL BUTTONS
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (1, 'Idea options:'   , NULL					 					  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (2, 'Lookup options:' , NULL					 					  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (3, 'Account options:', NULL					 					  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (4, NULL			   , 'SELECT DATA FROM HELP WHERE keyboardId = 0' , NULL, 1);
-- Idea buttons         btn_id
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (5 , NULL		     	 , 'SELECT ID, name, origin, price, isPublic FROM IDEAS WHERE user_id = (SELECT ID FROM USERS WHERE tg_id = @^;%& LIMIT 1) AND sts <> 9', 'tg_id', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (6 , NULL		     	 , 'Enter new Ideas name'	  		            , 'IDEA_CRE', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (7 , 'Modify options'   , NULL								            , NULL		, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (8 , NULL		     	 , 'Enter ideas name to delete'	                , 'IDEA_DEL', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (9 , NULL			     , 'SELECT DATA FROM HELP WHERE keyboardId = 1' , NULL		, 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (10, 'Choose an option:', NULL											, NULL		, 0);
-- LookUp buttons       btn_id
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (11, NULL			     , 'SELECT * FROM USERS'     					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (12, NULL			     , 'SELECT * FROM IDEAS'     					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (13, NULL			     , 'SELECT * FROM FRIENDS'   					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (14, NULL			     , 'SELECT * FROM HELP'      					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (15, NULL			     , 'SELECT * FROM IMAGES'    					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (16, NULL			     , 'SELECT * FROM BUTTONS'   					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (17, NULL			     , 'SELECT * FROM BUTTON_INF'					, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (18, NULL			     , 'SELECT DATA FROM HELP WHERE keyboardId = 2' , NULL, 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (19, 'Choose an option:', NULL					     					, NULL, 0);
-- Account button buttonbtn_id  
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (20, NULL  			  , 'SELECT ID, name, tg_id FROM USERS WHERE tg_id = @^;%& LIMIT 1', 'tg_id' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (21, NULL  			  , 'Enter new name'											   , 'ME_INP', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (22 , NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 3' 			       , NULL	 , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (23, 'Choose an option:' , NULL														   , NULL	 , 0);
-- Modify button buttonsbtn_id
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (24, NULL			  , 'Type following: <old_name>  <new_name>'     , 'MODI_NME', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (25, NULL			  , 'Type following: <idea_name> <new_descr>'    , 'MODI_DES', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (26, NULL			  , 'Type following: <idea_name> <new_price>'    , 'MODI_PRC', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (27, NULL			  , 'Type following: <idea_name> <new_origin>'   , 'MODI_ORI', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (28, 'Acces options:', NULL									     , NULL	     , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (29 , NULL			  , 'SELECT DATA FROM HELP WHERE keyboardId = 4' , NULL      , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (30, 'Idea options:' , NULL									     , NULL	     , 0);
-- Acces button buttons btn_id    
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (31, NULL			    , 'Type following: <idea_name>  <public/private>'							 , 'ACCS_CHG' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (32, NULL			    , 'Type your friends unique ID. He can find it in My account -> Display Info', 'ACCS_ADD' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (33, NULL			    , 'Type your friends unique ID. He can find it in My account -> Display Info', 'ACCS_RMV' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (34, NULL			    , 'SELECT DATA FROM HELP WHERE keyboardId = 5' 								 , NULL       , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (35, 'Modify options:' , NULL																	     , NULL       , 0);         
