#!/bin/sh

USER=$BASH_ARGV[1]
PASSWORD=$BASH_ARGV[0]

mongoimport -h ds029338.mongolab.com --port 29338 -u ${USER} -p ${PASSWORD} --db road --collection roadCases --jsonArray --file road-cases.json
