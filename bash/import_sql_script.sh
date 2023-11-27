#!/bin/bash

# Check if sql script is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <sql_script>"
    exit 1
fi

sql_script=$1

if [ ! -f "$sql_script" ]; then
    echo "Error: file '$sql_script' not found."
    exit 1
fi

# Source the database config
source /home/ubuntu/bash/db_config.sh

mysql -u "$DB_USER" -p"$DB_PASS" -D "$DB_NAME" < "$sql_script"
