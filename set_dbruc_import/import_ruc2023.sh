#!/bin/bash

# import of SET files for RUC equivalents - into accounting database
# by Klemens Häckel
# V 20210327
# run as root from within the directory with the ZIP files from SET

# call:
# script.sh tablename database


# must be root user
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

# initial parameter check
if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    echo "debe indicar nombre de tabla destino"
    echo "ejemplo: sh ./$0 set_ruclist_20190701"
    echo "opcional ademas la base de datos:"
    echo "ej.: sh ./$0 set_ruclist_import db_contabilidad"
    exit 1
fi


_db="conta"
_dbtable="conta"

# force desired database name
if [ $# -gt 1 ]
  then
    _db=$2
    echo "use database:"
    echo $2
fi

# force desired table name
if [ $# -gt 0 ]
  then
    _dbtable=$1
    echo "use table:"
    echo $1
fi

# check does target table exist ?

#mysql $_db -e "SELECT EXISTS(SELECT * FROM information_schema.tables WHERE table_schema = '$_db' AND table_name = '$1');"
#mysql $_db -e "SELECT 1 FROM $1;"
#mysql $_db -e "SHOW TABLES LIKE '$1';"

#ok check:
#mysql $_db -e "SELECT count(*) FROM information_schema.tables WHERE table_schema = '$_db' AND table_name = '$1';"
#mysql -N -s $_db -e "SELECT count(*) FROM information_schema.tables WHERE table_schema = '$_db' AND table_name = '$1';"

#if [ $(mysql -N -s $_db -e "SELECT count(*) FROM information_schema.tables WHERE table_schema = '$_db' AND table_name = '$1';") -eq 0 ]
if [ $(mysql -N -s $_db -e "SELECT count(*) FROM information_schema.tables WHERE table_schema = '$_db' AND table_name = '$_dbtable';") -eq 0 ]
  then
    echo "target table $_dbtable not found in database $_db"
    exit 2
fi


#unzip files downloaded from SET
for i in `ls *.zip` ; 
do 
	echo $i;
	unzip $i ; 
done


# immport individual files to database

# mysql conta < do_sql.txt 
for i in `ls ruc*.txt` ; 
do 
	#echo $PWD/$i ; 
	# mysql conta < do_sql.txt
	# mysql conta < do_sql.txt
	# pending
	# pre: vaccuum table
	# post: internal updates sp_ - summary log
	#echo "LOAD DATA LOCAL INFILE '$PWD/$i' INTO TABLE $1 FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';";
	#mysql $_db -e "LOAD DATA LOCAL INFILE '$PWD/$i' INTO TABLE $1 FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';"
	echo "LOAD DATA LOCAL INFILE '$PWD/$i' INTO TABLE $_dbtable FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';";
	mysql $_db -e "LOAD DATA LOCAL INFILE '$PWD/$i' INTO TABLE $_dbtable FIELDS TERMINATED BY '|' LINES TERMINATED BY '\n';"
	
done
