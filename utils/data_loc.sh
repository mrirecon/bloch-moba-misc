#!/bin/bash

set +u

REPO_NAME=phd_thesis_nscho

REPO2_NAME=bloch-moba

if [ ! -d ${DATA_ARCHIVE}/${REPO_NAME} ] ; then
	FOLDER=$(dirname $(readlink -f $BASH_SOURCE))
	DATA_LOC=$(realpath "$FOLDER"/../data)
	DATA_LOC2=$(realpath "$FOLDER"/../data)
else
	DATA_LOC=${DATA_ARCHIVE}/${REPO_NAME}
	DATA_LOC2=${DATA_ARCHIVE}/${REPO2_NAME}
fi

set -u
export DATA_LOC
export DATA_LOC2
