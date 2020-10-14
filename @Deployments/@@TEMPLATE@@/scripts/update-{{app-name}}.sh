#!/bin/bash

svn update {{dir-name}}/{{app-name}}/{{app-name}}

FILES={{dir-name}}/{{app-name}}/{{app-name}}/*.sh
chmod +x $FILES
