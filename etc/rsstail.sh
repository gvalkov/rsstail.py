
# automatically generated bash completion for rsstail.py
# http://github.com/gvalkov/rsstail.py

_rsstail() {
    local cur prev opts

    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="--verbose --version --help --help-format --interval --iterations --initial --newer --bytes --reverse --striphtml --nofail --timestamp --title --url --desc --pubdate --author --comments --no-heading --time-format --format -v -V -h -x -i -e -n -w -b -r -s -o -t -l -u -d -p -a -c -g -m -f"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

complete -F _rsstail rsstail

# vim: ft=sh:
