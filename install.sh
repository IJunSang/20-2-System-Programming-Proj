#! /bin/bash
sudo chmod -R 755 ./

sudo apt update -y

ECHO "update complete"
sudo apt install build-essential -y
sudo apt install autoconf -y
sudo apt install libtool -y
sudo apt install python3-dev -y
sudo apt install python3-sip-dev -y
sudo apt install cmake -y

cd protobuf-3.11.4

./autogen.sh
./configure
make -j
sudo make install

sudo ldconfig

cd .. && cd libArcus
mkdir build && cd build
cmake ..
make
sudo make install

sudo ldconfig

cd .. && cd .. && cd CuraEngine
mkdir build && cd build
cmake ..
make
