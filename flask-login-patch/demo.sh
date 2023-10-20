#!/usr/bin/env sh
set -euo pipefail
IFS=$'\n\t'

function log {
    echo == demo.sh == $@
}

if [ -d venv ]; then
    log "rm venv"
    rm -r venv
fi

# make venv
log "creating virtual environment"
python -m venv venv

# activate venv
log "activating virtual environment"
source venv/bin/activate

# upgrade pip
log "upgrading pip"
python -m pip install pip -U

# install flask-login
log "installing flask-login"
pip install flask-login

# get venv site package
log "get site packages path"
# NOTE
# - use or (||) true for compatibility with "strict mode" with commands having
#   an expected non-zero
# http://redsymbol.net/articles/unofficial-bash-strict-mode/#expect-nonzero-exit-status

sitepkgdir="$(python -c 'import site; print(site.getsitepackages()[0])')"
echo "${sitepkgdir}"

# == apply patch == #
#
# NOTES
# - patch created by:
#   `diff -ruN path/to/venv/flask_login path/to/cloned/repo/flask-login/flask_login`

log "applying patch for Flask 3.0"
# just following examples for this invocation
# feels goofy but diff/patch is very old
patch -d "${sitepkgdir}/flask_login" < flask-login.patch

log "done"
