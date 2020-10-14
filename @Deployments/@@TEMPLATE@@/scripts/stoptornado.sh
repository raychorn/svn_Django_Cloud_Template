#!/bin/bash

echo "BEGIN: stop-{{app-name}}-tornado"

if [ -f /var/run/{{app-name}}-tornado.pid ]; then
	x=$(cat /var/run/{{app-name}}-tornado.pid)
	kill -9 $x
	rm -f /var/run/{{app-name}}-tornado.pid
else
	echo "Nothing to do !!!"
fi

echo "END! stop-{{app-name}}-tornado"


