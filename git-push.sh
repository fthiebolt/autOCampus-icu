#!/bin/bash
#
# Simple helper script ;)
#

if [ "$#" == "0" ]; then
    msg='update'
else
    msg="$@"
fi

set -x

#git remote set-url origin git@github.com:fthiebolt/autOCampus-icu.git
git add --all
git commit -a -m "${msg}"
git push

