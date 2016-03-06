#!/usr/bin/python

import os

os.system("curl -u pi:python -i -H \"Content-Type: application/json\" -X POST -d '{\"title\":\"LightsOn\",\"description\":\"Turn tree lights on\"}' http://api.fisc.us:8080/pwmtree/api/tasks")

