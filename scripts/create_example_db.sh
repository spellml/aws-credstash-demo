#!/bin/bash
set -ex

if [[ ! -z "$1" ]]; then
    PROFILE=$1
else
    PROFILE=default
fi
if [[ ! -z "$2" ]]; then
    AZ=$2
else
    AZ=us-west-2a
fi

aws rds create-db-instance \
    --db-instance-identifier test-instance \
    --db-instance-class db.m4.large \
    --engine postgres \
    --master-username read_write \
    --master-user-password password \
    --availability-zone $AZ \
    --allocated-storage 20 \
    --publicly-accessible \
    --profile $PROFILE
ADDRESS=$(aws rds describe-db-instances \
    --db-instance-identifier test-instance \
    --query "DBInstances[0].Endpoint.Address" \
    --output text \
    --profile $PROFILE)
credstash --kms-region us-east-1 \
    --profile $PROFILE \
    put postgres_db_address $ADDRESS
credstash --kms-region us-east-1 \
    --profile $PROFILE \
    put postgres_db_read_write_user_pwd password
