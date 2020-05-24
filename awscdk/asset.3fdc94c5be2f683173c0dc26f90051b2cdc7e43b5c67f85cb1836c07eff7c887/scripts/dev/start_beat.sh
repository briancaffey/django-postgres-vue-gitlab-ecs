#!/bin/bash

set -o nounset
set -o errexit

PIDFILE='/code/celerybeat.pid'
SCHEDULE_FILE='/code/celerybeat-schedule'

trap "rm ${PIDFILE} ; exit 130" SIGINT
trap "rm ${PIDFILE} ; exit 137" SIGKILL
trap "rm ${PIDFILE} ; exit 143" SIGTERM

if [[ -f $PIDFILE ]]
then
  rm $PIDFILE
fi

if [[ -f $SCHEDULE_FILE ]]
then
  rm $SCHEDULE_FILE
fi

exec python3 manage.py watch_celery_beat
