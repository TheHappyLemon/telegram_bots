#!/bin/bash

SESSION_NAME="spotify"

# Check if the session exists and delete it if it does
tmux has-session -t $SESSION_NAME 2>/dev/null
if [ $? -eq 0 ]; then
    tmux kill-session -t $SESSION_NAME
fi

# Create a new tmux session and start it detached
tmux new-session -d -s $SESSION_NAME

# Send commands to the tmux session
tmux send-keys -t $SESSION_NAME C-c
tmux send-keys -t $SESSION_NAME "cd /home/ubuntu" C-m
tmux send-keys -t $SESSION_NAME "source pyenv/bin/activate" C-m
tmux send-keys -t $SESSION_NAME "cd bots/SpotifyBot/" C-m
tmux send-keys -t $SESSION_NAME "python3 spotifyBot.py >> /home/ubuntu/logs/bots/SpotifyBot/spotifyBot.log 2>&1" C-m
