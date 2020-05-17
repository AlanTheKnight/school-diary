#!/bin/bash

dashboard_name=''

read -p "Enter a dashboard name > " dashboard_name
cd school_diary/templates/
if [[ ! -d ./$dashboard_name ]]; then
    mkdir $dashboard_name
    cd $dashboard_name
    cp ../../../dashboard_example/dashboard_templates/dashboard.html ./dashboard.html
    cp ../../../dashboard_example/dashboard_templates/delete.html ./delete.html
    cp ../../../dashboard_example/dashboard_templates/create.html ./create.html
else
    echo "Panel with chosen name already exists."
    exit
fi
