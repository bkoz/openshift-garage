# How to move a container image into an airgapped OpenShift cluster

## Requirements
OpenShift v3.11 installed on RHEL7

This example should work with either ```docker``` or ```podman``` container engine clients. On a RHEL7 system, the ```docker``` commands should be run as ```root```.

This example assumes the airgapped cluster can access and pull an images from a separate insecure registry.

### Procedure

1) Pull the image into container storage.

```docker pull docker.io/openshift/hello-openshift```

2) Tag it for the destination registry.

```docker tag docker.io/openshift/hello-openshift reg.koz.redhatgov.io:5000/hello-openshift```

3) Save the image to a storage device that can be moved to the airgapped environment.

```docker save reg.koz.redhatgov.io:5000/hello-openshift -o image-archive.tar```

4) Load the image that was saved.

```docker load -i image-archive.tar```

5) Push to the destination registry.

```docker push reg.koz.redhatgov.io:5000/hello-openshift```

6) Login to OpenShift, create a project and a new application.

```
$ oc login
$ oc new-project hello
$ oc new-app --insecure-registry=true reg.koz.redhatgov.io:5000/hello-openshift
```

Check the pod is running.
```
$ oc get pods
```

Expose the service as a route and visit the application.
```
$ oc expose svc hello-openshift

$ HELLO_ROUTE=$(oc get route --selector=app=hello-openshift --output=custom-columns=NAME:.spec.host --no-headers)

$ curl $HELLO_ROUTE
```

### Image pull test

Skopeo inspect test.

```
$ skopeo inspect docker://reg.koz.redhatgov.io:5000/hello-openshift
```
