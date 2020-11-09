#!/bin/bash
# Save current window id
CURRENT_WINDOW=$(wmctrl -l | head -1 | cut -d ' ' -f 1)

# Run server background
PLOTLY_FIG_DIR=$(pwd)/plotly_figs python3 $VIEWER_DIR/server.py &> /dev/null &
SERVER_PID=$!

# Run plot viewer background
chromium-browser --app=file://$VIEWER_DIR/client.html --window-size="800,600" &> /dev/null &
VIEWER_PID=$!

# Wait 1 sec and restore window focus from the browser
sleep 1
wmctrl -i -a $CURRENT_WINDOW

ipython -i $1

# Cleanup
kill -KILL $SERVER_PID
wait $SERVER_PID &> /dev/null
kill -KILL $VIEWER_PID &> /dev/null
rmdir ./plotly_figs &> /dev/null
