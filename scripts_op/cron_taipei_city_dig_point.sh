#!/bin/bash

if [ "${BASH_ARGC}" != "1" ]
then
  echo "usage: cron_taipei_city_dig_point.sh [ini_filename]"
  exit 0
fi

ini_filename=${BASH_ARGV[0]}

cd roadpin_crawlers
. __/bin/activate
python -m app.cron.taipei_city.cron_taipei_city_dig_point -i "${ini_filename}"
cd ..
