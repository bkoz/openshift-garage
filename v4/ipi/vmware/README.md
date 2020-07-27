# Disconnected OpenShift 4.5.2 IPI install on vCenter
## (Some assembly required)

### Perform these steps on a RHEL7/8 host connected to the internet.

1. Follow the [documentation to mirror the OpenShift release-image content](https://docs.openshift.com/container-platform/4.5/installing/install_config/installing-restricted-networks-preparations.html#installing-restricted-networks-preparations) to a local directory.

2. Follow the [documentation to extract the installation program](https://docs.openshift.com/container-platform/4.5/installing/install_config/installing-restricted-networks-preparations.html#installation-mirror-repository_installing-restricted-networks-preparations) that matches
the desired release version. 

3. Download the [RHCOS ova image](https://mirror.openshift.com/pub/openshift-v4/dependencies/rhcos/4.5/latest/rhcos-4.5.2-x86_64-vmware.x86_64.ova) that matches the desired release version.

4. Copy all these artifacts to a RHEL7/8 content server on the restricted network. Note, the `ssh` program does not preserve symbolic links so the content must first be archived with a utility such as `tar` before copying. The `rsync -ar` command is another option.

### Perform these steps on the restricted network content server.

1. Follow the [documentation to create a local mirror registry](https://docs.openshift.com/container-platform/4.5/installing/install_config/installing-restricted-networks-preparations.html#installing-restricted-networks-preparations) and upload the OpenShift release-image content. 

2. Host the RHCOS ova file on a web server that the content server can access.

3. Follow all the steps in the [IPI install documentation](https://docs.openshift.com/container-platform/4.5/installing/installing_vsphere/installing-vsphere-installer-provisioned-customizations.html) up to and including creating an installation configuration file (`install-config.yaml`).

4. A disconnected install requires the following additional
parameters be added to the installation configuration file. Refer to the [install-config example template](install-config-template.yaml) for examples.

| Parameter      | Description |
| :------------- | :---------- |
|`imageContentSources` |Lists the sources and local repositories for the release-image content.|
|`platform.vsphere.clusterOSImage`|A URL to the locally hosted RHCOS ova file.|
|`additionalTrustBundle`|Local registry cert or CA bundle in PEM format|

5. Continue with the [IPI install documentation](https://docs.openshift.com/container-platform/4.5/installing/installing_vsphere/installing-vsphere-installer-provisioned-customizations.html) to run the installer.
