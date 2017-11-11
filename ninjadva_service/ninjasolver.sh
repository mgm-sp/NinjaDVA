#!/bin/sh

usage(){
	echo "usage: `basename $0` -r <solve-url> -i <ip-address> -c <category> -s <state> [-m message]"
	echo "e.g.: `basename $0` -r http://dashboard.mgmsp-lab.com/solve_srv.cgi -i 172.23.42.137 -c some_challenge -s 7 -m 'Ben solved something'"
	exit 1
}

while getopts r:i:c:s:m: option; do
	case "$option" in
		r) REMOTE=$OPTARG ;;
		i) IP=$OPTARG ;;
		c) CAT=$OPTARG;;
		s) STATE=$OPTARG;;
		m) MESSAGE=$OPTARG;;
		\?) usage ;;
	esac
done
shift `expr $OPTIND - 1`

curl -s \
	--data-urlencode "ip_addr=$IP" \
	--data-urlencode "state=$STATE" \
	--data-urlencode "category=$CAT" \
	--data-urlencode "comment=$MESSAGE" \
	$REMOTE
