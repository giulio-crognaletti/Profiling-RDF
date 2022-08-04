#!/bin/bash

# source code to be compiled
SRC="rdf-sin.cpp"

#Path of tools
TOOL_PATH="../../tools"

#Compile
$TOOL_PATH/compile.sh $SRC

#Call script in tools
$TOOL_PATH/run-profile-fp.sh ./${SRC%.*}


