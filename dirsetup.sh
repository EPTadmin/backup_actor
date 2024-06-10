#!/bin/bash

echo '📝 installing/updating cifs'
sudo apt-get install cifs-utils; 

echo '📝 creating/mounting the production data repo '
mkdir sync-origin;
sudo mount --bind ../actor_ldap  sync-origin;

echo '📝 creating/mounting the backup data repo [use the NTNU-username for kunde.it.ntnu.no]'
mkdir sync-dest;

read  -p "❔ what's the NTNU-username to use? " ntnu_user
sudo mount -t cifs -o uid=$USER,user=$ntnu_user,dir_mode=0700,file_mode=0700 //kunde.it.ntnu.no/ept-eksperimentell/indecol/USERS/Candy/actor-backup sync-dest;
