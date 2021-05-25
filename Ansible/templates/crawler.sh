#!/usr/bin/env bash
. ./openrc.sh; ansible-playbook crawler.yaml -i inventory/hosts.ini