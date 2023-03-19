CREATE UNIQUE INDEX indid
ON USERS (ID);

CREATE UNIQUE INDEX indtg_id
ON USERS (tg_id);

CREATE UNIQUE INDEX indid
ON IDEAS (ID);

CREATE INDEX induser_id
ON IDEAS (user_id);

CREATE INDEX indiduser_id
ON IDEAS (id, user_id);

CREATE INDEX indprice
ON IDEAS (price);

CREATE INDEX indidea_id
ON FRIENDS (idea_id);



