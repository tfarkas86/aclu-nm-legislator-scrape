1. To permit public downloads from S3 buckets, it's not enough to make the bucket public. 
You must update bucket policy (S3 -> <BUCKET> -> Permissions -> Bucket Policy) as below: 

{
    "Version": "2012-10-17",
    "Id": "Policy1661291954730",
    "Statement": [
        {
            "Sid": "Stmt1661291950787",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<BUCKET-NAME>/*"
        }
    ]
}

The AWS Policy Generator was used to create this policy. Not sure whether this can be copy/pasted for another bucket.  

2. To enable pandas in Lambda function, add a managed layer to the function AWS DataWrangler Python 3.9. 

3. For scraping, Lambda functions have timeout of 3 seconds, so will need to increase this considerably. Maybe Lambda not ideal for scraping?

4. To trigger Lambda function from website, create a Lambda Function  URL (Configuration pane) and use as href in website link. Note, you must put all code to be executed multiple times (on event) in the event handler. All code outside the event handler gets run only on deploy.  

5. To enable HTTP API, you need to use payload format Version 2.0. Switch from 1.0 in the Integration details. 

6. Probably disregard #6. Instead, add a $default route and attach the appropriate integration. Probably not necessary if API call is made properly, but the $default route catches anything, so ambiguously specified calls will route there.  

7. For a functional POST request (and maybe other REST API calls), create a POST request in the root resource, then Actions > Deploy. See tutorial: https://aws.amazon.com/getting-started/hands-on/build-web-app-s3-lambda-api-gateway-dynamodb/module-three/

