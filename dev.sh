#!/bin/bash
RESTORE='\033[0m'
RED='\033[00;31m'
GREEN='\033[00;32m'
YELLOW='\e[0;33m'

HOST=freedomsponsors.org

# Pq ninguem merece ter que ficar decorando comando
# Instruções:
# 1) ". dev.sh"
# 2) "devhelp"
# 3) Seja feliz


workon freedomsponsors  # Muda isso pro nome do virtalenv do seu projeto

export PROJ_BASE="$(dirname ${BASH_SOURCE[0]})"
CD=$(pwd)
cd $PROJ_BASE
export PROJ_BASE=$(pwd)
cd $CD

#. ci/funcs.sh

function devhelp {
    echo -e "${GREEN}devhelp${RESTORE}           Imprime este ${RED}help${RESTORE}"
    echo -e ""
    echo -e "${GREEN}pytests${RESTORE}           Roda os ${RED}testes${RESTORE} python"
    echo -e ""
    echo -e "${GREEN}runflake8${RESTORE}         Roda os ${RED}PEP8${RESTORE} no python"
    echo -e ""
    echo -e "${GREEN}djangorun${RESTORE}         Sobe o backend ${RED}django${RESTORE}"
    echo -e ""
    echo -e "${GREEN}dkbuild${RESTORE}           Cria a imagem docker desse projeto"
    echo -e ""
    echo -e "${GREEN}fullbuild${RESTORE}         Faz a build de tudo"
    echo -e ""
    echo -e "${GREEN}pullfront${RESTORE}         Builda e \"puxa\" o codigo do front pra ca"
    echo -e ""
    echo -e "${GREEN}dkrun${RESTORE}             Sobe o projeto dockerizado com o nginx na porta 80"
    echo -e ""
    echo -e "${GREEN}dknginx${RESTORE}           Sobe um nginx na porta 80, redirecionando pra 8000/3000"
    echo -e ""
    echo -e ""
}

function pytests {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "./manage.py test core --parallel 4" "Testes python"
    exitcode=$?
    cd $CD
    return $exitcode
}

function djangorun {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "./manage.py runserver" "Servidor django"
    exitcode=$?
    cd $CD
    return $exitcode
}

function dkbuild {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "docker build -t frespo ." "Build docker image"
    exitcode=$?
    cd $CD
    return $exitcode
}

function fullbuild {
    CD=$(pwd)
    cd $PROJ_BASE
    ./manage.py collectstatic
    pullfront
    dkbuild
    exitcode=$?
    cd $CD
    return $exitcode
}

function dknginx {
    CD=$(pwd)
    cd $PROJ_BASE
    docker-compose -f docker/nginx.yaml up
    exitcode=$?
    cd $CD
    return $exitcode
}


function dkrun {
    CD=$(pwd)
    cd $PROJ_BASE
    docker-compose -f docker/docker-compose.yaml up
    exitcode=$?
    cd $CD
    return $exitcode
}

function runflake8 {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "flake8 ." "Rodar PEP8"
    exitcode=$?
    cd $CD
    return $exitcode
}

function sendcode {
    CD=$(pwd)
    cd $PROJ_BASE
    rsync -a --progress --delete --exclude=.git . ubuntu@$HOST:./www.freedomsponsors.org/
    exitcode=$?
    cd $CD
    return $exitcode
}

function echo_red {
    echo -e "\e[31m$1\e[0m";
}

function echo_green {
    echo -e "\e[32m$1\e[0m";
}

function echo_yellow {
    echo -e "${YELLOW}$1${RESTORE}";
}

function now_milis {
    date +%s%N | cut -b1-13
}

function dorun {
    cmd="$1"
    name="$2"
    echo ----------------------------------
    echo_green "STARTING $name ..."
    echo "$cmd"
    t1=$(now_milis)
    $cmd
    exitcode=$?
    t2=$(now_milis)
    delta_t=$(expr $t2 - $t1)
    if [ $exitcode == 0 ]
    then
        echo_green "FINISHED $name in $delta_t ms"
        echo ----------------------------------
    else
        echo_red "ERROR! $name (status: $exitcode, time: $delta_t ms)"
        echo ----------------------------------
        return $exitcode
    fi
}

echo_green "Bem vindo ao ambiente de desenv. do freedomsponsors:"
echo_green "Dica: autocomplete funciona pros comandos abaixo ;)"
echo_red   "------------------------------------------------------------------------"
devhelp
