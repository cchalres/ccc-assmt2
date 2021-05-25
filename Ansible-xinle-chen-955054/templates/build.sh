#!/usr/bin/env bash

. ./openrc.sh; ansible-playbook -i inventory/hosts.ini build.yaml