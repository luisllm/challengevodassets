#!/bin/bash
LOGFILE=/myscripts/getjsons.log
echo "$(date "+%m%d%Y %T"): Starting script" >> $LOGFILE

S3BUCKET="$1"
echo "S3BUCKET: " $S3BUCKET >> $LOGFILE
#ARNSNSTOPIC="$2"
#echo "ARNSNSTOPIC: " $ARNSNSTOPIC >> $LOGFILE

echo "$(date "+%m%d%Y %T"): Getting json files from OMDB" >> $LOGFILE
curl "https://www.omdbapi.com/?i=tt0110912&apikey=cc7ff24c" > /myscripts/pulpFiction.json
curl "https://www.omdbapi.com/?i=tt0076759&apikey=cc7ff24c" > /myscripts/starWars.json
curl "https://www.omdbapi.com/?i=tt0112573&apikey=cc7ff24c" > /myscripts/braveheart.json

echo "$(date "+%m%d%Y %T"): Uploading json files to S3 bucket" >> $LOGFILE
#aws sns publish --topic-arn $ARNSNSTOPIC --message "pulpFiction.json file download and copied to the S3 Bucket" --region us-east-1
aws s3 cp /myscripts/pulpFiction.json "s3://"$S3BUCKET"/json/pulpFiction.json" &>> $LOGFILE
aws s3 cp /myscripts/starWars.json "s3://"$S3BUCKET"/json/starWars.json" &>> $LOGFILE
aws s3 cp /myscripts/braveheart.json "s3://"$S3BUCKET"/json/braveheart.json" &>> $LOGFILE

echo "$(date "+%m%d%Y %T"): Deleting json files from temp" >> $LOGFILE
rm -rf /myscripts/*.json &>> $LOGFILE

echo "$(date "+%m%d%Y %T"): script finish" >> $LOGFILE
