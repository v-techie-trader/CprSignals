#!/bin/sh
# This is a comment!
echo run halftrend
cd ~/halftrend
source venv/bin/activate

python3.9 manage.py runserver 0:8000 > webhook.log 2>&1 &

echo Started haltrend in the backround
echo check webhook.log and dashboard.log

