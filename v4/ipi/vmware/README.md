# Disconnected OpenShift 4.5.2 IPI install on vmware
## (Some assembly required)

### Perform these steps on the connected host.

* Follow the documentation to [mirror the OpenShift images](https://docs.openshift.com/container-platform/4.5/installing/install_config/installing-restricted-networks-preparations.html#installing-restricted-networks-preparations) to a local directory.

* Follow the documentation to [extract the installation program](https://docs.openshift.com/container-platform/4.5/installing/install_config/installing-restricted-networks-preparations.html#installation-mirror-repository_installing-restricted-networks-preparations) that matches
the desired release version. 

* Download the RHCOS [ova](https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.5/latest/rhcos-4.5.2-x86_64-vmware.x86_64.ova) image that matches the desired release version.

* Copy these artifacts to the target content server on the restricted network. Note, the `ssh` program does not preserve symbolic links so the content must first be archived with a utility such as `tar` before copying. The `rsync -ar` command is another option.

### Perform these steps on the restricted network host.

* Follow the documentation to create a [mirror registry](https://docs.openshift.com/container-platform/4.5/installing/install_config/installing-restricted-networks-preparations.html#installing-restricted-networks-preparations).

* Host the ova file on a web sever that the cluster nodes can access.

* Follow the [IPI install documentation](https://docs.openshift.com/container-platform/4.5/installing/installing_vsphere/installing-vsphere-installer-provisioned-customizations.html)
up to and including creating an installation configuration file (`install-config.yaml`). 

For a disconnected install, a few additional
parameters must be added to `install-config.yaml`.

| Parameter      | Description/Example  |
| :------------- | -----------: |
|`imageContentSources` |The `imageContentSources` section from the output of the command to mirror the repository.|
|`platform.vsphere.clusterOSImage`|http://content.lunchbox.lab:8000/rhcos-4.5.2-x86_64-vmware.x86_64.ova|
|`additionalTrustBundle`|Registry SSL certificate in PEM format|

Have a look at this [install-config example template](install-config-template.yaml) for details.

* Continue with the [IPI install documentation](https://docs.openshift.com/container-platform/4.5/installing/installing_vsphere/installing-vsphere-installer-provisioned-customizations.html).
