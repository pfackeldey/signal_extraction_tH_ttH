#!/usr/bin/env bash

action() {
    local origin="$( /bin/pwd )"

    [ -z "$USER" ] && export USER="$( whoami )"

    #
    # global variables "DHA = Di-Higgs-Analysis"
    #

    export DHA_BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"


    # please set this variable to your e.g. nfs
    export DHA_DATA="/net/scratch/cms/pfackeldey/"

    # complain when certain variables are not set
    true ${USER:?user name environment variable missing}
    true ${DHA_DATA:?data directory environment variable missing}

    # set defaults of other variables
    [ -z "$DHA_SOFTWARE" ] && export DHA_SOFTWARE="$DHA_DATA/software/$USER/$DHA_DIST_VERSION"
    [ -z "$DHA_STORE" ] && export DHA_STORE="$DHA_DATA/store"


    #
    # law setup
    #

    # law and luigi setup
    export LAW_HOME="$DHA_BASE/.law"
    export LAW_CONFIG_FILE="$DHA_BASE/law.cfg"
    # export LAW_TARGET_TMP_DIR="$DHA_DATA/tmp"

    # print a warning when no luigi scheduler host is set
    if [ -z "$DHA_SCHEDULER_HOST" ]; then
        2>&1 echo "NOTE: DHA_SCHEDULER_HOST is not set, use '--local-scheduler' in your tasks!"
    fi

    #
    # CMSSW setup
    #
    [ -z "$DHA_DIST_VERSION" ] && export DHA_DIST_VERSION="slc7"
    [ -z "$SCRAM_ARCH" ] && export SCRAM_ARCH="${DHA_DIST_VERSION}_amd64_gcc700"
    [ -z "$CMSSW_VERSION" ] && export CMSSW_VERSION="CMSSW_10_2_20_UL"
    [ -z "$CMSSW_BASE" ] && export CMSSW_BASE="$DHA_SOFTWARE/cmssw/$CMSSW_VERSION"

    #
    # software setup
    #

    source setup_cmssw.sh

    # VERY IMPORTANT...
    export GLOBUS_THREAD_MODEL="none"

    dha_list_cache_locks() {
        [ -d "$DHA_LOCAL_CACHE" ] && find "$DHA_LOCAL_CACHE" -name "*.lock" -print
    }
    export -f dha_list_cache_locks

    dha_release_cache_locks() {
        [ -d "$DHA_LOCAL_CACHE" ] && find "$DHA_LOCAL_CACHE" -name "*.lock" -delete
    }
    export -f dha_release_cache_locks

    # add _this_ repo
    export PYTHONPATH="$DHA_BASE:$PYTHONPATH"

    # source law's bash completion scipt
    source "$( law completion )"
}
action "$@"
