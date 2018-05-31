#!/usr/bin/env sh
# this is not redirect link safe
DEV_HOME=`dirname ${BASH_SOURCE[0]}`/devenv

source $DEV_HOME/helper.sh

ScriptInit ${BASH_SOURCE[0]}

APP_HOME=$PRG_DIR
ENV_SCRIPT_HOME=$APP_HOME/devenv

usage(){
    echo "Usage: env.sh <command> <command_args>"
    echo "<command>:"
    echo "    setup:            creates virtual environment to execute examples"
    echo "    clean:            destroys virtual environment to execute examples"
    echo "    run <example.py>: runs <example.py> in the virtual environment"
    echo "    activate:         executes the virtualenv script 'activate' to change the local environment settings"
    echo "    help:             prints this message"
    echo "<command_args>:"
    echo "    <example.py>: example python file"
}

COMMAND=$1
shift

#echo received command: $COMMAND

if [ "$COMMAND" == "setup" ]; then
    source $ENV_SCRIPT_HOME/env_setup.sh
elif [ "$COMMAND" == "clean" ]; then
    source $ENV_SCRIPT_HOME/env_cleanup.sh
elif [ "$COMMAND" == "run" ]; then
    EXAMPLE=$1
    shift
    if [ -f $EXAMPLE ]; then
        # ensure virtual python environment is setup
        ([ $DEV_ENV_HOME ] && [ -d $DEV_ENV_HOME ]) || source $ENV_SCRIPT_HOME/env_setup.sh
        # run example
        $ENV_PYTHON $EXAMPLE $@
    else
        echo "Example python file ($EXAMPLE) does not exists"
        exit 1
    fi
elif [ "$COMMAND" == "activate" ]; then
    # ensure virtual python environment is setup
    ([ $DEV_ENV_HOME ] && [ -d $DEV_ENV_HOME ]) || source $ENV_SCRIPT_HOME/env_setup.sh
    echo "Use environment command 'deactivate' to restore original environment settings"
    source $ENV_BIN/activate
elif [ "$COMMAND" == "" ] || [ "$COMMAND" == "help" ]; then
    usage
else
    echo "Unknown command $1"
    usage
fi
