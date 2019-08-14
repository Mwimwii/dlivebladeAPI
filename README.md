
![alt text](https://steemitimages.com/u/dlive/avatar)

# DLiveBlade
### Social Blade for Dlive TV  

This is official repo for DliveBlade, a population stat page for the Dlive platform in python. In version 0.4 we finally implemented the Serverless-Application-Model which comes with some neat testing features, that speed up local development and deployment:

- SAM Deploy
- Cloudformation Stack
- Sam local invocation
- Reduced the deployment packge 
- Lambda Layers


## File Structure

```bash
.
├── README.md                   <-- This instructions file
├── event.json                  <-- API Gateway Proxy Integration event payload
├── scripts                     <-- Application scripts
├── ├── compile.sh                      
├── ├── chromedriver.sh                 
├── ├── convert.sh                                    
├── src                             <-- Source code for a lambda function
│   ├── __init__.py                     <-- This instructions file
│   ├── app.py                          <-- Lambda function code
│   ├── event.json                      <-- Event payload with the Base64 encoded selenium script                
│   ├── requirements.txt                <-- Lambda function code
├── selenium-lambda-layer                   <-- Lambda layer       
├── ├── bin                                     <-- Chromedriver and chrome binary
├── ├── ├── chromedriver                            
├── ├── ├── headless-chromium                       
├── ├── python                                  <-- This instructions file
├── ├── ├── lib                                     
├── ├── ├── ├── python3.7
├── ├── ├── ├── ├── ssitepackages
├── template.yaml               <-- SAM Template
└── tests                       <-- Unit tests
    └── unit
        ├── __init__.py
        └── test_handler.py
```

## Requirements

* AWS CLI already configured with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)

## Setup process

### Local development

**Invoking function locally using a local sample payload**

```bash
sam local invoke lambdium --event .src/event.json
```

## Packaging and deployment

AWS Lambda Python runtime requires a flat folder with all dependencies including the application. SAM will use `CodeUri` property to know where to look up for both application and dependencies:

```yaml
...
    Lambdium:
        Type: AWS::Serverless::Function
        Properties:
            CodeUri: src/
            ...
```

Firstly, we need a `S3 bucket` where we can upload our Lambda functions packaged as ZIP before we deploy anything - If you don't have a S3 bucket to store code artifacts then this is a good time to create one:

```bash
aws s3 mb s3://BUCKET_NAME
```
Next, run the following command to package our Lambda function to S3:

```bash
sam package \
    --output-template-file packaged.yaml \
    --s3-bucket REPLACE_THIS_WITH_YOUR_S3_BUCKET_NAME
```

Alternatively you can use the `compile.sh` script to package the Lambda function to S3 
```bash
./scripts/compile.sh
```

Next, the following command will create a Cloudformation Stack and deploy your SAM resources.

```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name sam-app \
```

TODO

- Complete 
