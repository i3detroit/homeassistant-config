#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")"

# shellcheck disable=SC2120
help () {
    # if arguments, print them
    [ $# == 0 ] || echo "$*"

  cat <<EOF
Usage: $(basename "${BASH_SOURCE[0]}") [OPTION]... [yaml configs]...
  update a bunch of tasmota devices via esphome config
Available options:
  -h, --help       display this help and exit
      --no-build   don't run esphome compile, assume it's already done
EOF

    # if args, exit 1 else exit 0
    [ $# == 0 ] || exit 1
    exit 0
}

msg() {
    echo >&2 -e "${1-}"
}

die() {
    local msg=$1
    local code=${2-1} # default exit status 1
    msg "$msg"
    exit "$code"
}

# getopt short options go together, long options have commas
TEMP=$(getopt -o h --long help,no-build -n "$0" -- "$@")
#shellcheck disable=SC2181
if [ $? != 0 ] ; then
    die "something wrong with getopt"
fi
eval set -- "$TEMP"

noBuild=false
while true ; do
    case "$1" in
        -h|--help) help; exit 0; shift ;;
        --no-build) noBuild=true; shift ;;
        --) shift ; break ;;
        *) die "issue parsing args, unexpected argument '$0'!" ;;
    esac
done


for f in $@; do \
    if [ "$noBuild" = false ]; then
	esphome compile $f
    fi
    name=${f/\.yaml/};
    bin=build/$name/.pioenvs/$name/firmware.bin
    ip=$(sed -n 's/\s*ip_address: \(.*\)/\1/p' $f)
    if [ -z "$ip" ] || [ "$ip" == "10.13.107.256" ]; then
	    die "No ip in $f"
    fi
    if [ ! -f "$bin" ]; then
	    die "No bin for $f: $bin"
    fi

    msg "flashing $name at $ip with $bin..."
    response=$(curl "http://$ip/u2" \
	    -X 'POST' \
	    -F "u2=@$bin")
    if [[ "$response" == *"Success"* ]]; then
	    msg "success"
    else
	    msg "FAIL"
    fi
done
