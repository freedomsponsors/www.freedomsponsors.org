#!/bin/bash
HOST=ec2-54-186-164-147.us-west-2.compute.amazonaws.com

function deploy {
    rsync -a --progress * ubuntu@$HOST:./frespo/
    ssh ubuntu@$HOST "cd frespo && docker build -t frespo ."
}