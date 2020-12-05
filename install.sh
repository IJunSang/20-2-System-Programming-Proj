#! /bin/bash
chmod -R 755 ./

apt install build-essential autoconf libtool python3-dev python3-sip-dev cmake -y

cd protobuf-3.11.4

./autogen.sh
./configure
make
make install

ldconfig

cd .. && cd libArcus
mkdir build && cd build
cmake ..
make
make install

ldconfig

cd .. && cd .. && cd CuraEngine
mkdir build && cd build
cmake ..
make
