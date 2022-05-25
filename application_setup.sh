#!/bin/bash
#
# AutOCampus-ICU Setup
#
# Thiebolt F.   Mai.2022
# Maachou K.   Mai.2022

#
#Create React Build Repos
#
echo -e "\n[React] Build Repository Creation ..."
#cd app/autOCampus-icu-backend/autOCampus-icu-frontend ;
#rm -rf node_modules ; #we use these three commands only if npm is installed in your server "apt install npm"
#npm install
#npm run build; #already create a build folder on my personnel machine if you want to create your own youneed to install npm 
#cd ../ ; cd ../ ;cd ../ ;

#
#Build Container Application
#
#docker-compose build --force-rm --no-cache

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

