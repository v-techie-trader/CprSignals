#!/bin/sh
# This is a comment!
echo run cprsignals 
cd ~/crypto/CprSignals
source venv/bin/activate

python3.9 ~/crypto/CprSignals/bot.py > cprsignals.log 2>&1 &

echo Started cprsignals in backround
echo check cprsignals.log

