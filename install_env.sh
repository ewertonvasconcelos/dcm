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
            exit 1
        fi
    else 
        log "e" "Platform is not linux, aborting."
        exit 1
    fi

    unset UNAME 
    unset DISTRO

}
## Detecting if running as root:
function CheckIfRoot() {
    log "i" "Check if running as root:"
    if [ "$EUID" -ne 0 ]; then 
        log "e" "Please run this script as root, aborting."
        exit 1
    else
        log "i" "Running as root"
    fi
}

## Checking if internet connection is available:
function CheckInternetConn () {
    log "i" "Check internet connection:"
    echo -e "GET http://google.com HTTP/1.0\n\n" | nc google.com 80 > /dev/null 2>&1

    if [ $? -eq 0 ]; then
        log "i" "Internet connection is available, proceeding instalation."
    else
        log "e" "Internet connection is NOT available, proceeding instalation."
    fi
}

## Installing system requirements:
function InstallRequirements () {
    log "i" "Installing Requiremetns:"
    apt --yes install build-essential libevent-dev libjpeg62-dev uuid-dev libbsd-dev make gcc libjpeg8 libjpeg-turbo8 libuuid1 libbsd0 git tar
}


function InstallUstreamer () {
    log "i" "Installing uStreamer package:"
    if [ -d "/usr/bin/ustreamer" ]; then
        log "i" "uStreamer already installed, skipping installation"
        return 0
    else
        tar -xzvf ./packages/ustreamer-*.tar.gz -C /usr/bin
        cd /usr/bin/ustreamer
        make
        ver=$(/usr/bin/ustreamer/ustreamer -v)
        if [ "$?" == "0" ]; then
            log "i" "Successfully  installed and running on version $ver"
        else
            log "e" "Problem installing uStreamer, check the logs and try again"
            exit 1 
        fi          
    fi
}


## Function used to log information on the screen:
function log () {
    if [ "$1" == "i" ] ; then
        status="${green}INFO${reset}"
    elif [ "$1" == "e" ]; then
        status="${red}ERROR${reset}"
    fi

    echo "$(date) - $status - $2 "

}

function usage() {
    echo "usage: $0"
}

function main () {
    CheckDistro
    CheckIfRoot
    CheckInternetConn
    InstallRequirements
    InstallUstreamer
}

while [[ $# -ge 1 ]]
do
    key="$1"
	
    case $key in
    -h|--help)
        usage
        exit 0
        ;;
    *)
        (>&2 echo "unknown option: $key")
        usage
        exit 1
        ;;
    esac
    shift # past argument or value
done

## Do main:
main