#! /bin/bash

if [[ -z "${1}" ]]; then
    NAME="wallabot_sqlite"
else
    NAME=${1}
fi

scrapy crawl wallabot -O /data/${NAME}.csv -t csv