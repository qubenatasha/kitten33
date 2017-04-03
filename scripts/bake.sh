#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $KITTEN33_DOCKER_IMAGE_LOCAL

docker build -t $KITTEN33_DOCKER_IMAGE_LOCAL:$KITTEN33_IMAGE_VERSION . 
