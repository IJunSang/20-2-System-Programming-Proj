#! /bin/bash

cd CuraEngine
sudo ./build/CuraEngine slice -j $1 -l $2 -o $3
