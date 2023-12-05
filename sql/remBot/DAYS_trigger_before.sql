DELIMITER //

CREATE TRIGGER BEFORE_INSERT_DAYS
BEFORE INSERT ON DAYS
FOR EACH ROW
BEGIN

	IF NEW.format = 2 THEN
	   SET NEW.day = DATE_FORMAT(CURDATE(), '%Y-%m-%d');
	   
           IF NEW.period IS NULL THEN
              SET NEW.period = 'day';
           END IF;

           IF NEW.period_am IS NULL THEN
              SET NEW.period_am = 1;
           END IF;
        
        END IF;
END;

//

DELIMITER ;
