# Template for FAST Rest Api using Ubuntu and Conda

This repo contains the skeleton code for implementation of REST Api using fast api and conda environment.

## Why ?

The setting `FastApi + Ubuntu + Conda + Docker` seems to be used frequently enough to have a template for it.

I have also seen some other people describing this setting. But, it seems that they are using miniconda image rather Ubuntu image. Here, I want to have the flexibility of choosing ubuntu image myself.

If you want to use Ubuntu as a base image, there is also a problem due to `sh` being default shell. This template resolves this by calling necessary conda commands to activate the environment properly.

## Installation

If inside WSL, use this to start docker

```Bash
sudo service docker start
```

Then build docker image locally,

```Bash
sudo docker build --tag fastapi-rest:latest .
```

Then, run docker container using the docker image we just created

```Bash
sudo docker-compose up
```

Then, send get request to local endpoint `http://localhost:8080/greetings` (either through command line tool e.g. CURL or your browser). The server will send back the json response of the form

```Python
{
    'greetings': 'Hello World!'
}
```
