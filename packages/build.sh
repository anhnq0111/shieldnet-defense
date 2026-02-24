#!/bin/bash

# ShieldnetDefend package builder
# Copyright (C) 2015, ShieldnetDefend Inc.
#
# This program is a free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.
set -e

build_directories() {
  local build_folder=$1
  local shieldnet_defend_dir="$2"
  local future="$3"

  mkdir -p "${build_folder}"
  shieldnet_defend_version=$(awk -F'"' '/"version"[ \t]*:/ {print $4}' shieldnet*/VERSION.json)

  if [[ "$future" == "yes" ]]; then
    shieldnet_defend_version="$(future_version "$build_folder" "$shieldnet_defend_dir" $shieldnet_defend_version)"
    source_dir="${build_folder}/shieldnet-defend-${BUILD_TARGET}-${shieldnet_defend_version}"
  else
    package_name="shieldnet-defend-${BUILD_TARGET}-${shieldnet_defend_version}"
    source_dir="${build_folder}/${package_name}"
    cp -R $shieldnet_defend_dir "$source_dir"
  fi
  echo "$source_dir"
}

# Function to handle future version
future_version() {
  local build_folder="$1"
  local shieldnet_defend_dir="$2"
  local base_version="$3"

  specs_path="$(find $shieldnet_defend_dir -name SPECS|grep $SYSTEM)"

  local major=$(echo "$base_version" | cut -dv -f2 | cut -d. -f1)
  local minor=$(echo "$base_version" | cut -d. -f2)
  local version="${major}.30.0"
  local old_name="shieldnet-defend-${BUILD_TARGET}-${base_version}"
  local new_name=shieldnet-defend-${BUILD_TARGET}-${version}

  local new_shieldnet_defend_dir="${build_folder}/${new_name}"
  cp -R ${shieldnet_defend_dir} "$new_shieldnet_defend_dir"
  find "$new_shieldnet_defend_dir" "${specs_path}" \( -name "*VERSION*" -o -name "*changelog*" \
        -o -name "*.spec" \) -exec sed -i "s/${base_version}/${version}/g" {} \;
  sed -i "s/\$(VERSION)/${major}.${minor}/g" "$new_shieldnet_defend_dir/src/Makefile"
  sed -i "s/${base_version}/${version}/g" $new_shieldnet_defend_dir/src/init/shieldnet-defend-{server,client,local}.sh
  echo "$version"
}

# Function to generate checksum and move files
post_process() {
  local file_path="$1"
  local checksum_flag="$2"
  local source_flag="$3"

  if [[ "$checksum_flag" == "yes" ]]; then
    sha512sum "$file_path" > /var/local/checksum/$(basename "$file_path").sha512
  fi

  if [[ "$source_flag" == "yes" ]]; then
    mv "$file_path" /var/local/shieldnetdefend
  fi
}

# Main script body

# Script parameters
export REVISION="$1"
export JOBS="$2"
debug="$3"
checksum="$4"
future="$5"
legacy="$6"
src="$7"

build_dir="/build_shieldnet_defend"

source helper_function.sh

if [ -n "${SHIELDNET_DEFEND_VERBOSE}" ]; then
  set -x
fi

# Download source code if it is not shared from the local host
if [ ! -d "/shieldnet-defend-local-src" ] ; then
    curl -sL https://github.com/shieldnetdefend/shieldnetdefend/tarball/${SHIELDNET_DEFEND_BRANCH} | tar zx
    short_commit_hash="$(curl -s https://api.github.com/repos/shieldnetdefend/shieldnetdefend/commits/${SHIELDNET_DEFEND_BRANCH} \
                          | grep '"sha"' | head -n 1| cut -d '"' -f 4 | cut -c 1-7)"
else
    if [ "${legacy}" = "no" ]; then
      short_commit_hash="$(cd /shieldnet-defend-local-src && git rev-parse --short=7 HEAD)"
    else
      # Git package is not available in the CentOS 5 repositories.
      head=$(cat /shieldnet-defend-local-src/.git/HEAD)
      hash_commit=$(echo "$head" | grep "ref: " >/dev/null && cat /shieldnet-defend-local-src/.git/$(echo $head | cut -d' ' -f2) || echo $head)
      short_commit_hash="$(cut -c 1-7 <<< $hash_commit)"
    fi
fi

# Build directories
source_dir=$(build_directories "$build_dir/${BUILD_TARGET}" "shieldnet*" $future)

shieldnet_defend_version=$(awk -F'"' '/"version"[ \t]*:/ {print $4}' $source_dir/VERSION.json)
# TODO: Improve how we handle package_name
# Changing the "-" to "_" between target and version breaks the convention for RPM or DEB packages.
# For now, I added extra code that fixes it.
package_name="shieldnet-defend-${BUILD_TARGET}-${shieldnet_defend_version}"
specs_path="$(find $source_dir -name SPECS|grep $SYSTEM)"

setup_build "$source_dir" "$specs_path" "$build_dir" "$package_name" "$debug"

set_debug $debug $sources_dir

# Installing build dependencies
cd $sources_dir
build_deps $legacy
build_package $package_name $debug "$short_commit_hash" "$shieldnet_defend_version"

# Post-processing
get_package_and_checksum $shieldnet_defend_version $short_commit_hash $src
