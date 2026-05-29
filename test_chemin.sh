#!/bin/bash
#echo $1
chemin=`which $1`
#echo $chemin
if [[ "$chemin" == /* ]]
then
    echo "Existe à $chemin";
else
    echo "N'existe pas";
fi
