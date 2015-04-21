#!/bin/bash
SYS=`uname`
ARCH=`uname -m`
git submodule update --init
cd jd-cmd
mvn clean package
cp jd-cli/target/jd-cli.jar .. 
cd ..
cd dex2jar-build
mvn clean package
unzip ./dex-tools/target/dex2jar-*.zip
rm -Rf ../dex2jar
mv dex2jar-* ../dex2jar
cd ..
chmod 755 dex2jar/*
cd ./apktool-build
./gradlew
./gradlew build fatJar
cp -f ./brut.apktool/apktool-cli/build/libs/apktool-cli.jar ../apktool/apktool.jar
cd ..
pwd
