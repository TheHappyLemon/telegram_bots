-- 0 level buttons
-- 0 level buttons
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to manage your ideas'  			   , 0, 1 , 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to look at system information'		, 0, 2 , 6);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to manage your account'			   , 0, 3 , 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'				     			  		   , 0, 4 , 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to manage your friends and requests' , 0, 37, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to look at oher people ideas'	   , 0, 60, 2);
-- Modify button buttons          , btn_id, ordr
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all your ideas sorting by Filter that is choosen in settings - \'Set Idea filter\' and using mode choosen in settings - \'Set output mode\'' , 1 ,5 , 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new ideas name to create'								  																		  , 1, 6 , 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input ideas name and opens sub-menu to modify it'			  																		  , 1, 7 , 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'				   			  		  							      																		  , 1, 9 , 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'					  							      																		  , 1, 10, 6);
-- LookUp button buttons          , btn_id, ordr
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all users'     	, 2, 11, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Ideas'     	, 2, 12, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Friends'   	, 2, 13, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Helps'     	, 2, 14, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Images'    	, 2, 15, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Buttons'   	, 2, 16, 6);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Button_inf'	, 2, 17, 7);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Fr_requests'	, 2, 58, 8);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Idea_inf'		, 2, 59, 9);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all Feedback'		, 2, 72, 10);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Displays all feedbacks that you have left\. Status:\n\t\t\t0 - not seen\n\t\t\t1 - seen\n\t\t\t2 - working on\n\t\t\t3 - rejected\n\t\t\t4 - done', 2, 73, 11);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits untll you input something for an adminstrator', 2, 71, 12);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'				, 2, 49, 13);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu', 2, 19, 14);
-- Account button buttons         , btn_id, ordr
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Displays all information about your account'			  , 3, 20, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input a new name and changes your name', 3, 21, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input output mode \'long\' or \'short\'. If long mode is choosen, full information about ideas will be printed out. If Short mode is choosen only ideas names will be printed out', 3, 62, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input filter to sort ideas\. Available filters can be found by pressing \'Show filters\'. By default ideas will be sorted by name', 3, 63, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input order to sort ideas\. Available orders can be found by pressing \'Show orders\'. By default ideas will be sorted ascending', 3, 67, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new default currency\. Available currencies can be found by pressing \'Show currencies\'. By default EUR will be used', 3, 69, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all available filters to sort ideas'  																											, 3, 66, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all available orders to sort ideas'  																											, 3, 68, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all supported currencies'  																										, 3, 70, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'								   																											, 3, 22, 6);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'				   																											, 3, 23, 7);
-- Modify button buttons          , btn_id, ordr
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new ideas name and changes choosen idea name to your input'			  , 4, 24, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new ideas description and changes choosen idea description to your input', 4, 25, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new ideas price and changes choosen idea price to your input. Price can be a whole number, a decimal number(both dot and a comma are accepted. Decial numbers, can only have 2 digits after a dot), a range between two numbers (like 12 - 16), and can have \'`\' at the beginning, which means \`approximately\` ', 4, 26, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new ideas source and changes choosen idea source to your input'		  , 4, 27, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to manage ideas access'				   						  				  , 4, 28, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new ideas currency and changes choosen idea currency to your input'	  , 4, 74, 6);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Opens sub-menu to manage ideas images'				   						  				  , 4, 50, 7);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Prints all information about choosen idea. It will always use \'long\' format'				  , 4, 57, 8);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Asks confirmation and deletes choosen idea'			   						  				  , 4, 8 , 9);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'											   						  				  , 4, 29, 10);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'							   						  				  , 4, 30, 11);
-- Acces button buttons           , btn_id, ordr
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input new acces mode \'private\' or \'public\'. Public - any user may see it, if he is not blocked by button \'Hide from\'. Private - only your friends can see it, if they are not blocked', 5, 31, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Restrict user from seeing an idea', 5, 32, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists users who can see and idea' , 5, 36, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'					     , 5, 33, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'		 , 5, 34, 5);
-- Friends button buttons 
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all your friends'    									 		      , 6, 38, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Wait until you input user`s name and sends him request'	 		      , 6, 39, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Wait until you input friend`s name and removes him from your friend list', 6, 40, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'					     							 		      , 6, 41, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'		 							 		      , 6, 42, 6);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Open sub-menu to manage your friend requests'		 		 		      , 6, 43, 4);
-- Request button buttons
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all requests that were sent to you'	 				, 7, 44, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input requester name and adds him to friends', 7, 45, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input requester name and rejects him'		, 7, 46, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'		 					     				    , 7, 47, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'		 		 				    , 7, 48, 5);
-- Image button buttons        
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all images connected to choosen idea'	 				, 8, 51, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input images name (or its number) and sends it to you'   	, 8, 52, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input images new images name and then waits for an images itself'	 				, 8, 53, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input images name (or its number) and deletes it'	    	, 8, 54, 4);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'	 												, 8, 55, 5);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'	 								, 8, 56, 6);
-- Users idea button buttons                                                     
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all ideas of choosen user sorting by Filter that is choosen in settings - \'Set Idea filter\' and using mode choosen in settings - \'Set output mode\'', 9, 61, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input choosen users`s idea and open sub-menu to work with it'								 												, 9, 75, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'	 												, 9, 64, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'	 								, 9, 65, 4);
-- Pick idea button
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Lists all images of choosen user`s choosen idea'		 , 10, 76, 1);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Waits until you input images name (or its number) and sends it to you', 10, 77, 2);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Writes help'	 										 , 10, 78, 3);
INSERT INTO HELP (data, keyboardId, btn_id, ordr) VALUES ('Returns to previous menu'	 						 , 10, 79, 4);
