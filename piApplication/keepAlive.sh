#! /bin/bash

case "$(pidof python HepGrow.py | wc -l)" in

0)  echo "Restarting HepGrow:     $(date)" >> /var/log/hepgrow.txt
    python3 /etc/hepgrow/hepgrow.py &
    ;;
1)  # all ok
    ;;
*)  echo "Removed double HepGrow: $(date)" >> /var/log/hepgrow.txt
    kill $(pidof python HepGrow.py | awk '{print $1}')
    ;;
esac