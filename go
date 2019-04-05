#!/bin/bash

aws cloudformation deploy \
  --stack-name athena-lambda-example-build \
  --template-file ./build.yml \
  --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM \
  

  
  