#!/usr/bin/env /bin/bash

ARGV[1]=${1^^} #request type (^^ = strtoupper())
ARGV[2]=${2}   #method name

USERNAME="pi"
PASSWORD="python"

if [ $# -ge 1 ]; then
	set -x
	curl -u ${USERNAME}:${PASSWORD} -i -H "Content-Type: application/json" -X ${ARGV[1]} -d '{"title":"'${ARGV[2]}'"}' http://api.fisc.us:8080/pwmtree/api/tasks

fi