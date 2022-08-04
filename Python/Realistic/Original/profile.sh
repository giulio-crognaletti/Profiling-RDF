#!/bin/bash

#Script to be profiled
PY_SCRIPT="df105_WBosonAnalysis.py"

#Path of tools
TOOL_PATH="../../../tools"

COMMAND="/usr/bin/time python $PY_SCRIPT"

#Call script in tools
$TOOL_PATH/run-profile-fp.sh $COMMAND
