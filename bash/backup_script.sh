#!/bin/bash

# Source the database config
source /home/ubuntu/bash/db_config.sh

DATE=$(date "+%Y%m%d_%H:%M:%S")
NAME="${DB_NAME}_${DATE}"

mysqldump -u $DB_USER -p$DB_PASS $DB_NAME > $BACKUP_DIR/$NAME.sql

