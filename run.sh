#!/bin/bash
chromium-browser --app=file://$(pwd)/client.html --window-size="800,600" &
python3 plotly_window/server.py
