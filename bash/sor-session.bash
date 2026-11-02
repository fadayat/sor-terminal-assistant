# The recorder starts a child Bash with these paths in its environment.
if [[ $- == *i* ]] && [[ -n ${SOR_SESSION_RECORDING:-} ]] \
    && [[ -n ${SOR_SESSION_EVENT_HELPER:-} ]] \
    && [[ -n ${SOR_SESSION_EVENTS:-} ]] \
    && [[ -n ${SOR_SESSION_START_FILE:-} ]]; then
    __sor_finish_command() {
        local command_status=${1:-$?}
        local history_line command_text command_id marker
        if [[ ${HISTCMD:-0} -gt ${__sor_last_histcmd:-0} ]]; then
            history_line=$(HISTTIMEFORMAT= builtin history 1)
        else
            history_line=
        fi
        __sor_last_histcmd=${HISTCMD:-0}
        if [[ $history_line =~ ^[[:space:]]*[0-9]+[[:space:]]+(.*)$ ]]; then
            command_text=${BASH_REMATCH[1]}
            command_id=$(printf '%s' "$command_text" \
                | "$SOR_SESSION_EVENT_HELPER" finish "$command_status" "$PWD" \
                    2>/dev/null) || command_id=
        else
            command_id=$("$SOR_SESSION_EVENT_HELPER" cancel 2>/dev/null) || command_id=
        fi
        if [[ $command_id =~ ^[A-Za-z0-9._:-]+$ ]]; then
            marker=$'\033]777;sor-end='"$command_id"$'\007'
            printf '%s' "$marker"
        fi
        return "$command_status"
    }

    __sor_last_histcmd=${HISTCMD:-0}
    __sor_start_marker() {
        local command_id
        command_id=$("$SOR_SESSION_EVENT_HELPER" start 2>/dev/null) || return 0
        if [[ $command_id =~ ^[A-Za-z0-9._:-]+$ ]]; then
            printf '\033]777;sor-start=%s\007' "$command_id"
        fi
    }

    # PS0 expands after Bash reads a command; the helper's text stays out of argv.
    PS0="${PS0:-}\$(__sor_start_marker)"
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
