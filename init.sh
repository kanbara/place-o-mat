#!/bin/bash

START=$(date +"%m-%d-%Y-%T")

# abort if there are errors
set -o errexit
set -o xtrace

sudo apt-get install -f -y \
    python3 \
    python3-pip \
    python-pytest \
    curl \
    jq \

# not fancy enough to require ansible in the Vagrantfile
# this will do fine

# googlemaps needs newer chardet and urllib3 than requests
pip3 install -U \
    urllib3 \
    chardet

sudo pip3 install -r /vagrant/requirements.txt

FINISH=$(date +"%m-%d-%Y-%T")

echo "cd /vagrant" > ~/.bashrc
echo "export GMAPS_KEY='<KEY_HERE>'" >> ~/.bashrc
echo "export YELP_KEY='<KEY_HERE>'" >> ~/.bashrc

TOP=$(cd $(dirname $0) && pwd)
echo "export PYTHONPATH=${TOP}" >> ~/.bashrc

# Finished!
echo "-------------------------------"
echo "-        FINISHED!            -"
echo -e "- Start:  $START -"
echo -e "- Finish: $FINISH -"
echo "-------------------------------"
