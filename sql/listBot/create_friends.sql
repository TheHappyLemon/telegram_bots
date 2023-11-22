CREATE TABLE FRIENDS (
  user_id BIGINT NOT NULL,
  friend_id BIGINT NOT NULL,
  PRIMARY KEY (user_id, friend_id),
  INDEX idx_user_id (user_id),
  INDEX idx_friend_id (friend_id),
  FOREIGN KEY (user_id) REFERENCES USERS(tg_id),
  FOREIGN KEY (friend_id) REFERENCES USERS(tg_id)
);
