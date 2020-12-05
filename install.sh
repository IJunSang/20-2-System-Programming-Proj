#! /bin/bash
sudo chmod -R 755 ./

sudo apt update

sudo apt install -y build-essential autoconf libtool python3-dev python3-sip-dev cmake

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
