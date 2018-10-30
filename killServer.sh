kill -9 $(ps -aef | grep server.py | grep -v grep | awk -F ' ' '{print $2}')
