import json
import urllib.parse
import boto3
import os

print('Loading function')

s3 = boto3.client('s3')
sns = boto3.client('sns')

def lambda_handler(event, context):
    print("Received event")

    # Get the bucket and the key (filename)
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')
    try:
        print("Getting the object from S3")
        print ("Bucket: ", bucket)
        print ("Filename", key)

        response = s3.get_object(Bucket=bucket, Key=key)

        # Get the data from the json file
        jsonData = response['Body'].read()
        jsonToPython = json.loads(jsonData)

        # Replace ',' so that they don't "break" the final csv file
        genre= jsonToPython['Genre'].replace(',',';')
        writer= jsonToPython['Writer'].replace(',',';')
        actors= jsonToPython['Actors'].replace(',',';')
        plot= jsonToPython['Plot'].replace(',',';')
        language= jsonToPython['Language'].replace(',',';')
        country= jsonToPython['Country'].replace(',',';')
        imdbVotes= jsonToPython['imdbVotes'].replace(',','.')
        boxOffice= jsonToPython['BoxOffice'].replace(',','.')

        # Generate the data for the csv file
        body_temp= "Title,Year,Rated,Released,Runtime,Genre,Director,Writer,Actors,Plot,Language,Country,Awards,Poster,Ratings.0.Source,Ratings.0.Value,Ratings.1.Source,Ratings.1.Value,Ratings.2.Source,Ratings.2.Value,Metascore,imdbRating,imdbVotes,imdbID,Type,DVD,BoxOffice,Production,Website,Response"
        body_temp=body_temp+'\n'+jsonToPython['Title']+','+jsonToPython['Year']+','+jsonToPython['Rated']+','+jsonToPython['Released']
        body_temp=body_temp+','+jsonToPython['Runtime']+','+genre+','+jsonToPython['Director']+','+writer+','+actors+','+plot+','+language
        body_temp=body_temp+','+country+','+jsonToPython['Awards']+','+jsonToPython['Poster']+','+jsonToPython['Ratings'][0]['Source']+','+jsonToPython['Ratings'][0]['Value']
        body_temp=body_temp+','+jsonToPython['Ratings'][1]['Source']+','+jsonToPython['Ratings'][1]['Value']
        body_temp=body_temp+','+jsonToPython['Ratings'][2]['Source']+','+jsonToPython['Ratings'][2]['Value']
        body_temp=body_temp+','+jsonToPython['Metascore']+','+jsonToPython['imdbRating']+','+imdbVotes+','+jsonToPython['imdbID']
        body_temp=body_temp+','+jsonToPython['Type']+','+jsonToPython['DVD']+','+boxOffice+','+jsonToPython['Production']
        body_temp=body_temp+','+jsonToPython['Website']+','+jsonToPython['Response']

        # Create the csv file
        new_filename= key.replace('.json','')
        new_filename=new_filename.replace('json/','')
        new_filename= "csv/"+new_filename+".csv"

        print ("Putting csv file to S3")
        s3.put_object(Bucket=bucket, Key=new_filename, Body=body_temp, ContentEncoding='text/csv')

        print ("SNS TOPIC: ", os.environ['SNS_TOPIC_ARN'])
        # Send message to SNS topic
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject="json file converted to csv",
            Message=key+" converted sucessfully to "+new_filename
        )

        print (key+" converted sucessfully to "+new_filename)
        return ('File converted to csv')
    except Exception as e:
        print("Error converting file")
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Subject="Error converting json file to csv",
            Message="Error converting "+key+" to "+new_filename
        )
        print(e)
        raise e
