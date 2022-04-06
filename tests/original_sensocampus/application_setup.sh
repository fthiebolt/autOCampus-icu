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
echo -e "\n[Django] collect static files ..."
python3 manage.py collectstatic --no-input 2>&1
_ret=$?
[ ${_ret} -ne 0 ] && { echo -e "\nERROR code ${_ret} while running Django application collectstatic!" >&2 ; sleep 10; exit ${_ret}; }


# because supervisor wants tasks to last at least 1s ;)
sleep 1

exit 0



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

#python3 manage.py create_users --no-input 2>&1
#[ ${_ret} -ne 0 ] && { echo -e "\nERROR code ${_ret} while running Django application create_users!" >&2 ; sleep 10; exit ${_ret}; }



# [Server]
# Note: we're using exec in order to replace bash shell PID with runserver to enable
# it to receive the SIGTERM
echo -e "\n[Django] application server launch ..."
exec python3 manage.py runserver --noreload 0.0.0.0:8000 2>&1
_ret=$?
[ ${_ret} -ne 0 ] && { echo -e "\nERROR code ${_ret} while running Django application server!" >&2; exit ${_ret}; }


