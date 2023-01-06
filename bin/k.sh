#!/bin/sh
kill -9 $(ps -ef | grep /CprSignals/bot.py | awk '{print $2}')
