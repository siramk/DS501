#!/bin/zsh

set -e
set -x

ACTION=$1
shift 
PARAMS=$*

SCRIPT_DIR="$(cd "$( dirname "${(%):-%N}" )" && pwd)"
cd $SCRIPT_DIR

if [ -f /.dockerenv ]; then
    echo "Cannot run $0 inside a docker container"
    exit 2
fi

setopt shwordsplit
COMPOSE='docker-compose -f docker-compose.yml'



usage() {
  PROG=`basename $0`
  echo "$PROG [<options>]"
  echo "    build - Build docker containers"
  echo "    console - Build and connect to console"
  echo "    console_only - Connect to console"
  echo "    test - Run and test within container"
  echo "    run [<command>] - Run and connect to container"
  echo "    start - Start docker containers"
  echo "    stop - Start docker containers"
  echo "    restart - restart docker containers"
  echo "    rm - Remove docker containers"
  echo "    logs [<args>] - show logs of container"
  echo "    ports - show hosts and posts"
}

docker_build() {
  local service=$1
  $COMPOSE build $service
}

docker_up() {
  local service=$1
  docker_build $service
  $COMPOSE up -d --scale authorizer=3 $service
}

docker_start() {
  local service=$1
  $COMPOSE start $service
}

docker_stop() {
  local service=$1
  $COMPOSE stop $service
}

docker_restart() {
  local service=$1
  $COMPOSE restart $service
}

docker_run() {
  local service=$1
  shift
  local cmd=$@
  docker_build $service
  $COMPOSE run -p 5000:5000 $service ${=cmd}
}

_docker_test() {
  PARAM=$1
  set +e
  docker_console bash bin/test.sh  $PARAM
  local result=$?
  set -e
  if [ $result -ne 0 ]; then
      echo "ERROR: $PARAMS failed"
      docker_logs '*' '--tail=10'
      echo "ERROR: $PARAMS failed"
      exit $result
  fi
}

docker_unittest() {
    _docker_test unittest
}

docker_integtest() {
    _docker_test integtest
}

docker_deploy() {
  docker_console bash bin/deploy.sh -e $PARAMS
}

docker_console() { 
  local args=$@
  docker_up
  docker_console_only ${=args}
}

docker_console_only() {
  local cmd=${@:-/bin/bash}
  if [ -z "$CI" ];then
    touch $SCRIPT_DIR/python/scripts/bash_history
  fi
  docker_run python ${=cmd}
}


docker_ps() {
  $COMPOSE ps
}

docker_rm() {
  local service=$1
  docker_stop $1
  $COMPOSE rm -f -v $service
}

docker_logs() {
  local service=$1
  local args='-f --tail=100'
  if [ ! -z "$service" ]; then
    shift
    args=$@
  fi
  if [ $service = '*' ];then
      unset service
  fi
  $COMPOSE logs ${=args} $service
}

docker_ports() {
  for c in `$COMPOSE ps -q`; do
    name=`docker inspect --format='{{index .Config.Labels "com.docker.compose.service"}}' $c`
    IFS=':' read -A ports <<< `docker inspect --format='{{range $p, $conf := .Config.ExposedPorts}}{{$p}}:{{end}}' $c | grep 'tcp' | sed -E 's/[^0-9:]//g'`
    for port in $ports; do
      echo "$name:$port"
    done
  done
}



case "x$ACTION" in 
  xbuild|xup|xconsole|xconsole_only|xunittest|xintegtest|xdeploy|xrun|xstart|xstop|xrestart|xrm|xps|xlogs|xports)
    docker_${ACTION} ${=PARAMS}
      ;;
  *) usage
    exit 1
    ;;
esac
