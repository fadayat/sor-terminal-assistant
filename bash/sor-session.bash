# The recorder starts a child Bash with these paths in its environment.
if [[ $- == *i* ]] && [[ -n ${SOR_SESSION_RECORDING:-} ]] \
    && [[ -n ${SOR_SESSION_EVENT_HELPER:-} ]] \
    && [[ -n ${SOR_SESSION_EVENTS:-} ]] \
    && [[ -n ${SOR_SESSION_START_FILE:-} ]]; then
    __sor_finish_command() {
        local command_status=${1:-$?}
        local history_line command_text
        history_line=$(HISTTIMEFORMAT= builtin history 1)
        if [[ $history_line =~ ^[[:space:]]*[0-9]+[[:space:]]+(.*)$ ]]; then
            command_text=${BASH_REMATCH[1]}
            printf '%s' "$command_text" \
                | "$SOR_SESSION_EVENT_HELPER" finish "$command_status" "$PWD" \
                    >/dev/null 2>&1 || true
        fi
        return "$command_status"
    }

    # PS0 expands after Bash reads a command; its command text stays out of argv.
    PS0="${PS0:-}\$(\"$SOR_SESSION_EVENT_HELPER\" start >/dev/null 2>&1)"
    if declare -p PROMPT_COMMAND 2>/dev/null | grep -q '^declare -a'; then
        PROMPT_COMMAND=("__sor_finish_command \$?" "${PROMPT_COMMAND[@]}")
    elif [[ -n ${PROMPT_COMMAND:-} ]]; then
        PROMPT_COMMAND="__sor_finish_command \$?; ${PROMPT_COMMAND}"
    else
        PROMPT_COMMAND='__sor_finish_command $?'
    fi
elif [[ $- == *i* ]] \
    && [[ -t 0 && -t 1 ]] \
    && [[ -n ${VTE_VERSION:-} ]] \
    && [[ -z ${SOR_SESSION_RECORDING:-} ]]; then
    exec "$HOME/.local/bin/sor-session-recorder"
fi
