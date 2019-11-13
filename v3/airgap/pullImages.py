import subprocess

dryRun = False
engine = "docker"
srcRegistry = "registry.redhat.io"
destRegistry = "reg.koz-airgap.redhatgov.io:5000"
dockerHub = "docker.io"
exportDir = "/storage/export/images/"

baseImageSet = ['/openshift3/apb-base',
'/openshift3/apb-tools',
'/openshift3/automation-broker-apb',
'/openshift3/csi-attacher',
'/openshift3/csi-driver-registrar',
'/openshift3/csi-livenessprobe',
'/openshift3/csi-provisioner',
'/openshift3/grafana',
'/openshift3/local-storage-provisioner',
'/openshift3/manila-provisioner',
'/openshift3/mariadb-apb',
'/openshift3/mediawiki',
'/openshift3/mediawiki-apb',
'/openshift3/mysql-apb',
'/openshift3/ose-ansible-service-broker',
'/openshift3/ose-cli',
'/openshift3/ose-cluster-autoscaler',
'/openshift3/ose-cluster-capacity',
'/openshift3/ose-cluster-monitoring-operator',
'/openshift3/ose-console',
'/openshift3/ose-configmap-reloader',
'/openshift3/ose-control-plane',
'/openshift3/ose-deployer',
'/openshift3/ose-descheduler',
'/openshift3/ose-docker-builder',
'/openshift3/ose-docker-registry',
'/openshift3/ose-efs-provisioner',
'/openshift3/ose-egress-dns-proxy',
'/openshift3/ose-egress-http-proxy',
'/openshift3/ose-egress-router',
'/openshift3/ose-haproxy-router',
'/openshift3/ose-hyperkube',
'/openshift3/ose-hypershift',
'/openshift3/ose-keepalived-ipfailover',
'/openshift3/ose-kube-rbac-proxy',
'/openshift3/ose-kube-state-metrics',
'/openshift3/ose-metrics-server',
'/openshift3/ose-node',
'/openshift3/ose-node-problem-detector',
'/openshift3/ose-operator-lifecycle-manager',
'/openshift3/ose-ovn-kubernetes',
'/openshift3/ose-pod',
'/openshift3/ose-prometheus-config-reloader',
'/openshift3/ose-prometheus-operator',
'/openshift3/ose-recycler',
'/openshift3/ose-service-catalog',
'/openshift3/ose-template-service-broker',
'/openshift3/ose-tests',
'/openshift3/ose-web-console',
'/openshift3/postgresql-apb',
'/openshift3/registry-console',
'/openshift3/snapshot-controller',
'/openshift3/snapshot-provisioner',
'/openshift3/metrics-cassandra',
'/openshift3/metrics-hawkular-metrics',
'/openshift3/metrics-hawkular-openshift-agent',
'/openshift3/metrics-heapster',
'/openshift3/metrics-schema-installer',
'/openshift3/oauth-proxy',
'/openshift3/ose-logging-curator5',
'/openshift3/ose-logging-elasticsearch5',
'/openshift3/ose-logging-eventrouter',
'/openshift3/ose-logging-fluentd',
'/openshift3/ose-logging-kibana5',
'/openshift3/prometheus',
'/openshift3/prometheus-alertmanager',
'/openshift3/prometheus-node-exporter']

baseTags = ['v3.11.153', 'v3.11', 'latest']

storageImageSet =[
'/rhgs3/rhgs-server-rhel7',
'/rhgs3/rhgs-volmanager-rhel7',
'/rhgs3/rhgs-gluster-block-prov-rhel7',
'/rhgs3/rhgs-s3-server-rhel7']

storageImageTags = ['v3.11', 'latest']

additionalImageSet = ['/rhel7/etcd:3.2.22']

publicImageSet = [ '/registry:2', '/openshift/hello-openshift:latest' ]

# Pull the main image tag
cmd = "pull"
for tag in baseTags[0:1]:
    for image in baseImageSet:
        command = []
        command.append(engine)
        command.append(cmd)
        command.append(srcRegistry+image+":"+tag)
        if dryRun:
            print(command)
        else:
            subprocess.call(command)
        del command

