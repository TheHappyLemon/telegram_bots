-- 0 LEVEL BUTTONS
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (1,  'Idea options:'   , NULL					 					  				   , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (2,  'Lookup options:' , NULL					 					  				   , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (3,  'Account options:', NULL					 					  				   , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (37, 'Friends options:', NULL					 					  				   , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (4, NULL			   , 'SELECT DATA FROM HELP WHERE keyboardId = 0 ORDER BY ordr ASC', NULL, 1);
-- Idea buttons         btn_id
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (5 , NULL		     	 , 'SELECT ID, name, origin, price, isPublic FROM IDEAS WHERE user_id = @^;%& AND sts <> 9', 'tg_id', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (6 , NULL		     	 , 'Enter new Ideas name'	  		            				  						   , 'IDEA_CRE', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (7 , 'Modify options'   , NULL								            				  						   , NULL		, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (8 , NULL		     	 , 'Enter ideas name to delete'	                				  						   , 'IDEA_DEL', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (9 , NULL			     , 'SELECT DATA FROM HELP WHERE keyboardId = 1 ORDER BY ordr ASC' 						   , NULL		, 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (10, 'Choose an option:', NULL															  						   , NULL		, 0);
-- LookUp buttons       btn_id
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (11, NULL			     , 'SELECT * FROM USERS'     									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (12, NULL			     , 'SELECT * FROM IDEAS'     									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (13, NULL			     , 'SELECT * FROM FRIENDS'   									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (14, NULL			     , 'SELECT * FROM HELP'      									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (15, NULL			     , 'SELECT * FROM IMAGES'    									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (16, NULL			     , 'SELECT * FROM BUTTONS'   									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (17, NULL			     , 'SELECT * FROM BUTTON_INF'									  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (18, NULL			     , 'SELECT * FROM HELP' 										  , NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (49, NULL			     , 'SELECT DATA FROM HELP WHERE keyboardId = 2 ORDER BY ordr ASC' , NULL, 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (19, 'Choose an option:', NULL					     									  , NULL, 0);
-- Account button buttonbtn_id  
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (20, NULL  			  , 'SELECT name, tg_id FROM USERS WHERE tg_id = @^;%& LIMIT 1'		, 'tg_id' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (21, NULL  			  , 'Enter new name'										   		, 'ME_INP', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (22 , NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 3 ORDER BY ordr ASC' 	, NULL	  , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (23, 'Choose an option:' , NULL													   		, NULL	  , 0);
-- Modify button buttonsbtn_id
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (24, NULL			    , 'Type following: *<old\\_name\\>* *<new\\_name\\>*'     		     , 'MODI_NME', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (25, NULL			    , 'Type following: *<idea\\_name\\>* *<new\\_descr\\>*'    		     , 'MODI_DES', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (26, NULL			    , 'Type following: *<idea\\_name\\>* *<new\\_price\\>*'    		     , 'MODI_PRC', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (27, NULL			    , 'Type following: *<idea\\_name\\>* *<new\\_origin\\>*'   		     , 'MODI_ORI', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (28, 'Privacy options:', NULL									       					 , NULL	     , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (29 , NULL			    , 'SELECT DATA FROM HELP WHERE keyboardId = 4 ORDER BY ordr ASC' , NULL      , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (30, 'Idea options:'   , NULL									     					 , NULL	     , 0);
-- Acces button buttons btn_id    
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (31, NULL			    , 'Type following: *<idea\\_name\\>* *<public/private\\>*'		 , 'ACCS_CHG' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (32, NULL			    , 'Type your friends name'					     				 , 'ACCS_RMV' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (36, NULL			    , 'Type <idea\\_name\\>'	   							 		 , 'ACCS_SEE' , 0);     
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (33, NULL			    , 'SELECT DATA FROM HELP WHERE keyboardId = 5 ORDER BY ordr ASC' , NULL       , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (34, 'Modify options:' , NULL											 				 , NULL       , 0);                                                           
-- Friends button buttons                                                                 
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (38, NULL				  , 'SELECT tg_id, name from USERS WHERE tg_id IN (SELECT friend_id FROM FRIENDS WHERE user_id = @^;%&);', 'tg_id'    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (39, NULL			      , 'Type user\\`s *name* to send requst'  		     												     , 'FRND_ADD' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (40, NULL			      , 'Type your friends *name* to *delete*'     	     												     , 'FRND_RMV' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (41, NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 6 ORDER BY ordr ASC' 										 , NULL       , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (42, 'Choose an option:' , NULL										 													     , NULL       , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (43, 'Request options'   , NULL																								 , NULL       , 0);
-- Request button buttons
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (44, NULL			      , 'SELECT tg_id, name FROM USERS WHERE tg_id IN (SELECT user_from FROM FR_REQUESTS WHERE user_to = @^;%& AND sts = 0)', 'tg_id'    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (45, NULL			      , 'Type requester *name* to *ACCEPT* it'     	     																    , 'FRND_ACC' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (46, NULL			      , 'Type requester *name* to *REJECT* it'     	     																    , 'FRND_REJ' , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (47, NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 7 ORDER BY ordr ASC'														, NULL       , 1);  
INSERT INTO BUTTON_INF (btn_id, label, command, status, onlyData) VALUES (48, 'Friends options:'  , NULL     	     															    									, NULL       , 0);        
