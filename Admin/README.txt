# run docker with this, first number is the port the dahsboard sends out the second number is port you search on
docker run -p 5001:8050 panthera_dash_gcm_aws 

# push docker image to docker hub
docker build -t <hub-user>/<repo-name>[:<tag>]
docker tag <existing-image> <hub-user>/<repo-name>[:<tag>]
docker commit <existing-container> <hub-user>/<repo-name>[:<tag>] 
docker push <hub-user>/<repo-name>:<tag>


deploy to image to aws
docker tag panthera_dash_gcm_aws:latest public.ecr.aws/w9i9s1d1/dashboard:latest
docker push public.ecr.aws/w9i9s1d1/dashboard:latest

aws ip = 3.139.240.198:8050