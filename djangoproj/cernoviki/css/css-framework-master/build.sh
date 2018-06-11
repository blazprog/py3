#! /bin/bash

# Variables
FRAMEWORK_VERSION="4.0.2"
FRAMEWORK_NAME=framework
FRAMEWORK_CR="/* css-framework v${FRAMEWORK_VERSION} http://css-framework.com/ | http://creativecommons.org/licenses/by/3.0/ */"

CR_FILE=./css/cr.css
LESS_FILE=./less/${FRAMEWORK_NAME}.less
CSS_FILE=./css/${FRAMEWORK_NAME}.css
CSS_MIN_FILE=./css/${FRAMEWORK_NAME}.min.css
CSS_MIN_TEMP_FILE=${CSS_MIN_FILE}.temp

YUICOMPRESSOR=`find . -type f -name yuicompressor\*.jar`

echo 'Remove old css files...'
rm ./css/*

echo 'CSS building & compression...'
lessc ${LESS_FILE} > ${CSS_FILE}
java -jar ${YUICOMPRESSOR} -o ${CSS_MIN_TEMP_FILE} ${CSS_FILE}

# Put head
echo "${FRAMEWORK_CR}" >> ${CR_FILE}
cat ${CR_FILE} ${CSS_MIN_TEMP_FILE} > ${CSS_MIN_FILE}

echo 'Removing temp files...'
rm ${CR_FILE} ${CSS_MIN_TEMP_FILE}

echo 'Done.'