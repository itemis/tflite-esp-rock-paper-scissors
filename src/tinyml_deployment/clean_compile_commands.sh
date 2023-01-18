#!/bin/bash
echo "---- ---- ---- ---- ---- ----"
echo "---- ---- ---- CLEANING compile_commands.json"
echo "---- ---- ---- ---- ---- ----"

# make script executable form any path within project
SCRIPT=$(readlink -f $0)
SCRIPTPATH=`dirname $SCRIPT`
BUILD_PATH=$SCRIPTPATH/build

# remove ESP-IDF specific flags in order for clang-tidy to work
sed -i "s/-mlongcalls/ /g" $BUILD_PATH/compile_commands.json
sed -i "s/-fno-tree-switch-conversion/ /g" $BUILD_PATH/compile_commands.json
sed -i "s/-fstrict-volatile-bitfields/ /g" $BUILD_PATH/compile_commands.json