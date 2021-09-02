@echo off
title COVID DASHBOARD
echo STOPPING CONTAINERS...
echo STOPPED: & docker stop covid_rsa 
echo REMOVING CONTAINERS... 
echo REMOVED: & docker container rm covid_rsa 

echo PULLING IMAGE... 
docker pull gcmarais/panthera_interview:latest 
echo IMAGE PULLED!

echo SPINNING UP CONTAINER... 
docker run -d -p 5001:8050 --name covid_rsa -P gcmarais/panthera_interview:latest 
echo CONTAINER SPINNED UP! 
echo STARTING UP DASHBOARD...
timeout 5 
start http://localhost:5001 
echo DASHBOARD STARTED!
