#!/usr/bin/env python
# encoding: utf-8

'''Generate bash/zsh completion files for rsstail.'''

from sys import argv, stdout, exit
from rsstail.main import parseopt


usage = 'compgen.py bash|zsh > completion.sh\n'

if len(argv) == 1 or argv[1] not in ('zsh', 'bash'):
    stdout.write(usage) ; exit(1)

# get all options from all option groups
parser = parseopt()[0]
options = sum([i.option_list for i in parser.option_groups], [])


zsh_tmpl = '''\
#compdef rsstail

# automatically generated zsh completion for rsstail.py
# http://github.com/gvalkov/rsstail.py

_arguments -s -S \\
%s
&& ret=0

# vim: ft=zsh:
'''

bash_tmpl = '''\
# automatically generated bash completion for rsstail.py
# http://github.com/gvalkov/rsstail.py

_rsstail() {
    local cur prev opts
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    opts="%s"

    if [[ ${cur} == -* ]] ; then
        COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
        return 0
    fi
}

complete -F _rsstail rsstail

# vim: ft=bash:
'''


escapable = lambda c: c == '[' or c == ']' or c == '"'

def escape(s):
    res = [('\\%s' % c) if escapable(c) else c for c in s]
    return ''.join(res)


def zshopts():
    fmt = '"%s[%s]%s%s"'

    def getmetavar(action):
        if action.takes_value():
            return ':arg'
        else:
            return ''

    long_opts  = [(a._long_opts, getmetavar(a), a.help)  for a in options]
    short_opts = [(a._short_opts, getmetavar(a), a.help) for a in options]

    for op in (long_opts, short_opts):
        for o, m, h in op:
            yield fmt % (o[0], escape(h), m, '')


def bashopts():
    opts  = [a._long_opts  for a in options]
    opts += [a._short_opts for a in options]
    opts  = sum(opts, [])

    return ' '.join(opts)


if argv[1] == 'zsh':
    opts = ['%s \\' % i for i in zshopts()]
    stdout.write(zsh_tmpl % '\n'.join(opts))

elif argv[1] == 'bash':
    stdout.write(bash_tmpl % bashopts())
