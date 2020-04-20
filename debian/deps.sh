#!/bin/sh

# Intended for Docker testing only.
# Command: sudo docker run --rm -ti -v (pwd):/data debian:buster

set -e
set -x

apt update
apt install -y make nano wget unzip git
apt-get install -y ruby ruby-dev rubygems build-essential
gem install fpm
apt install systemd
