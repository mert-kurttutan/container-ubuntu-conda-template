# AUTHOR: Mert Kurttutan
FROM ubuntu:20.04
LABEL maintainer="mert-kurttutan"

ARG MLFLOW_USER=ml-flow
ARG MLFLOW_USER_HOME=/home/ml-flow

# Run commands with bash
SHELL ["/bin/bash", "--login", "-c"]

RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# system dependencies
COPY script/systemlibs.sh /systemlibs.sh
RUN chmod u+x /systemlibs.sh && /systemlibs.sh

# Install python dependencies with a non-root user
RUN useradd -ms /bin/bash "${MLFLOW_USER}"
USER ml-flow
WORKDIR ${MLFLOW_USER_HOME}

# Python dependencies
COPY --chown=${MLFLOW_USER} ./requirements.txt ${MLFLOW_USER_HOME}/requirements.txt
COPY --chown=${MLFLOW_USER} ./environment.yml ${MLFLOW_USER_HOME}/environment.yml
COPY --chown=${MLFLOW_USER} script/bootstrap.sh ${MLFLOW_USER_HOME}/bootstrap.sh
RUN chmod u+x ${MLFLOW_USER_HOME}/bootstrap.sh && ${MLFLOW_USER_HOME}/bootstrap.sh


# Post bootstrap to avoid expensive docker rebuilds
COPY --chown=${MLFLOW_USER} ./app ${MLFLOW_USER_HOME}/app
COPY --chown=${MLFLOW_USER} ./main.py ${MLFLOW_USER_HOME}/main.py
COPY --chown=${MLFLOW_USER} script/entrypoint.sh ${MLFLOW_USER_HOME}/entrypoint.sh

# App for REST API
ENTRYPOINT ["bash", "-c", "source ./entrypoint.sh && set_python_env && python main.py"]
