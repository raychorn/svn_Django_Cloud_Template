#!/bin/bash

for f in `find -L /usr/local -iname "vyperlogix*.zip"`; do
	x=$(expr index "$f" @@TEMPLATE@@)
	if [ $x -eq 0 ] ; then
		echo "File -> $f"
	fi
done

