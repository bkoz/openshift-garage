#!/bin/sh

mkdir -p /storage/registry
chmod -R 777 /storage/registry
chcon -R system_u:object_r:container_file_t:s0 /storage/registry
docker run -d -p 5000:5000 --name registry --restart=always -v /storage/registry:/var/lib/registry docker.io/library/registry:2

#
# Clean registry
#
# docker stop registry
# docker rm registry
# rm -rf /storage/registry

