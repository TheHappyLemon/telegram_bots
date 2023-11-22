CREATE TABLE IDEAS_INF (
  idea_id INT NOT NULL,
  user_id BIGINT NOT NULL,
  PRIMARY KEY (idea_id, user_id),
  INDEX idx_idea_id (idea_id),
  INDEX idx_user_id (user_id),
  FOREIGN KEY (idea_id) REFERENCES IDEAS(id),
  FOREIGN KEY (user_id) REFERENCES USERS(tg_id)
);

-- stores users who are forbidden to see an idea
