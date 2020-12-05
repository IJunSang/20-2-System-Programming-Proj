#! /bin/bash

cd CuraEngine

sudo ./build/CuraEngine slice -v -j "../Cura/resources/definitions/anet3d_a8.def.json" -l "./tests/testModel.stl" -o "test.gcode"

echo "result gcode saved in /CuraEngine/test.gcode"