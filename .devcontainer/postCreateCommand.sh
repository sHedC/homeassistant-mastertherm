#!/bin/bash
if [ ! -f ./local.env ]; then
  cp ./.devcontainer/configuration-template.yaml ./.devcontainer/configuration.yaml
fi

container install

if [ ! ${REQUIREMENTS_TXT} == "none" ]; then
    pip3 install --user -r requirements_${REQUIREMENTS_TXT}.txt
fi
