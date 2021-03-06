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


function AddDcmUser() {
    log "i" "Adding dcm user"
    useradd -r dcm
    usermod -aG video dcm
    usermod -aG sudo dcm
    echo -e "dcm\ndcm" | (passwd --stdin dcm)
    usermod dcm -s /bin/bash



    log "i" "Adding sudoers rule"
    echo "# Sudoers configuration for Date Center Mamager" >> /etc/sudoers
    echo "dcm ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

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

function AddSystemdUstreamer () {
    log "i" "Adding uStreamer to systemd"
    ver=$(/usr/bin/ustreamer/ustreamer -v)
    if [ "$?" == "0" ]; then
        log "i" "uStreamer is installed on on version $ver"
    else
        log "e" "uStreamer is not installed, install it and try again"
        exit 1 
    fi 

    if [ -d "/etc/systemd/system/ustreamer@.service" ]; then
        log "i" "uStreamer already in systemd services, skipping configuration"
        return 0
    fi

    log "i" "Adding ustreamer to systemd"

    cat << EOF > /etc/systemd/system/ustreamer@.service
[Unit]
Description=uStreamer servicemói
After=network.target
[Service]
Environment="SCRIPT_ARGS=%I"
User=dcm
ExecStart=/usr/bin/ustreamer/ustreamer --log-level 0 --device-timeout=8 --resolution 1920x1080 --host=0.0.0.0  --process-name-prefix ustreamer-%I --device /dev/video%I--port=810%I
[Install]
WantedBy=multi-user.target
EOF

    systemctl daemon-reload
    #sudo systemctl enable ustreamer@.service
    #sudo systemctl enable ustreamer@0.service
    #sudo systemctl start ustreamer@0.service

}

function InstallDocker () {
    log "i" "Starting Docker installation"

    checkInstraled=$(dpkg -l | grep docker-ce | wc -l)
    if [ "$checkInstraled" != "0" ]; then
        log "i" "docker already installed, skipping docker installation"
        return 0
    else 
        wget -qO- https://get.docker.com/ | sh
    fi

    apt --yes install docker-compose
    if [ "$?" == "0" ]; then
        log "i" "docker-compose successfully installed"
    else
        log "e" "error installing docker-compose, check the logs and try again"
        exit 1 
    fi  

} 

function InstanciateKeycloakPostgres () {
    log "i" "Starting Keycloak and Postgres instanciation on Docker"

    checkKeycloakRunning=$(docker ps --filter "name=keycloak" --format '{{.Names}}' | wc -l)
    if [ "$checkKeycloakRunning" != "0" ]; then
        log "i" "keycloak container ir already running, skiping."
    else
        docker-compose -f ./containers/keycloak-postgres.yml up -d
        docker cp ./packages/dcm-theme/ containers_keycloak_1:/opt/jboss/keycloak/themes
        # script to create dcm database
        log "i" "Creating user and DB to store servers list"
        docker cp ./containers/dcm_db_create.sh containers_postgres_1:/docker-entrypoint-initdb.d/
        docker exec -i -t containers_postgres_1 bash /docker-entrypoint-initdb.d/dcm_db_create.sh
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

# Teste later, not tested
function AddUserPermissions () {
    user add dcm
    ./scripts/setSerialPermissions.sh dcm
}

#function ConfigureNetplan() {
#    chmod 666 /etc/netplan/01-netcfg.yaml
#}

function InstallWebServer () {
    log "i" "Instaling Python requirements"
    apt install python3
    apt install python3-venv

    log "i" "Instaling Apache2"
    apt install -y apache2
    log "i" "Creating firewall rules"
    ufw allow 'Apache'
    systemctl status apache2


    log "i" "Instaling Apache requirements"
    apt install -y libapache2-mod-wsgi python-dev
    apt install -y libapache2-mod-wsgi libapache2-mod-wsgi-py3 python-dev


    log "i" "Configuring Web App"
    mkdir -p /var/www/dcmweb/
    python3 -m venv /var/www/dcmweb/env && . /var/www/dcmweb/env/bin/activate
    python -m pip install --upgrade pip
    pip install -r dcmweb/requirements.txt

    log "i" "Configuring WSGI"

cat << EOF > /etc/apache2/sites-available/dcmweb.conf
WSGIPythonHome /var/www/dcmweb/env
WSGIPythonPath /var/www/



<VirtualHost *:80>
    ServerName 192.168.1.2
    ServerAdmin email@mywebsite.com
    #WSGIScriptAlias /dcmweb /home/ewerton/flask-test/wsgi.py
    WSGIScriptAlias / /var/www/wsgi.py
    #WSGIDaemonProcess user=root group=root processes=1 threads=1

   
#Alias /dcmweb /home/ewerton/flask-test/oi.html  
   <Directory /var/www/dcmweb/>
        #Order allow,deny
        #Allow from all
        Require all granted	
    </Directory>
    Alias /static /var/www/dcmweb/static
    <Directory /var/www/dcmweb/static/>
	Require all granted
    </Directory>
    ErrorLog ${APACHE_LOG_DIR}/error.log
    LogLevel warn
    CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

EOF
    cp -r dcmweb/dcmweb/* /var/www/dcmweb/
    cd /var/www/dcmweb/ a2ensite dcmweb
    systemctl reload apache2

    log "i" "Seting permissions"
    usermod -a -G tty www-data
    usermod -a -G dialout www-data



    cat << EOF > /var/www/dcmweb/dcmweb.wsgi
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/dcmweb/")

from dcmweb import app as application
application.secret_key = 'Add your secret key'
EOF

    systemctl reload apache2

}





function DoMain () {
    CheckDistro
    CheckIfRoot
    CheckInternetConn
    InstallRequirements
    AddDcmUser
    InstallUstreamer
    AddSystemdUstreamer
    InstallDocker
    InstanciateKeycloakPostgres
    AddUserPermissions
    ConfigureNetplan
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
DoMain
