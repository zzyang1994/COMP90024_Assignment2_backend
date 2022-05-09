#!/usr/bin/env bash
ansible-playbook -i ./inventory/openstack_inventory.py -u ubuntu --key-file=~/.ssh/test01privatekey deploy_backend.yaml