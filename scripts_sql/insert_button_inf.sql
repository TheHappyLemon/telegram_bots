-- status_inp -> sets user to this status, if button wants input. If button just prints data, used for formatting column label
-- status_out -> used for formatting command column only
-- access = isPublic. 1 -> everyone except blocked sees. 0 - only friends except blocked sees
-- accs_lvl 0 - user, 10 - admin. if users has accs_lvl >= button.accs_lvl he can see it.
--
-- 0 LEVEL BUTTONS
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (1,  'Idea options:'   			, NULL					 					  				    , NULL	 	, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (2,  'Administrator options:'		, NULL					 					  				    , NULL	 	, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (3,  'Account options:'			, NULL					 					  				    , NULL	 	, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (37, 'Friends options:'			, NULL					 					  				    , NULL	 	, NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (60, 'User\\`s ideas options:'		, 'Enter user\\`s name'			  			  				    , 'USRI_SEE', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (4,  'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 0 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL		, 'accs_lvl', 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (80, 'Films options', NULL, NULL, NULL, 0);
-- Idea buttons         btn_id                        _inp, status_out                       
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (5 , 'You have *@^;%&* ideas\nSorted by *@^;%&* *@^;%&*\nOutput mode is *@^;%&*', 'SELECT IF ((SELECT idea_mode FROM USERS WHERE tg_id = @^;%&) = \'short\', \'SELECT name FROM IDEAS WHERE user_id = @^;%& AND sts <> 9 ORDER BY @^;%& @^;%&\', \'SELECT CURRENCIES.sign AS priceSign, IDEAS.name AS Name, IDEAS.description AS Description, IDEAS.price AS Price, IDEAS.currency AS Currency, IDEAS.source AS Source, IDEAS.access as Access FROM IDEAS JOIN CURRENCIES ON IDEAS.currency = CURRENCIES.code WHERE user_id = @^;%& AND sts <> 9 ORDER BY @^;%& @^;%&\') AS sub_query', 'rows_total,idea_filter,idea_sort,idea_mode', 'tg_id,tg_id,idea_filter,idea_sort,tg_id,idea_filter,idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (6 , NULL		     	            , 'Enter new Ideas name'	  		            				, 'IDEA_CRE'  , NULL   , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (7 , 'Modify options'             , 'Enter idea\\`s name to modify'								, 'IDEA_MOD'  , NULL   , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (9 , 'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 1 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL	      , 'accs_lvl'   , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (10, 'Choose an option:'			, NULL															, NULL	      , NULL   , 0);
-- LookUp buttons       btn_id                        _inp, status_out                       
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (11, 'DB has *@^;%&* users'		, 'SELECT * FROM USERS ORDER BY tg_id @^;%&'     				, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (12, 'DB has *@^;%&* ideas'		, 'SELECT * FROM IDEAS ORDER BY ID @^;%&'     					, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (13, 'DB has *@^;%&* friends'	, 'SELECT * FROM FRIENDS ORDER BY user_id @^;%&'   				, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (14, 'DB has *@^;%&* helps'		, 'SELECT * FROM HELP ORDER BY ID @^;%&'      					, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (15, 'DB has *@^;%&* images'		, 'SELECT * FROM IMAGES ORDER BY ID @^;%&'    					, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (16, 'DB has *@^;%&* buttons'	, 'SELECT * FROM BUTTONS ORDER BY ID @^;%&'   					, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (17, 'DB has *@^;%&* button_inf'	, 'SELECT * FROM BUTTON_INF ORDER BY btn_id @^;%&'				, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (58, 'DB has *@^;%&* FR_REQUESTS', 'SELECT * FROM FR_REQUESTS ORDER BY user_from @^;%&'			, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (59, 'DB has *@^;%&* IDEAS_INF'	, 'SELECT * FROM IDEAS_INF ORDER BY idea_id @^;%&'				, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (72, 'DB has *@^;%&* FEEDBACK'	, 'SELECT * FROM FEEDBACK ORDER BY whn @^;%&'				, 'rows_total', 'idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (73, 'You have left *@^;%&* feedbacks\nSorted by time *@^;%&*:', 'SELECT data AS Data, whn AS \'When\', sts AS Status FROM FEEDBACK WHERE user_id = @^;%& ORDER BY whn @^;%&', 'rows_total,idea_sort', 'tg_id,idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (71,  NULL						, 'Please Enter you *Suggestions* or *Complaints*'				, 'ADMN_INP'  , NULL	   , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (49, 'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 2 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL		  , 'accs_lvl'	   , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (19, 'Choose an option:'		    , NULL					     									, NULL		  , NULL	   , 0);
-- Account button buttonbtn_id                        _inp, status_out                       
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (20, 'Your *account* informaton:'    			, 'SELECT name AS Name, tg_id AS \'Telegram id\', last_input AS \'Last input\', sts_chat AS Status, currency AS Currency, idea_filter AS \'Idea filter\', idea_mode AS \'Idea mode\', idea_sort AS \'Idea sort\' FROM USERS WHERE tg_id = @^;%& LIMIT 1', NULL	      , 'tg_id' , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (21, NULL  			  		      			, 'Enter new name'										        																										  , 'ME_INP'      , NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (62, NULL								    	, 'Enter *mode* for idea representation \\(short*\\\\*long\\)'											                                                                  , 'ME_MDE'	  , NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (63, NULL								    	, 'Enter *filter* to sort idea\\.\\\nTo see available *filters* press *\'Show Filters\'*'		                                                                          , 'ME_SRT'      , NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (67, NULL								    	, 'Enter *order* to sort ideas\\.\\\nTo see available *orders* press *\'Show Orders\'*'		                                                                              , 'ME_ORD'      , NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (69, NULL								    	, 'Enter *currency code* \\(3 letters\\)\\.\\\nTo see supported *currencies* press *\'Show currencies\'*'		                                                          , 'ME_PRC'      , NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (66, 'There are *@^;%&* filters available:'	, 'SELECT fname FROM IDEA_FILTERS WHERE code = \'filter\''		   																										  , 'rows_total'  , NULL    , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (68, 'There are *@^;%&* orders available:' 	, 'SELECT fname FROM IDEA_FILTERS WHERE code = \'order\''		   																										  , 'rows_total'  , NULL    , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (70, 'There are *@^;%&* currencies supported:', 'SELECT descr AS Description, code AS Code, sign AS Sign FROM CURRENCIES ORDER BY descr'																				  , 'rows_total'  , NULL    , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (22, 'Button *description* in order' 			, 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 3 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC'			  , NULL	      , 'accs_lvl'    , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (23, 'Choose an option:'		      			, NULL													   	    																										  , NULL	      , NULL    , 0);
-- Modify button buttonsbtn_id                        _inp, status_out                       
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (24, NULL			    			, 'Enter new name for idea *@^;%&*'       					     , 'MODI_NME'  , 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (25, NULL			    			, 'Enter new description for idea *@^;%&*'					     , 'MODI_DES'  , 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (26, NULL			    			, 'Enter new price  for idea *@^;%&*'     					     , 'MODI_PRC'  , 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (27, NULL			    			, 'Enter new source for idea *@^;%&*'     					     , 'MODI_ORI'  , 'last_input' ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (28, 'Privacy options:'			, NULL									       					 , NULL	       , NULL         ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (74, NULL							, 'Enter *currency code* \\(3 letters\\)\\.\\\nSupported *currencies*: Settings\\-*\'Show currencies\'*', 'MODI_CUR', NULL ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (50, 'Image options:'  			, NULL									       					 , NULL	       , NULL         ,0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (57, 'Idea`s *@^;%&*  data:'   	, 'SELECT CURRENCIES.sign AS priceSign, IDEAS.name AS Name, IDEAS.description AS Description, IDEAS.price AS Price, IDEAS.currency AS Currency, IDEAS.source AS Source, IDEAS.access as Access FROM IDEAS JOIN CURRENCIES ON IDEAS.currency = CURRENCIES.code WHERE user_id = @^;%& AND name = \'@^;%&\' AND sts <> 9 LIMIT 1', 'last_input', 'tg_id,last_input', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (8 , NULL	           				, 'Are you sure?\\(yes*\\\\*no\\)'	                				 , 'MODI_DEL'  , NULL   	  , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (29, 'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 4 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC' , NULL        , 'accs_lvl'         ,1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (30, 'Idea options:'   			, 'UPDATE USERS SET last_input = NULL WHERE tg_id = @^;%&'  	 , NULL	       , 'tg_id'      ,0);
-- access button buttons btn_id                        _inp, status_out                      
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (31, NULL			    		           						    , 'Enter new access mode private or public for idea *@^;%&*'        , 'ACCS_CHG' , 'last_input', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (32, NULL			    		           						    , 'Enter user\\`s name to restrict him seeeing idea *@^;%&*'     , 'ACCS_RMV' , 'last_input', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (36, 'SELECT IF((SELECT access FROM IDEAS WHERE user_id = @^;%& AND name = \'@^;%&\') = 1, \'Idea is *public* and *everyone* except users below can see it:\',\'Idea is *private* only following friends can see it:\') AS sub_query', 'SELECT IF ((SELECT access FROM IDEAS WHERE user_id = @^;%& AND name = \'@^;%&\') = 1, \'SELECT name FROM USERS WHERE tg_id = (SELECT user_id FROM IDEAS_INF WHERE idea_id = ( SELECT id FROM IDEAS WHERE user_id = @^;%& AND LOWER(name) = ( SELECT last_input FROM USERS WHERE tg_id = @^;%& ) ) ) ORDER BY name @^;%& \', \'SELECT name FROM USERS WHERE tg_id IN ( SELECT friend_id FROM FRIENDS WHERE user_id = @^;%& ) AND tg_id NOT IN ( SELECT user_id FROM IDEAS_INF WHERE idea_id = ( SELECT id FROM IDEAS WHERE user_id = @^;%& AND LOWER(name) = ( SELECT last_input FROM USERS WHERE tg_id = @^;%& ) ) ) ORDER BY name @^;%&;\') AS sub_query', 'tg_id,last_input', 'tg_id,last_input,tg_id,tg_id,idea_sort,tg_id,tg_id,tg_id,idea_sort', 1);     
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (33, 'Button description in order'        						    , 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 5 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC'   , NULL       , 'accs_lvl'        , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (34, 'Modify options:' 		           						    , NULL											 				  , NULL       , NULL        , 0);                                                           
-- Friends button buttons                             _inp, status_out                                    
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (38, 'You have *@^;%&* friends'   , 'SELECT name from USERS WHERE tg_id IN (SELECT friend_id FROM FRIENDS WHERE user_id = @^;%&) OR tg_id IN (SELECT user_id FROM FRIENDS WHERE friend_id = @^;%&) ORDER BY name @^;%&;', 'rows_total', 'tg_id,tg_id,idea_sort' , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (39, NULL			      		    , 'Type user\\`s *name* to send requst'  		     												     																, 'FRND_ADD'  , NULL		  , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (40, NULL			      		    , 'Type your friends *name* to *delete*'     	     												     																, 'FRND_RMV'  , NULL		  , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (41, 'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 6 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC'											, NULL        , 'accs_lvl'		  , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (42, 'Choose an option:' 		    , NULL										 													     																    , NULL        , NULL		  , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (43, 'Request options'   		    , NULL																								 																    , NULL        , NULL		  , 0);
-- Request button buttons                             _inp, status_out                       
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (44, 'You have *@^;%&* requests'  , 'SELECT name FROM USERS WHERE tg_id IN (SELECT user_from FROM FR_REQUESTS WHERE user_to = @^;%& AND sts = 0) ORDER BY name @^;%&', 'rows_total', 'tg_id,idea_sort', 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (45, NULL			      		    , 'Type requester *name* to *ACCEPT* it'     	     																 , 'FRND_ACC'  , NULL   , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (46, NULL			      		    , 'Type requester *name* to *REJECT* it'     	     																 , 'FRND_REJ'  , NULL   , 0); 
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (47, 'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 7 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL, 'accs_lvl'   , 1);  
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (48, 'Friends options:'  		    , NULL     	     															    									 , NULL        , NULL   , 0);        
-- Image button buttons                                _inp, status_out                      
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (51, 'You have *@^;%&* images in idea *@^;%&*'	, 'SELECT img_num, name FROM IMAGES WHERE idea_id = (SELECT id FROM IDEAS WHERE user_id = @^;%& AND name = \'@^;%&\') AND sts <> 9 ORDER BY img_num', 'rows_total,last_input', 'tg_id,last_input', 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (52, NULL			      		   				, 'Type image\\`s *name* to *SEE* it'    	     																, 'IMAG_SEE'			 , NULL   			 , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (53, NULL			      		   				, 'Type new image\\`s *name*'									   												, 'IMAG_ADD'			 , NULL   			 , 0);  
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (54, NULL			      		   				, 'Type image\\`s *name* to *DELETE* it'						   												, 'IMAG_DEL'			 , NULL   			 , 0);  
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (55, 'Button description in order'			, 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 8 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL 	     , 'accs_lvl'		 , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (56, 'Modify options:'   		   				, NULL  																										, NULL	    			 , NULL   			 , 0);
-- Users idea button buttons                                                                 
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (61, 'User *@^;%&* has *@^;%&* ideas\nSorted by *@^;%&* *@^;%&*\nOutput mode is *@^;%&*'	, 'SELECT IF ((SELECT idea_mode FROM USERS WHERE tg_id = @^;%&) = \'short\', "SELECT name FROM IDEAS WHERE IDEAS.user_id = (SELECT tg_id FROM USERS WHERE name = \'@^;%&\') AND IDEAS.sts <> 9  AND @^;%& NOT IN (SELECT user_id FROM IDEAS_INF WHERE idea_id = IDEAS.id) AND (IDEAS.access = 1 OR (IDEAS.access = 0 AND (@^;%& = (SELECT user_id FROM FRIENDS WHERE friend_id = (SELECT tg_id FROM USERS WHERE name = \'@^;%&\')) OR @^;%& = (SELECT friend_id FROM FRIENDS WHERE user_id = (SELECT tg_id FROM USERS WHERE name = \'@^;%&\'))))) ORDER BY @^;%& @^;%&", "SELECT IDEAS.name AS Name, IDEAS.description AS Description, IDEAS.price AS Price, IDEAS.currency AS Currency, CURRENCIES.sign AS priceSign, IDEAS.source AS Source, IDEAS.access AS Access FROM IDEAS LEFT JOIN CURRENCIES ON IDEAS.currency = CURRENCIES.code WHERE IDEAS.user_id = (SELECT tg_id FROM USERS WHERE name = \'@^;%&\') AND IDEAS.sts <> 9 AND @^;%& NOT IN (SELECT user_id FROM IDEAS_INF WHERE idea_id = IDEAS.id) AND (IDEAS.access = 1 OR (IDEAS.access = 0 AND (@^;%& = (SELECT user_id FROM FRIENDS WHERE friend_id = (SELECT tg_id FROM USERS WHERE name = \'@^;%&\')) OR @^;%& = (SELECT friend_id FROM FRIENDS WHERE user_id = (SELECT tg_id FROM USERS WHERE name = \'@^;%&\'))))) ORDER BY @^;%& @^;%&;") AS sub_query', 'last_input,rows_total,idea_filter,idea_sort,idea_mode', 'tg_id,last_input,tg_id,tg_id,last_input,tg_id,last_input,idea_filter,idea_sort,last_input,tg_id,tg_id,last_input,tg_id,last_input,idea_filter,idea_sort', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (75, NULL						   , 'Enter idea\\`s name', 'OUSR_IDE', 'last_input', 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (64, 'Button description in order', 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 9 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL , 'accs_lvl'		   , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (65, 'Choose an option:'		   , NULL																							 	    , NULL		 		     			 , NULL		   , 0);
-- Pick idea button
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (76, 'User *@^;%&* has *@^;%&* images in idea *@^;%&*', 'SELECT img_num, name FROM IMAGES WHERE idea_id = (SELECT id FROM IDEAS WHERE user_id = (SELECT tg_id FROM USERS WHERE name =  \'@^;%&\') AND name = \'@^;%&\') AND sts <> 9 ORDER BY img_num', 'last_input,rows_total,last_idea', 'last_input,last_idea', 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (77, NULL			      		   					   , 'Type image\\`s *name* to *SEE* it'    	     																		        							, 'IMAG_SEE_1'			 	, NULL   			 		  , 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (78, 'Button description in order'					   , 'SELECT HELP.DATA FROM BUTTONS JOIN HELP ON BUTTONS.ID = HELP.btn_id WHERE BUTTONS.keyboardId = 10 AND @^;%& >= BUTTONS.accs_lvl ORDER BY BUTTONS.ordr ASC', NULL 					    , 'accs_lvl'		   		  , 1);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (79, 'User options:'		   						   , NULL																							 	    												    , NULL		 		     	, NULL		   				  , 0);
-- Films buttons
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (81, 'There are *@^;%&* movies', 'SELECT IF ((SELECT idea_mode FROM USERS WHERE tg_id = @^;%&) = \'short\', \'SELECT name FROM FILMS ORDER BY name\', \'SELECT name AS Name, category AS Category, length AS Length, link AS Source, user_notes AS Notes, seen AS Seen FROM FILMS ORDER BY name\') AS sub_query', 'rows_total', 'tg_id', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (82, NULL, 'If you want a random movie *within a specific category*, provide the *desired category*, otherwise type *\'No\'*', 'MOVIE_RAND', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (83, NULL, 'Type movie *name* to *add* it', 'MOVIE_ADD', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (84, 'Modify options:', 'Type movie *name* to *modify* it', 'MOVIE_MOD', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (85, 'Choose an option:', NULL, NULL, NULL, 0);
-- Modify Movie buttons
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (93, 'Here is *@^;%&* movie:', 'SELECT name AS Name, category AS Category, length AS Length, link AS Source, user_notes AS Notes, seen AS Seen FROM FILMS WHERE name = \'@^;%&\'', 'last_input', 'last_input', 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (86, NULL, 'Type new *name* of a movie', 'MOVIE_CHG_1', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (87, NULL, 'Type new *category* of a movie', 'MOVIE_CHG_2', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (88, NULL, 'Type new *length* of a movie', 'MOVIE_CHG_3', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (89, NULL, 'Type new *source* of a movie', 'MOVIE_CHG_4', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (90, NULL, 'Type text to *Change* a *note* of a movie', 'MOVIE_CHG_5', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (91, NULL, 'Type text to *Append* to a *note* of a movie', 'MOVIE_CHG_6', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (94, NULL, 'Have you *seen* this movie?\\(yes*\\\\*no\\)\\. Typing \'Yes\' will remove this movie from random picker', 'MOVIE_CHG_7', NULL, 0);
INSERT INTO BUTTON_INF (btn_id, label, command, status_inp, status_out, onlyData) VALUES (92, 'Films options', NULL, NULL, NULL, 0);
