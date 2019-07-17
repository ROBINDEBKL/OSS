### 2019/7/12, lab 6. Robin Hong, hongz@rpi.edu.
# Virtualization



## Step 1 (example0)
Running the command `docker run docker/whalesay cowsay boo`
![step1](./pictures/step1.png)



## Step 2 (example1)
The full syntax for docker run is 

`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

Some options are:
* `-v`: allow user to mount a directory on the *host* machine in the container.
* `-e`: allow for environment variables to be passed into the container.
* `-it`: allow the interaction with the docker container from the command line terminal.

Running the command `docker run -it ubuntu bash`
![step2_1](./pictures/step2_1.png)

Running the command `apt update`
![step2_2](./pictures/step2_2.png)

Installing Vim with `apt intall vim`
![step2_3](./pictures/step2_3.png)

Using Vim to create a new `testfile` in `\root`.
![step2_4](./pictures/step2_4.png)

Installing cowsay with `apt install cowsay` and running.
![step2_5](./pictures/step2_5.png)



## Step 3 (example2)
Running the command `docker run --name db -d mongo:3.2 mongod --smallfiles` and `docker run --name rocketchat -p 3000:3000 --env ROOT_URL=http://localhost --link db:db -d rocket.chat:0.62`
![step3_1](./pictures/step3_1.png)
![step3_2](./pictures/step3_2.png)

Rocketchat at localhost:3000
![step3_3](./pictures/step3_3.png)

Running the command `docker ps` to check running containers, and then `docker stop` and `docker rm` to stop and remove the container.
![step3_4](./pictures/step3_4.png)

Finally use `docker rmi` to remove local images from docker.
![step3_5](./pictures/step3_5.png)



## Step 4 (example3)
Following the instructions of writing Dockerfile, I have run the command `docker build -t lab6step4 .` to build the image and `docker run -p 5000:5000 lab6step4` to run in the container.
![step4_1](./pictures/step4_1.png)
![step4_2](./pictures/step4_2.png)
![step4_3](./pictures/step4_3.png)



## Step 5 (example4)
Creating `Dockerfile`
![step5_1](./pictures/step5_1.png)

Running the command `docker build -t message-app .`
![step5_9](./pictures/step5_9.png)

Running the command `docker images` and `docker run message-app`, which gives some error messages
![step5_2](./pictures/step5_2.png)
![step5_3](./pictures/step5_3.png)

Creating `docker-compose.yml`

Build docker-compose with `docker-compose build`
![step5_4](./pictures/step5_4.png)

Run the services with `docker-compose up`
![step5_5](./pictures/step5_5.png)

Using the message app in another terminal
![step5_6](./pictures/step5_6.png)
![step5_7](./pictures/step5_7.png)
![step5_8](./pictures/step5_8.png)