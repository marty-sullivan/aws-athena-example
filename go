#!/bin/bash

source ./config.sh

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --template-file ./init.yml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    "NdfdElement=$NDFD_ELEMENT" \
    "CenterLatitude=$CENTER_LATITUDE" \
    "CenterLongitude=$CENTER_LONGITUDE" \
    "TimeZone=$TIMEZONE" \
