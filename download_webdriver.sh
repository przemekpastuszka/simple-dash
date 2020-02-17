unameOut="$(uname -s)"
case "${unameOut}" in
    Linux*)     SYSTEM=linux64;;
    Darwin*)    SYSTEM=mac64;;
    *)          SYSTEM="UNKNOWN:${unameOut}"
esac

VERSION=80.0.3987.16
FILENAME=chromedriver_${SYSTEM}.zip

mkdir -p chromedriver_bin
curl http://chromedriver.storage.googleapis.com/${VERSION}/${FILENAME} -o /tmp/${FILENAME}
yes | unzip /tmp/${FILENAME} -d chromedriver_bin

