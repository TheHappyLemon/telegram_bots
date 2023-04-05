-- 0 LEVEL BUTTONS
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (1,  'Idea options:'   , NULL					 					  				    , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (2,  'Lookup options:' , NULL					 					  				    , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (3,  'Account options:', NULL					 					  				    , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (37, 'Friends options:', NULL					 					  				    , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (4, NULL			    , 'SELECT DATA FROM HELP WHERE keyboardId = 0 ORDER BY ordr ASC', NULL, NULL, 1);
-- Idea buttons         btn_id                        _inp, status_out
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (5 , NULL		     	 , 'SELECT ID, name, descr, origin, price, isPublic FROM IDEAS WHERE user_id = @^;%& AND sts <> 9', NULL	  , 'tg_id', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (6 , NULL		     	 , 'Enter new Ideas name'	  		            				  						   		  , 'IDEA_CRE', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (7 , 'Modify options'   , 'Enter idea\\`s name to modify'								            			   		  , 'IDEA_MOD', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (8 , NULL		     	 , 'Enter ideas name to delete'	                				  						   		  , 'IDEA_DEL', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (9 , NULL			     , 'SELECT DATA FROM HELP WHERE keyboardId = 1 ORDER BY ordr ASC' 						   		  , NULL	  , NULL, 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (10, 'Choose an option:', NULL															  						   		  , NULL	  , NULL, 0);
-- LookUp buttons       btn_id                        _inp, status_out
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (11, NULL			     , 'SELECT * FROM USERS'     									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (12, NULL			     , 'SELECT * FROM IDEAS'     									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (13, NULL			     , 'SELECT * FROM FRIENDS'   									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (14, NULL			     , 'SELECT * FROM HELP'      									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (15, NULL			     , 'SELECT * FROM IMAGES'    									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (16, NULL			     , 'SELECT * FROM BUTTONS'   									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (17, NULL			     , 'SELECT * FROM BUTTON_INF'									  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (18, NULL			     , 'SELECT * FROM HELP' 										  , NULL, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (49, NULL			     , 'SELECT DATA FROM HELP WHERE keyboardId = 2 ORDER BY ordr ASC' , NULL, NULL, 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (19, 'Choose an option:', NULL					     									  , NULL, NULL, 0);
-- Account button buttonbtn_id                        _inp, status_out
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (20, NULL  			  , 'SELECT name, tg_id FROM USERS WHERE tg_id = @^;%& LIMIT 1'		, NULL	  , 'tg_id' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (21, NULL  			  , 'Enter new name'										   		, 'ME_INP', NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (22 , NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 3 ORDER BY ordr ASC' 	, NULL	  , NULL    , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (23, 'Choose an option:' , NULL													   		, NULL	  , NULL    , 0);
-- Modify button buttonsbtn_id                        _inp, status_out
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (24, NULL			    , 'Enter new name for idea *@^;%&*'       					     , 'MODI_NME', 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (25, NULL			    , 'Enter new description for idea *@^;%&*'					     , 'MODI_DES', 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (26, NULL			    , 'Enter new price  for idea *@^;%&*'     					     , 'MODI_PRC', 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (27, NULL			    , 'Enter new origin for idea *@^;%&*'     					     , 'MODI_ORI', 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (28, 'Privacy options:', NULL									       					 , NULL	     , NULL         ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (29 , NULL			    , 'SELECT DATA FROM HELP WHERE keyboardId = 4 ORDER BY ordr ASC' , NULL      , NULL         ,1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (30, 'Idea options:'   , NULL									     					 , NULL	     , NULL         ,0);
-- Acces button buttons btn_id                        _inp, status_out
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (31, NULL			    , 'Enter new acces mode private or public for idea *@^;%&*'        , 'ACCS_CHG' , 'last_input', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (32, NULL			    , 'Enter friend\\`s name to restrict him seeeing idea *@^;%&*'     , 'ACCS_RMV' , 'last_input', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (36, NULL			    , 'SELECT IF ((SELECT isPublic FROM IDEAS WHERE user_id = @^;%& AND name = \'@^;%&\') = 1, \'Idea is *Public* and *EVERYONE* can see it\', \'SELECT tg_id, name FROM USERS WHERE tg_id IN ( SELECT friend_id FROM FRIENDS WHERE user_id = @^;%& ) AND tg_id NOT IN ( SELECT user_id FROM IDEAS_INF WHERE idea_id = ( SELECT id FROM IDEAS WHERE user_id = @^;%& AND LOWER(name) = ( SELECT last_input FROM USERS WHERE tg_id = @^;%& ) ) );\') AS sub_query', NULL, 'tg_id,last_input,tg_id,tg_id,tg_id', 0);     
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (33, NULL			    , 'SELECT DATA FROM HELP WHERE keyboardId = 5 ORDER BY ordr ASC' , NULL       , NULL        , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (34, 'Modify options:' , NULL											 				 , NULL       , NULL        , 0);                                                           
-- Friends button buttons                             _inp, status_out                                    
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (38, NULL				  , 'SELECT tg_id, name from USERS WHERE tg_id IN (SELECT friend_id FROM FRIENDS WHERE user_id = @^;%&) OR tg_id IN (SELECT user_id FROM FRIENDS WHERE friend_id = @^;%&);', NULL	   , 'tg_id,tg_id', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (39, NULL			      , 'Type user\\`s *name* to send requst'  		     												     																   , 'FRND_ADD', NULL		  , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (40, NULL			      , 'Type your friends *name* to *delete*'     	     												     																   , 'FRND_RMV', NULL		  , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (41, NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 6 ORDER BY ordr ASC' 										 																   , NULL      , NULL		  , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (42, 'Choose an option:' , NULL										 													     																   , NULL      , NULL		  , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (43, 'Request options'   , NULL																								 																   , NULL      , NULL		  , 0);
-- Request button buttons                             _inp, status_out
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (44, NULL			      , 'SELECT tg_id, name FROM USERS WHERE tg_id IN (SELECT user_from FROM FR_REQUESTS WHERE user_to = @^;%& AND sts = 0)', NULL		 , 'tg_id', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (45, NULL			      , 'Type requester *name* to *ACCEPT* it'     	     																    , 'FRND_ACC' , NULL   , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (46, NULL			      , 'Type requester *name* to *REJECT* it'     	     																    , 'FRND_REJ' , NULL   , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (47, NULL			      , 'SELECT DATA FROM HELP WHERE keyboardId = 7 ORDER BY ordr ASC'														, NULL       , NULL   , 1);  
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (48, 'Friends options:'  , NULL     	     															    									, NULL       , NULL   , 0);        
