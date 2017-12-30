#!/usr/bin/env bash

#export SECRET_KEY=''
export FLASK_CONFIG=''
if [[ $FLASK_CONFIG -eq 'production' ]]; then
    export DATABASE_URL='mysql+pymysql://user:password@hostname/database'
    export ACCESS_KEY_ID=''
    export ACCESS_KEY_SECRET=''
fi
#export DEV_DATABASE_URL=''
#export TEST_DATABASE_URL=''
