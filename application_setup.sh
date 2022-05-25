#!/bin/bash
#
# AutOCampus-ICU Setup
#
# Thiebolt F.   Mai.2022
# Maachou K.   Mai.2022



#
#Build Container Application
#
docker-compose build --force-rm --no-cache

#
#Export variables
#
if [ "$#" == "0" ]; then
    export MQTT_PASSWD='test'
    export MQTT_USER='test'
    export APPLICATION_USERNAME='admin'
    export APPLICATION_PASSWORD='admin'
    export APPLICATION_SERVER='http://defi-midoc.univ-tlse3.fr'
else :
    export MQTT_USER="$1"
    export MQTT_PASSWD="$2"
    export APPLICATION_USERNAME="$3"
    export APPLICATION_PASSWORD="$4"
    export APPLICATION_SERVER="$5"
fi
#
#Start container
#
docker-compose --verbose up -d 

