#!/bin/bash

# Save current window id
CURRENT_WINDOW=$(wmctrl -l | head -1 | cut -d ' ' -f 1)

# Run server background
PLOTLY_FIG_DIR=$(pwd)/plotly_figs python3 $VIEWER_DIR/server.py &> /dev/null &

# Run plot viewer background
chromium-browser --app=file://$VIEWER_DIR/client.html --window-size="800,600" &> /dev/null &
VIEWER_PID=$!

# Restore windowfocus
sleep 0.7
wmctrl -i -a $CURRENT_WINDOW

ipython -i

# Cleanup
SERVER_PIDS=$(ps aux|grep python|grep server.py|awk '{print $2}')
kill -KILL $SERVER_PIDS &> /dev/null
kill -KILL $VIEWER_PID &> /dev/null
