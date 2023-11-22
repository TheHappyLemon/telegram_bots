CREATE TABLE FR_REQUESTS (
  user_from BIGINT NOT NULL,
  user_to BIGINT NOT NULL,
  sts INT NOT NULL DEFAULT 0,
  PRIMARY KEY (user_from, user_to),
  INDEX idx_from (user_from),
  INDEX idx_to (user_to),
  FOREIGN KEY (user_from) REFERENCES USERS(tg_id),
  FOREIGN KEY (user_to) REFERENCES USERS(tg_id)
);

-- statuses:
-- 0 - new
-- 5 - rejected
-- 6 - accepted
-- 9 - deleted
