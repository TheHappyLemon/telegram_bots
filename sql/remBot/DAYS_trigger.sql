DELIMITER //

CREATE TRIGGER ON_INSERT_DAYS
AFTER INSERT ON DAYS
FOR EACH ROW
BEGIN
    INSERT INTO link (usr_id, id1, opt, format) VALUES (NEW.who, NEW.id, 'look' , 'days');
	INSERT INTO link (usr_id, id1, opt, format) VALUES (NEW.who, NEW.id, 'modify' , 'days');
	IF (NEW.format = 1) THEN
		INSERT INTO WEEKDAY_prm (day_id) VALUES(NEW.id);
	ELSEIF (NEW.format = 2) THEN
		INSERT INTO CONTINIOUSDAY_prm (day_id, day_start) VALUES(NEW.id, DATE_FORMAT(CURDATE(), '%Y-%m-%d'));
	END IF;
END;

//

DELIMITER ;
