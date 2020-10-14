#!/bin/bash

svn checkout https://unmetered.vyperlogix.com/svn/repo1/trunk/python/_django-projects/{{app-name}} {{dir-name}}/{{app-name}}/{{app-name}} --username read_only --password peekab00
