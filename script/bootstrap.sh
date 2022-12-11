#!/bin/bash -l
set -e

# install adduser and add the airflow user
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ${MLFLOW_USER_HOME}/miniconda3-latest-linux.sh > /dev/null 2>&1
bash ${MLFLOW_USER_HOME}/miniconda3-latest-linux.sh -b -u -p ${MLFLOW_USER_HOME}/miniconda3
rm -f ${MLFLOW_USER_HOME}/miniconda3-latest-linux.sh


# Activate conda
${MLFLOW_USER_HOME}/miniconda3/bin/conda init bash
source ${MLFLOW_USER_HOME}/miniconda3/etc/profile.d/conda.sh

# create new conda environment
conda env create --file=${MLFLOW_USER_HOME}/environment.yml
conda activate fastapi-rest

# snapshot the packages
if [ -n "$INDEX_URL" ]
then
  pip3 freeze > /requirements.txt
else
  # flask-swagger depends on PyYAML that are known to be vulnerable
  # even though Airflow 1.10 names flask-swagger as a dependency, it doesn't seem to use it.
  if [ "$AIRFLOW_VERSION" = "1.10.12" ]
  then
    pip3 uninstall -y flask-swagger
  fi
fi