#!/bin/bash
#
# Django application setup
#
# Thiebolt F.   Oct.17
#   only undertaking basic setup ops in an automated way
#
# Thiebolt F.   Mar.16
#


#
# DJANGO setup static files
#
echo -e "\n[static] collect static files ..."
python3 manage.py collectstatic --no-input 2>&1
_ret=$?
[ ${_ret} -ne 0 ] && { echo -e "\nERROR code ${_ret} while running Django application collectstatic!" >&2 ; sleep 10; exit ${_ret}; }


#
# DJANGO superuser
# ... create if it does not already exists
cat <<EOF | python3 manage.py shell
import sys
from django.contrib.auth.models import User
if( not User.objects.filter(username="admin").exists() ):
    User.objects.create_superuser("admin", "thiebolt@irit.fr", "admin@neOCom")
    # superuser created
    sys.exit(0)
sys.exit(1)
EOF
[ $? -eq 0 ] && { echo -e "\n[users] superuser created"; }


#
# DJANGO 'sqlite' backend detection
cat <<EOF | python3 manage.py shell
import sys
from django.db import connection
if( "sqlite" in connection.vendor ):
    sys.exit(0)
else:
    sys.exit(1)
EOF
if [ $? -ne 0 ]; then
    echo -e "\n[database] not an sqlite database ... thus it's over :)"
    # because supervisor wants tasks to last at least 1s ;)
    sleep 1
    exit 0
else
    echo -e "\n[database] SQLite detected ... continuing ..."
fi



# 
# DATABASE modification related tools
#
echo -e "\n[Django] application migration ..."

python3 manage.py makemigrations --no-input 2>&1
_ret=$?
[ ${_ret} -ne 0 ] && { echo -e "\nERROR code ${_ret} while running Django application makemigrations!" >&2 ; sleep 10; exit ${_ret}; }

python3 manage.py migrate --no-input 2>&1
_ret=$?
[ ${_ret} -ne 0 ] && { echo -e "\nERROR code ${_ret} while running Django application migrate!" >&2 ; sleep 10; exit ${_ret}; }



# because supervisor wants tasks to last at least 1s ;)
sleep 1

exit 0

