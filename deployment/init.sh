#!/bin/bash
. ./unimelb-comp90024-2021-grp-39-openrc.sh; ansible-playbook init-instances.yaml; sleep 30; ansible-playbook -i openstack_inventory.py init-application.yaml;