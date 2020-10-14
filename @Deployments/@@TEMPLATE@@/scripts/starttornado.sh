#!/bin/bash

echo "BEGIN: start-{{app-name}}-tornado"

if [ -f /var/run/{{app-name}}-tornado.pid ]; then
	rm -f /var/run/{{app-name}}-tornado.pid
	echo "Nothing to do !!!"
else
	nohup {{dir-name}}/{{app-name}}/{{app-name}}/runtornado.sh > {{dir-name}}/{{app-name}}/{{app-name}}/nohup2.out 2>&1&
	sleep 5
	ps aux | grep {{app-name}}/tornadowsgi.py | grep -v grep | awk '{print $2}' | tail -n 1 > /var/run/{{app-name}}-tornado.pid
fi

echo "END! start-{{app-name}}-tornado"


