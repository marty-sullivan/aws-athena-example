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

echo "Building State Machine via CodeBuild (3-5 minutes)..."

BUILD_ID=$(aws codebuild start-build \
  --project-name $BUILD_PROJECT \
  --query 'build.id' \
  --output text \
)

echo "You can watch progress at https://console.aws.amazon.com/codesuite/codebuild/projects/$BUILD_PROJECT/build/$BUILD_PROJECT%3A$BUILD_ID/log"

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

if [ "$BUILD_STATUS" != "SUCCEEDED" ]
then
  echo "There was a problem with the build, report the logs at the link above to the GitHub repository!"
  exit 1
else
  echo "Build complete!"
fi

echo "Running the Athena State Machine to generate your forecast animation (5-10 minutes)..."

ATHENA_MACHINE_ARN=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --query 'Stacks[0].Outputs[?OutputKey==`AthenaMachineArn`].OutputValue' \
  --output text \
)

EXECUTION_ARN=$(aws stepfunctions start-execution \
  --state-machine-arn $ATHENA_MACHINE_ARN \
  --input "{ }" \
  --query 'executionArn' \
  --output text \
)

while true
do
  EXECUTION_STATUS=$(aws stepfunctions describe-execution \
    --execution-arn $EXECUTION_ARN \
    --query 'status' \
    --output text \
  )
  
  if [ "$EXECUTION_STATUS" != "RUNNING" ]
  then
    break
  fi
  
  sleep 10
done

if [ "$EXECUTION_STATUS" != "SUCCEEDED" ]
then
  echo "There was a problem with generating the animation, report the logs at the link above to the GitHub repository!"
  exit 1
else
  echo "Your forecast animation has been generated! View it at the link below!"
  
  ANIMATION_URI=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --query 'Stacks[0].Outputs[?OutputKey==`AnimationUri`].OutputValue' \
    --output text \
  )
  
  echo "$ANIMATION_URI"
fi
