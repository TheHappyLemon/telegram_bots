--   MAIN KEYBOARD                                                                               id   text         func                         group next ord prnt  accs
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(1 , 'My events'     ,  NULL           , 0, 1   , 0, NULL, 0 , 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(43, 'My invitations',  NULL           , 0, 7   , 1, NULL, 0 , 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(24, 'My settings'   ,  NULL           , 0, 5   , 2, NULL, 0 , 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(7 , 'Admin'         ,  NULL           , 0, 6   , 3, NULL, 10, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(59, 'Help'          ,  'get_help'     , 0, NULL, 4, NULL, 0 , 'IDLE');
--   EVNT KEYBOARD                                                                               id   text         func                           group next ord prnt  accs
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(2 , 'Print events'   , 'print_events'   , 1, NULL, 0, 1, 0, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(3 , 'Add Regular'    , 'add_regular'    , 1, NULL, 1, 1, 0, 'EVENTS_ADD_R');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(4 , 'Add Irregular'  , 'add_irregular'  , 1, NULL, 2, 1, 0, 'EVENTS_ADD_I');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(60 , 'Add Continious', 'add_continious' , 1, NULL, 3, 1, 0, 'EVENTS_ADD_C');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(5 , 'Modify data'    , 'pick_event_mod' , 1, NULL, 4, 1, 0, 'EVENTS_PICK_D');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(6 , 'Modify acces'   , 'pick_event_mod' , 1, NULL, 5, 1, 0, 'EVENTS_PICK_A');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(55, 'Unsubscribe'    , 'pick_event_look', 1, NULL, 6, 1, 0, 'EVENTS_PICK_U');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(56, 'Stop redacting' , 'pick_event_mod' , 1, NULL, 7, 1, 0, 'EVENTS_PICK_R');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(22, 'Back'           , NULL             , 1, 0   , 8, 1, 0, 'IDLE');
-- MODIFY KEYBOARD                                                                               id   text         func                                        group next ord prnt  accs
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(8 , 'Delete'            , 'delete_event'    , 2, NULL, 0,  5, 0, 'MODIFY_DEL'                       );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(9 , 'Change date'       , 'change_date'     , 2, NULL, 1,  5, 0, 'MODIFY_DATE', 'is_event_regular'  );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(10, 'Change description', 'change_desc'     , 2, NULL, 2,  5, 0, 'MODIFY_DESC'                      );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(11, 'Change period'     , 'change_period'   , 2, NULL, 3,  5, 0, 'MODIFY_PER', 'is_event_regular,is_event_continious');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(12, 'Change amount'     , 'change_amount'   , 2, NULL, 4,  5, 0, 'MODIFY_AMT', 'is_event_regular,is_event_continious');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(48, 'Change weekday'    , 'change_weekday'  , 2, NULL, 5,  5, 0, 'MODIFY_WKD', 'is_event_irregular' );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(49, 'Change occurence'  , 'change_occurence', 2, NULL, 6,  5, 0, 'MODIFY_OCR', 'is_event_irregular' );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(50, 'Change month'      , 'change_month'    , 2, NULL, 7,  5, 0, 'MODIFY_MTH', 'is_event_irregular' );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(61, 'Change start date' , 'change_date'     , 2, NULL, 8,  5, 0, 'MODIFY_BGN', 'is_event_continious');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(62, 'Change end date'   , 'change_date'     , 2, NULL, 9,  5, 0, 'MODIFY_END', 'is_event_continious');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(63, 'Delete after execution', 'change_delIfPast', 2, NULL, 10, 5, 0, 'MODIFY_PST', 'is_event_regular,is_event_continious');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(51, 'Back'              , NULL              , 2, 1   , 11, 5, 0, 'IDLE'                             );
-- ACCES KEYBOARD                                                                               id   text         func                                      group next ord prnt accs
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(17, 'Make private'     , 'make_private'   , 3, NULL, 0, 6, 0, 'MAKE_PRIVATE'  , 'is_event_public' );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(18, 'Make public'      , 'make_public'    , 3, NULL, 1, 6, 0, 'MAKE_PUBLIC'   , 'is_event_private');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(31, 'Who can see'      , 'acces_who'      , 3, NULL, 2, 6, 0, 'IDLE'                              );
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(13, 'Remove subscriber', 'pick_subscriber', 3, NULL, 3, 6, 0, 'SUBSCRIBER_RMV', 'is_event_private');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(14, 'Print invitations', 'invites_print'  , 3, NULL, 4, 6, 0, 'INVITE_SEE'    , 'is_event_private');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(15 , 'Send invitation' ,  NULL            , 3, 8   , 5, 6, 0, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(16, 'Delete invitation', 'pick_invitation', 3, NULL, 6, 6, 0, 'INVITE_PICK'   , 'is_event_private');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(20, 'Back'             , NULL             , 3, 1   , 7, 6, 0, 'IDLE'                              );
--   SETTINGS KEYBOARD                                                                                      id   text               func             group next ord prnt accs 
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(29, 'Change name'     , 'change_name'     , 5, NULL, 0, 24, 0, 'MODIFY_NAME');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(36, 'My feedback '    , 'feedback_print'  , 5, NULL, 1, 24, 0, 'FEEDBACK_PRINT');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(37, 'Leave feedback'  , 'feedback_leave'  , 5, NULL, 2, 24, 0, 'FEEDBACK_LEAVE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(38, 'Delete feedback' , 'pick_feedback_my', 5, NULL, 3, 24, 0, 'FEEDBACK_DELET');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(30, 'Back'            , NULL              , 5, 0   , 4, 24, 0, 'IDLE');
--   ADMIN KEYBOARD                                                                                         id   text               func        group next ord prnt accs 
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(32, 'See feedback', 'feedback_see'     , 6, NULL, 0, 7, 10, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(33, 'Answer to'   , 'pick_feedback_adm', 6, NULL, 1, 7, 10, 'FEEDBACK_ANSW');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(34, 'Ban user'    , 'ban_user'         , 6, NULL, 2, 7, 10, 'BAN_USER');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(57, 'Jobs'        , 'print_jobs'       , 6, NULL, 3, 7, 10, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(58, 'Recalculate', 'calc_force'       , 6, NULL, 4, 7, 10, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(35, 'Back'        , NULL               , 6, 0   , 4, 7, 10, 'IDLE');
--   ADMIN KEYBOARD                                                                                         id   text               func                group next ord prnt accs 
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(44, 'Print invitations', 'print_invitations_my', 7, NULL, 0, 43, 0, 'IDLE');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(45, 'Accept invitation', 'pick_invitation_my'  , 7, NULL, 1, 43, 0, 'INVITE_PICK_MY_A');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(46, 'Reject invitation', 'pick_invitation_my'  , 7, NULL, 2, 43, 0, 'INVITE_PICK_MY_R');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user) VALUES(47, 'Back'             , NULL                  , 7, 0   , 3, 43, 0, 'IDLE');
--   ADMIN KEYBOARD                                                                                         id   text               func       group next ord prnt accs 
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user, showif) VALUES(52, 'Invite subscriber', 'invite_send_look'  , 8, NULL, 0, 15, 0, 'INVITE_SEND_LOOK', 'is_event_private');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(53, 'Invite redactor'  , 'invite_send_modify', 8, NULL, 1, 15, 0, 'INVITE_SEND_MODF');
INSERT INTO DAYS_buttons (id, text, func, group_num, nextGroup, ordr, parent_id, accs_lvl, sts_user)         VALUES(54, 'Back'     , NULL                , 8, 3   , 2, 15, 0, 'IDLE');
