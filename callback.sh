#!/usr/bin/env bash

IP=192.168.1.172
USER=michong
PASSWORD=michong
TARGET=im

for i in `seq -w 0 23`; do
    DIR_PATH=`date +%Y/%m/%d`
    FILENAME=`date +%Y%m%d`${i}
    echo --ftp-password=xxx ftp://${USER}@${IP}/yuechang_log/${DIR_PATH}/${TARGET}-${FILENAME}
done
