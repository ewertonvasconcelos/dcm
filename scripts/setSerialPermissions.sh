#!/bin/sh
echo ""
echo "******* Add User to dialout,tty, uucp, plugdev groups *******"
echo ""

sudo usermod -a -G tty $1
sudo usermod -a -G dialout $1
sudo usermod -a -G uucp $1
sudo usermod -a -G plugdev $1


acmrules () {

    echo ""
    echo "# Setting serial port rules"
    echo ""

    cat <<EOF
    "KERNEL="ttyUSB[0-9]*", TAG+="udev-acl", TAG+="uaccess", OWNER="$1"
   "KERNEL="ttyACM[0-9]*", TAG+="udev-acl", TAG+="uaccess", OWNER="$1"
EOF

}