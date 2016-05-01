#!/bin/sh

cd `dirname $0`
MYNAME=`basename $0`
SCRIPT_DIR="`pwd`"
if [ -d ../workflows ]; then
    cd ../workflows
    WORKFLOW_DIR="`pwd`"
else
    echo "workflow dir not found."
    exit 2
fi

WF_RGB="${WORKFLOW_DIR}/pdf2jpeg_rgb.workflow"

if [ $# -eq 0 ] ; then exit 0; fi

WORK_ID=$2
if [ ${WORK_ID:-X} = X ]; then WORK_ID=`uuidgen`; fi
LOGFILE=/tmp/${WORK_ID}/${MYNAME}.log
INFOFILE=/tmp/${WORK_ID}/${MYNAME}.output

if [ `file "$1" | awk -F: '{print $2}' | awk '$1 == "PDF"' | wc -l` -eq 1 ]; then
        echo "OK: $1 is PDF file." > $LOGFILE
else
        exit 0
fi

/usr/bin/automator -i "$1" "$WF_RGB" | tr -d '()'| sed s/,$//g |awk 'NF' > $INFOFILE
