#!/usr/bin/env sh

SCRIPT_DIR=`dirname ${BASH_SOURCE[0]}`

source $SCRIPT_DIR/helper.sh

ScriptInit ${BASH_SOURCE[0]}

cd $PRG_DIR

# check and delete virtual environment directories

PYTHON_DEV_ENV=$PRG_DIR/dev_python_env

APP_TOOLS=$PRG_DIR/tools

[ -d $PYTHON_DEV_ENV ] && echo "Removing Python virtual environment at: $PYTHON_DEV_ENV" && $(rm -rf $PYTHON_DEV_ENV)
[ -d $APP_TOOLS ] && echo "Removing Local tool virtualenv at: $APP_TOOLS" && $(rm -rf $APP_TOOLS)

# unset environment variables 
unset DEV_ENV_HOME
unset ENV_BIN
unset ENV_PYTHON
unset ENV_PIP

cd $SAVED
