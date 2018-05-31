#!/usr/bin/env sh

############ Helper functions #############

ToolExists() {
    command -v $1 >/dev/null 2>&1
}

ScriptInit() {
    PRG="$1"
    SAVED="`pwd`"

    # Attempt to set APP_HOME
    # Resolve links: $0 may be a link
    # Need this for relative symlinks.
    local SOURCE=$PRG 
#"${BASH_SOURCE[0]}"
    while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
        local DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
        local SOURCE="$(readlink "$SOURCE")"
        [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
    done
    PRG_DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

}


############ END HELPER FUNCTIONS #########

