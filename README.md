# challengevodassets

getjsons.sh
Shell script to download some json files from OMDB and to copy them into an S3 bucket

nagraChallengeLuisLongoCloudFormation.yaml
CloudFormation template

convertJsonToCsv.py
Lambda function to process and convert a json file to a csv file, and then send messages to an SNS topic

sendMessageToSlack.js
Lambda function to send messages to Slack
(https://gist.github.com/vgeshel/1dba698aed9e8b39a464)

