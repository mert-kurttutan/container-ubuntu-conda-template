#!/bin/bash

set -e
apt-get update

apt-get install -y apt-utils

# needed for downloading files
apt-get install -y wget

# Archiving Libraries
apt-get install -y zip unzip bzip2 gzip

apt-get install -y build-essential libssl-dev libasound2

#### Required Libraries for entrypoint.sh script

# jq is used to parse ECS-injected AWSSecretsManager secrets
# apt-get install -y jq

apt-get clean
