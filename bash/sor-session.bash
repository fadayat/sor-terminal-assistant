# Record each VTE Bash terminal separately for the `sor` command.
if [[ $- == *i* ]] \
    && [[ -t 0 && -t 1 ]] \
    && [[ -n ${VTE_VERSION:-} ]] \
    && [[ -z ${SOR_SESSION_RECORDING:-} ]]; then
    exec "$HOME/.local/bin/sor-session-recorder"
fi
