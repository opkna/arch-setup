#!/bin/bash

DEFAULT_PROFILE_DIR="/usr/share/archiso/configs/releng"

set -e

cd $(dirname $0)

function verify_archiso {
    if [ ! -d $DEFAULT_PROFILE_DIR ] || [ ! command -v mkarchiso &>/dev/null ]; then
        echo "archiso is not installed"
        exit 1
    fi
}

function create_build_dir {
    if [ -d build ]; then
        if [ ! -f build/.arch-setup-build-dir ]; then
            echo "Unknown build dir"
            exit 1
        fi
        sudo rm -rf build
    fi

    mkdir build
    touch build/.arch-setup-build-dir
}

function create_profile {
    cp -R $DEFAULT_PROFILE_DIR build/profile
    cp assets/myarchinstall build/profile/airootfs/usr/local/bin/myarchinstall
    sed -i 's/file_permissions=(/file_permissions=(\n  ["\/usr\/local\/bin\/myarchinstall"]="0:0:755"/g' build/profile/profiledef.sh
}

function build_iso {
    sudo mkarchiso -v -w build/workdir -o build build/profile
}

verify_archiso
create_build_dir
create_profile
build_iso