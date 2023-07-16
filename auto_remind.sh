#!/bin/bash

# Step 1: Activate Python virtual environment
source /home/ubuntu/pyenv/bin/activate >> /var/log/remBot.log

# Step 2: Launch remBot.py
python3 /home/ubuntu/scripts_bot/remBot/remBot.py >> /var/log/remBot.log
