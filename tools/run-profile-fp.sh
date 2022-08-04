#!/bin/bash

#Usage:
# $ /your/tool/path/run-profile-fp.sh [COMMAND]

#Set arguments
COMMAND=$@

#Path of the working directory where data will be stored.
#If not set, the current path is used
[ -z "$WORKING_PATH" ] && WORKING_PATH=`pwd`

DATA_FOLDER="$WORKING_PATH/Data"
OUT_FOLDER="$WORKING_PATH/Graphs"

unset WORKING_PATH

#Create folders
[ ! -d $DATA_FOLDER ] && mkdir $DATA_FOLDER
[ ! -d $OUT_FOLDER ] && mkdir $OUT_FOLDER

#Run and profile
echo "Profiling: $COMMAND"
CLING_PROFILE=1 perf record --call-graph=fp -F 1000 -o $DATA_FOLDER/raw.data $COMMAND

TOOL_PATH=${0%run-profile-fp.sh}

#Fold data
perf script --no-demangle -i $DATA_FOLDER/raw.data > $DATA_FOLDER/scripted.data
c++filt -p < $DATA_FOLDER/scripted.data > $DATA_FOLDER/after_filt.data
${TOOL_PATH}stackcollapse.pl --all $DATA_FOLDER/after_filt.data > $DATA_FOLDER/folded_by_sc.data

#Flame Graph
${TOOL_PATH}flamegraph.pl -w 1500 --colors java $DATA_FOLDER/folded_by_sc.data > $OUT_FOLDER/flamegraph.svg

#G2D
python ${TOOL_PATH}gprof2dot.py -f perf -o $DATA_FOLDER/graph.dot $DATA_FOLDER/after_filt.data
dot -Tpng -o $OUT_FOLDER/graph.png $DATA_FOLDER/graph.dot
