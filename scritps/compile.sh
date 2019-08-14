echo -n "s3-bukcet: "
read s3bucket
SELENIUM_SCRIPT=../src/app.py
BASE64_ENCODED=`cat $SELENIUM_SCRIPT | openssl base64`
PAYLOAD_STRING='{"Base64Script": "'$BASE64_ENCODED'"}'
echo $PAYLOAD_STRING > ../src/event.json
sam package --template-file ../template.yaml --output-template-file ../deploy.yaml --s3-bucket $s3bucket
