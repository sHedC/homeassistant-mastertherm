#!/bin/bash
container install

if [ ! ${REQUIREMENTS_TXT} == "none" ]; then
    pip3 install --user -r requirements_${REQUIREMENTS_TXT}.txt
fi
