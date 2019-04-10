#!/bin/bash

source ./config.sh

aws cloudformation deploy \
  --stack-name $STACK_NAME \
  --template-file ./init.yml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  --parameter-overrides \
    "NdfdElement=$NDFD_ELEMENT" \
    "SquareKm=$SQUARE_KM" \
    "CenterLatitude=$CENTER_LATITUDE" \
    "CenterLongitude=$CENTER_LONGITUDE" \
    "TimeZone=$TIMEZONE" \

BUILD_PROJECT=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].Outputs[?OutputKey==`BuildProject`].OutputValue' \
  --output text \
)

echo "Building State Machine, (3-5 min)..."

BUILD_ID=$(aws codebuild start-build \
  --project-name $BUILD_PROJECT \
  --query 'build.id' \
  --output text \
)

while true
do
  BUILD_STATUS=$(aws codebuild batch-get-builds \
    --ids $BUILD_ID \
    --query 'builds[0].buildStatus' \
    --output text
  )
  
  if [ "$BUILD_STATUS" != "IN_PROGRESS" ]
  then
    break
  fi
  
  sleep 10
done

echo $BUILD_STATUS
