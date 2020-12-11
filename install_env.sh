#!/usr/bin/env bash
###############################################
# Universidade Federal do Rio de Janeiro
# Engenharia Eletrônica e da Computação
# DCM - Data Center Manager
# Aluno: Ewerton Vasconcelos da Silva
# Orientador: Rodrigo de Souza Couto 
###############################################
## Variables:
red=`tput setaf 1`
green=`tput setaf 2`
reset=`tput sgr0`

## Detecting platform:
function CheckDistro () {
    log "i" "Cheking Distro:"
    UNAME=$(uname | tr "[:upper:]" "[:lower:]")
    if [ "$UNAME" == "linux" ]; then
        if [ -f /etc/lsb-release -o -d /etc/lsb-release.d ]; then
            export DISTRO=$(lsb_release -i | cut -d: -f2 | sed s/'^\t'//)
        fi

        if [ "$DISTRO" == "Ubuntu" ]; then
            log "i" "Running Ubuntu, starting installation"
        else
            log "e" "Distro $DISTRO not supported, aborting."
            exit 0
        fi
    else 
        log "e" "Platform is not linux, aborting."
        exit 0
    fi

    unset UNAME 
    unset DISTRO

}
## Detecting if running as root:
function CheckIfRoot() {
    log "i" "Check if running as root:"
    if [ "$EUID" -ne 0 ]; then 
        log "e" "Please run this script as root, aborting."
        exit 0
    else
        log "i" "Running as root"
    fi
}

function CheckInternetConn () {
    log "i" "Check internet connection:"
    echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        log "i" "Internet connection is available, proceeding instalation."
    else
        log "e" "Internet connection is NOT available, proceeding instalation."
    fi
}

function InstallRequirements () {
    log "i" "Installing Requiremetns:"
    apt --yes install build-essential libevent-dev libjpeg62-dev uuid-dev libbsd-dev make gcc libjpeg8 libjpeg-turbo8 libuuid1 libbsd0
}


function log () {
    if [ "$1" == "i" ] ; then
        status="${green}INFO${reset}"
    elif [ "$1" == "e" ]; then
        status="${red}ERROR${reset}"
    fi

    echo "$(date) - $status - $2 "

}




CheckDistro
CheckIfRoot
CheckInternetConn
InstallRequirements