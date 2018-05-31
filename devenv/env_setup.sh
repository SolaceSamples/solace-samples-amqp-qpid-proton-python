#!/usr/bin/env sh

SCRIPT_DIR=`dirname ${BASH_SOURCE[0]}`

source $SCRIPT_DIR/helper.sh

ScriptInit ${BASH_SOURCE[0]}

cd $PRG_DIR
APP_HOME="`pwd -P`"
cd "$SAVED"


if [ $(ToolExists python) ]; then
    echo "python not found please install python."
    exit 1
fi

PATH_PYTHON_CMD=`which python`

echo APP home:  $APP_HOME

# locate/setup virtual environment tool

if ! [ $(ToolExists virtualenv) ]; then

    mkdir -p $APP_HOME/tools

    cd $APP_HOME/tools

    # TODO make configurable
    VENV_MAJOR="16"
    VENV_MINOR="0"
    VENV_MAINTAINCE=".0" # this seems to be optional for previous versions

    VENV_DIR="virtualenv-${VENV_MAJOR}.${VENV_MINOR}${VENV_MAINTAINCE}"
    VENV_CMD_PATH=$APP_HOME/tools/$VENV_DIR

    # check for local install of virtualenv
    if ! [ -d $VENV_CMD_PATH ] && ! [ -f $VENV_CMD_PATH/virtualenv.py ]; then
        # download source for virtualenv tool
        curl -L "https://files.pythonhosted.org/packages/source/v/virtualenv/${VENV_DIR}.tar.gz" > ${VENV_DIR}.tar.gz
        tar xvfz ${VENV_DIR}.tar.gz
    fi

    cd $VENV_DIR

    VENV_CMD="$PATH_PYTHON_CMD $VENV_CMD_PATH/virtualenv.py"

else

    VENV_CMD=vitualenv

fi

# intialize python developer environment

export DEV_ENV_HOME=$APP_HOME/dev_python_env

if ! [ -d $DEV_ENV_HOME ]; then

    $VENV_CMD $DEV_ENV_HOME

fi

cd $APP_HOME

export ENV_BIN=$DEV_ENV_HOME/bin

export ENV_PYTHON=$ENV_BIN/python

export ENV_PIP=$ENV_BIN/pip

# install environment dependencies

$ENV_PIP install python-qpid-proton

cd $SAVED


