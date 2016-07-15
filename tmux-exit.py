#!/bin/python

import argparse
import shlex
import subprocess


def main():

    parser = argparse.ArgumentParser(
        description='Exits properly the tmux session.')
    parser.add_argument('session', help='will try to exit the session. Implemented: hack')

    args = parser.parse_args()

    if args.session in SESSIONS:
        session_name = args.session
        session_fn = SESSIONS[session_name]
    else:
        raise Exception('No such session is implemented.')

    output, _ = call_command('tmux list-sessions')
    if session_name in str(output):
        session_fn()
        call_command('tmux kill-session -t {0}'.format(session_name))
    else:
        print("There isn't an opened {0} session.".format(session_name))


def hack():

    command_list = [
        "tmux send-keys -t weechat '/exit' enter",
    ]

    for command in command_list:
        output, _ = call_command(command)

# Implemented sessions

SESSIONS = {
    'hack': hack,
}

def call_command(command):
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=False,)
    return process.communicate()


if __name__ == '__main__':
    main()

