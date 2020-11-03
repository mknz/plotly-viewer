#!/bin/bash
google-chrome --app=http:localhost:5000 --window-size="800,600" &
python3 plotly_window/__main__.py
