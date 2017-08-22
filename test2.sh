#!/bin/bash
IFS=","
while read f1 f2 f3 f4
do
a="$f1 -"`date +%F%T%N`
e="insert into alerts.status(Identifier,Summary,Node)values('$a', '$f3', '$f2' );"
f="go"
echo "$e">>"1.sql"
echo "$f">>"1.sql"
done < Test1.csv
cmd="nco_sql -server NCOMS_RK -user root -password 'access' < 1.sql";
bash -c "$cmd"
