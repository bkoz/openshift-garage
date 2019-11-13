#!/bin/bash
EXPORT_DIR=/storage/export/rpms
mkdir -p ${EXPORT_DIR}

subscription-manager clean
subscription-manager register --username=bkozdemb
subscription-manager attach --pool=8a85f99a6ae5e464016b1efbd8000bdb
subscription-manager repos --disable=*
subscription-manager repos \
    --enable="rhel-7-server-rpms" \
    --enable="rhel-7-server-extras-rpms" \
    --enable="rhel-7-server-ose-3.11-rpms" \
    --enable="rhel-7-server-ansible-2.6-rpms"

reposync --newest-only --repoid="rhel-7-server-rpms" \
    --repoid="rhel-7-server-extras-rpms" \
    --repoid="rhel-7-server-ose-3.11-rpms" \
    --repoid="rhel-7-server-ansible-2.6-rpms" --download_path=${EXPORT_DIR}
