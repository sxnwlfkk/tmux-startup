#!/bin/python

import argparse
import shlex
import subprocess


# Constants and long docstrings
DESC = """Something"""


def main():

    parser = argparse.ArgumentParser(description=DESC)

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-s', '--start', action='store_true')
    group.add_argument('-e', '--exit', action='store_true')

    parser.add_argument('session', choices=['hack', 'work', 'wargame'],
                        help='Will use this predefined session. Implemented: hack, work, wargame')

    args = parser.parse_args()

    if args.start == True and args.session:
        tm_start(args.session)
    if args.exit == True and args.session:
        tm_exit(args.session)


#############
# Functions #
#############


def tm_start(session):

    def hack():

        command_list = [
            "tmux new -d",
            "tmux new-session -s hack -n weechat -d",
            "tmux send-keys -t weechat 'weechat' enter",
            "tmux neww -n htop",
            "tmux send-keys -t htop 'htop' enter",
            "tmux neww -n ranger",
            "tmux send-keys -t ranger 'ranger' enter",
            "tmux neww -n mail",
            "tmux send-keys -t mail 'alpine' enter",
            "tmux neww -n news",
            "tmux send-keys -t news 'newsbeuter' enter",
            "tmux neww -n calenda",
            "tmux send-keys -t calenda 'calcurse' enter",
            "tmux neww -n zsh",
            "tmux send-keys -t zsh 'fortune | cowthink -f skeleton | lolcat' enter",
            "tmux attach -t hack",
       ]

        for command in command_list:
            output, _ = call_command(command)

    def work():

        command_list = [
            "tmux new -d",
            "tmux new-session -s work -n ranger -d",
            "tmux send-keys -t ranger 'ranger' enter",
            "tmux neww -n zsh",
            "tmux send-keys -t zsh 'fortune | cowthink -f skeleton | lolcat' enter",
            "tmux attach -t work",
        ]

        for command in command_list:
            output, _ = call_command(command)


    def wargame():

        command_list = [
            "tmux new -d",
            "tmux new-session -s wargame -n ssh -d",
            "tmux send-keys -t wargame 'fortune | cowthink -f skeleton | lolcat' enter",
            "tmux neww -n vim",
            "tmux send-keys -t vim 'vim' enter",
            "tmux neww -n man",
            "tmux attach -t wargame"
        ]

        for command in command_list:
            output, _ = call_command(command)


    # Global variable for implemented session functions. Has to be after functions.
    SESSIONS = {
        'hack': hack,
        'work': work,
        'wargame': wargame,
    }

    session_fn = SESSIONS[session]

    output, _ = call_command('tmux list-sessions')
    if session in str(output):
        call_command('tmux attach -t ' + session)
    else:
        session_fn()


def tm_exit(session):

    def hack():

        command_list = [
            "tmux send-keys -t weechat '/exit' enter",
        ]

        for command in command_list:
            output, _ = call_command(command)

    def work():
        pass

    # Implemented sessions

    SESSIONS = {
        'hack': hack,
        'work': work,
    }

    session_fn = SESSIONS[session]

    output, _ = call_command('tmux list-sessions')
    if session in str(output):
        session_fn()
        call_command('tmux kill-session -t {0}'.format(session))
    else:
        print("There isn't an opened {0} session.".format(session))


def call_command(command):
    process = subprocess.Popen(shlex.split(command),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=False,)

    return process.communicate()


if __name__ == '__main__':
    main()
