#!/bin/bash
set -ex

if [[ ! -z "$1" ]]; then
    PROFILE=$1
else
    PROFILE=default

aws rds delete-db-instance "test-instance"