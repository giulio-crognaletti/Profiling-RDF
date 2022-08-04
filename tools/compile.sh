#!/bin/bash

#Usage:
# $ /path/tools/compile.sh /name/of/source.cpp

#Name of the source (with .cpp extension)
SRC=$1

#Compile example
g++ -o ${SRC%.*} -g -fno-omit-frame-pointer $SRC `root-config --cflags --glibs`
