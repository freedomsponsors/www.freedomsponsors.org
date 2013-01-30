#reconstruct private key file to authenticate on Github

if [ $TRAVIS_SECURE_ENV_VARS == "false" ]
then 
	exit 0
fi
oi

echo -n $idrsa_{00..28} >> ~/.ssh/id_rsa_base64
base64 --decode --ignore-garbage ~/.ssh/id_rsa_base64 > ~/.ssh/id_rsa
chmod 600 ~/.ssh/id_rsa
echo -e "Host github.com\n\tStrictHostKeyChecking no\n" >> ~/.ssh/config

git clone --quiet --branch=gh-pages git://github.com/freedomsponsors/www.freedomsponsors.org.git gh-pages
cp -Rf coverage_html_report/ gh-pages/
cd gh-pages/
git add .
git commit -m 'adding coverage reports generated on Travis'
git push origin gh-pages