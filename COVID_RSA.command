
docker stop covid_rsa & echo STOPPING COVID_RSA CONTAINER... ;
docker container rm covid_rsa & echo REMOVING COVID_RSA CONTAINER...;
echo COVID_RSA SUCCESSFULLY STOPPED AND REMOVED! ;
docker pull gcmarais/panthera_interview:latest & echo PULLING COVID_RSA IMAGE...;
echo COVID_RSA SUCCESSFULLY PULLED! ;
docker run -d -p 5001:8050 --name covid_rsa -P gcmarais/panthera_interview:latest & echo OPENING COVID_RSA DASHBOARD...;
sleep 10;
open http://localhost:5001