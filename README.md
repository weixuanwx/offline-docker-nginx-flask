# Purpose
- There is a need to maintain and control the software environment of an application sitting in an internet segregated network. The standard manner of building a docker image could not be used as the application environment has no access to the internet to download packages
- This repo walks through the basics of setting up an analytics Flask app in an internet segregated environment served with uWSGI and NginX.
- As long as docker is installed (via offline installations) on the target server, we would be able to test and debug our application in our local environment before updating the docker image.

# Installation/Setup Instructions
## Within your local/development environment
1. Install docker and docker-compose
    1. https://docs.docker.com/compose/install/
2. Run `docker-compose build` at the directory with the docker-compose.yml file
    - You may run `docker-compose up` now to test if your deployment works locally too
3. Save the built Flask and Nginx images from the docker repo into a tarball so you may bring it into your internet segretated environment
    - `docker save app_flask:latest > app_flask.tar`
    - `docker save app_nginx:latest > app_nginx.tar`
4. SCP/SFTP/etc to bring your files into the offline environment
5. If you ran `docker-compose up` from before, you may test your deployments and check your logs
    - `sudo docker logs -n 50 flask` where 'flask' is the name assigned to the instance of the flask app container
    - `sudo docker logs -n 50 nginx` where 'nginx' is the name assigned to the instance of the nginx server container

## Will need to change DB connections to local DB in app/flask/app/api.py. 
#### Assuming the target server is under a CentOS linux environment here
1. On server, install docker and docker-compose
    1. https://docs.docker.com/compose/install/
2. Start Docker Daemon: sudo systemctl start docker
3. run `mkdir my_offline_app` in the directory of your choice
4. Transfer the 2 tar files app_nginx.tar and app_flask.tar in my_offline_app/
5. load the flask app and nginx containers into local repo
    1. `sudo docker load < app_nginx.tar`
    2. `sudo docker load < app_flask.tar`
6. Go to the directory with the .yml file and the top level flask and nginx folder - run the following to start the app in detached mode
    1. `sudo docker-compose up -d`

# Configuration Instructions
- configure ports accordingly.
    - docker-compose.yml
        - nginx: e.g. 8080:80 tells you to listen from external sources on 8080 and passes to port 80 within nginx container
        - flask: e.g. expose: - 5000 opens port 5000 from the Flask app container for the NginX container to communicate to
    - nginx.conf
        - nginx container listens at port 80 and redirects requests via uwsgi to the 'flask' app (docker uses container hostname to find the host) at port 5000
    - app.ini listens for nginx at socket 5000 and calls wsgi file via run.py
- kill or stop by 
    - `docker container kill deploy`
    - `docker container stop deploy`
    - where 'deploy' is the name assigned to the instance of the container
- clean up spinned up dockers
    - `docker container prune`
- clean docker images by:
    - `docker image prune -a`
- check docker container processes running
    - `sudo docker ps`
- restart the deployed docker app
    - `sudo docker-compose restart`

# Dockerfile
- app > flask > app > Dockerfile
    - used the Docker base image python-slim as a few references seems to suggest alpine OS makes the build slower
    - set the working directory for the flask app and copy the contents over
    - install the some basic linux distributions and dependencies as well as uWSGI for the app
    - install the python dependencies from the requirements.txt file
    - included some common nltk downloads
- app > nginx > Dockerfile
	- replaces the default nginx.conf with ours

# Reference:
- https://realpython.com/offline-python-deployments-with-docker/
- https://pythonise.com/series/learning-flask/building-a-flask-app-with-docker-compose#flask-dockerfile