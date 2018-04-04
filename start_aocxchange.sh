#!/usr/bin/env bash

xhost +local:aocxchange
docker start aocxchange
docker exec -it aocxchange /bin/bash