# Pull the addtionalImageSet
for image in additionalImageSet:
    command = []
    command.append(engine)
    command.append(cmd)
    command.append(srcRegistry+image)
    if dryRun:
        print(command)
    else:
        subprocess.call(command)

    del command

# Pull the storageImageSet
cmd = "pull"
for tag in storageImageTags[0:1]:
    for image in storageImageSet:
        command = []
        command.append(engine)
        command.append(cmd)
        command.append(srcRegistry+image+":"+tag)
        if dryRun:
            print(command)
        else:
            subprocess.call(command)
        del command

# Pull the publicImageSet
for image in publicImageSet:
    command = []
    command.append(engine)
    command.append(cmd)
    command.append(dockerHub+image)
    if dryRun:
        print(command)
    else:
        subprocess.call(command)
    
    del command

# Tag for the destination registry
cmd = "tag"
for tag in baseTags[0:1]:
    for image in baseImageSet:
        command = []
        command.append(engine)
        command.append(cmd)
        command.append(srcRegistry+image+":"+tag)
        command.append(destRegistry+image+":"+tag)
        if dryRun:
            print(command)
        else:
            subprocess.call(command)
        del command

# Tag the storageImageSet for the destination registry
cmd = "tag"
for tag in storageImageTags[0:1]:
    for image in storageImageSet:
        command = []
        command.append(engine)
        command.append(cmd)
        command.append(srcRegistry+image+":"+tag)
        command.append(destRegistry+image+":"+tag)
        if dryRun:
            print(command)
        else:
            subprocess.call(command)
        del command

# Tag the additional images for the destination registry.
for image in additionalImageSet:
    command = []
    command.append(engine)
    command.append(cmd)
    command.append(srcRegistry+image)
    command.append(destRegistry+image)
    if dryRun:
        print(command)
    else:
        subprocess.call(command)

    del command

# Tag the public images for the destination registry.
for image in publicImageSet:
    command = []
    command.append(engine)
    command.append(cmd)
    command.append(dockerHub+image)
    command.append(destRegistry+image)
    if dryRun:
        print(command)
    else:
        subprocess.call(command)

    del command

# Save to tar files.
cmd = "save"
for tag in baseTags[0:1]:
    for image in baseImageSet:
        filename = image.split('/')
        command = []
        command.append(engine)
        command.append(cmd)
        command.append(destRegistry+image+":"+tag)
        command.append('-o')
        command.append(exportDir+filename[2]+'.tar')
        if dryRun:
            print(command)
        else:
            subprocess.call(command)

        del command

# Save the storageImageSet to tar files.
cmd = "save"
for tag in storageImageTags[0:1]:
    for image in storageImageSet:
        filename = image.split('/')
        command = []
        command.append(engine)
        command.append(cmd)
        command.append(destRegistry+image+":"+tag)
        command.append('-o')
        command.append(exportDir+filename[2]+'.tar')
        if dryRun:
            print(command)
        else:
            subprocess.call(command)

        del command

# Save the additional images to tar files.
for image in additionalImageSet:
    filename = image.split('/')
    command = []
    command.append(engine)
    command.append(cmd)
    command.append(destRegistry+image)
    command.append('-o')
    command.append(exportDir+filename[2]+'.tar')
    if dryRun:
        print(command)
    else:
        subprocess.call(command)

    del command

# Save the public images. A hack.
tmp = publicImageSet[0].split('/')
filename = tmp[1].split(':')
command = []
command.append(engine)
command.append(cmd)
command.append(destRegistry+publicImageSet[0])
command.append('-o')
command.append(exportDir+filename[0]+'.tar')
if dryRun:
    print(command)
else:
    subprocess.call(command)

del command

tmp = publicImageSet[1].split('/')
filename = tmp[2]
command = []
command.append(engine)
command.append(cmd)
command.append(destRegistry+publicImageSet[1])
command.append('-o')
command.append(exportDir+filename+'.tar')
if dryRun:
    print(command)
else:
    subprocess.call(command)

del command
