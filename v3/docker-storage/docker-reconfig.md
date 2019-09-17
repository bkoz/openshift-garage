# Changing Docker Storage for an existing OCP v3.11 cluster.

=> This procedure is not supported by Red Hat but is based on this [documentation](https://docs.openshift.com/container-platform/3.11/day_two_guide/docker_tasks.html#changing-the-storage-backend).

## Procedure

This example was performed on a single master and used ```/dev/xvdf``` for docker storage with the
```overlay2``` driver.

For each node in the cluster.

- Drain the node and mark it as not schedulable.
- Shutdown and disable the node service.
- Shutdown and disable the docker service.
- Remove the docker storage configuration.
- Remove the docker directory.
- Reboot if necessary.
- Create the new docker storage configuration.
- Start and enable docker.
- Start and enable the node service.
- Mark the node as schedulable.

Login with cluster-admin privileges and mark the node as not schedulable.
```
$ oc login https://api-server-url -u admin
```
```
$ oc adm manage-node <node> --schedulable=false
```

Drain off the running pods.
```
$ oc adm drain <node> --force=true --ignore-daemonsets=true
```
Login to the node as a super user.

Shutdown the services.
```
# systemctl stop atomic-openshift-node
# systemctl disable atomic-openshift-node
# systemctl stop docker
# systemctl disable docker
````
If necessary, remove the old docker storage configuration.

```
# docker-storage-setup list
# docker-storage-setup remove containers
```
Remove the old docker directory.
```
# rm -rf /var/lib/docker
```
If removing ```/var/lib/docker``` fails with a ```device busy``` error, reboot the node.

Remove the old docker storage configuration.

```
# rm /etc/sysconfig/docker-storage
```
Now configure ```/etc/sysconfig/docker-storage-setup```.

Next, create the storage configuration.

Example ```/etc/sysconfig/docker-storage-setup``` file.
```
STORAGE_DRIVER=overlay2
VG=containers
DEVS=/dev/xvdf
WIPE_SIGNATURES=true
CONTAINER_ROOT_LV_NAME="container-root-lv"
CONTAINER_ROOT_LV_MOUNT_PATH="/var/lib/docker"
```
Create the new storage configuration.
```
# docker-storage-setup create containers /etc/sysconfig/docker-storage-setup

INFO: Volume group backing root filesystem could not be determined
INFO: Writing zeros to first 4MB of device /dev/xvdf
4+0 records in
4+0 records out
4194304 bytes (4.2 MB) copied, 0.0147041 s, 285 MB/s
INFO: Device node /dev/xvdf1 exists.
  Physical volume "/dev/xvdf1" successfully created.
  Volume group "containers" successfully created
  Logical volume "container-root-lv" created.
Created storage configuration containers
```

Confirm the storage configuration.
```
# docker-storage-setup list

NAME                     DRIVER           STATUS        
containers               overlay2         active 
```

Start and enable docker.
```
# systemctl restart docker
# systemctl enable docker
```
Confirm the new storage configuration. The docker service should create this file.
```
# cat /etc/sysconfig/docker-storage

DOCKER_STORAGE_OPTIONS="--storage-driver overlay2 "
```
```
# docker info | grep "Storage Driver"

Storage Driver: overlay2
```
Confirm the logical volume and mount point.
```
 # lvscan

  ACTIVE            '/dev/containers/container-root-lv' [<12.00 GiB] inherit
  ```
  ```
# df /var/lib/docker

Filesystem                                 1K-blocks  Used Available Use% Mounted on
/dev/mapper/containers-container--root--lv  12568576 33152  12535424   1% /var/lib/docker
```
Start and enable the node service.
```
# systemctl restart atomic-openshift-node
# systemctl enable atomic-openshift-node
```

Run ```docker ps``` and notice the control plane pods are running.

Mark the node as schedulable.

```
$ oc adm manage-node <node> --schedulable=true

NAME                             STATUS    ROLES     AGE       VERSION
ip-172-33-112-116.ec2.internal   Ready     master    53m       v1.11.0+d4cacc0
```
```
$ oc get nodes


NAME                             STATUS    ROLES     AGE       VERSION
ip-172-33-112-116.ec2.internal   Ready     master    53m       v1.11.0+d4cacc0
ip-172-33-20-242.ec2.internal    Ready     compute   42m       v1.11.0+d4cacc0
ip-172-33-239-252.ec2.internal   Ready     infra     42m       v1.11.0+d4cacc0
```