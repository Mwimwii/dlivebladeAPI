
sam_lib=~/projects/sam-app/selenium-lambda-layer
site_pkg=~/projects/sam-app/selenium-lambda-layer/python/lib/python3.7/site-packages/
alias pip3.7='~/python37/bin/pip3'

cd $sam_lib

echo -n " Chromedriver version: "
read chromedriver
echo -n " headless-chromium version "
read headless
echo -n " selenium version "
read sln

#rm $sam_lib/headless-chromium
#rm $sam_lib/chromedriver
rm Rf bin
rm -Rf python

mkdir -p bin

curl -SL https://chromedriver.storage.googleapis.com/2.$chromedriver/chromedriver_linux64.zip > chromedriver.zip
curl -SL https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-$headless/stable-headless-chromium-amazonlinux-2017-03.zip > headless-chromium.zip
pip3.7 install selenium==$sln --target $site_pkg/
pip3.7 install lxml --target $site_pkg/

unzip headless-chromium.zip -d bin/
unzip chromedriver.zip -d bin/

rm headless-chromium.zip
rm chromedriver.zip

zip -r selenium-lambda-layer.zip headless-chromium chromedriver python/

cd -


