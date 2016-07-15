#!/bin/python

import argparse
import shlex
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description='Starts tmux with predefined arguments. If the session with the argument\'s name is live, it attaches itself to the session, otherwise makes a new one.')

    parser.add_argument('session', help='will use this predefined session. Implemented: hack')

    args = parser.parse_args()

    if args.session in SESSIONS:
        session_name = args.session
        session_fn = SESSIONS[session_name]
    else:
        raise Exception("No such session is implemented.")

    output, _ = call_command('tmux list-sessions')
    if session_name in str(output):
        call_command('tmux attach -t ' + session_name)
    else:
        session_fn()


def hack():

    command_list = [
        "tmux new -d",
        "tmux new-session -s hack -n weechat -d",
        "tmux send-keys -t weechat 'weechat' enter",
        "tmux neww -n htop",
        "tmux send-keys -t htop 'htop' enter",
        "tmux neww -n ranger",
        "tmux send-keys -t ranger 'ranger' enter",
        "tmux neww -n zsh",
        "tmux send-keys -t zsh 'fortune | cowthink -f skeleton | lolcat' enter",
        "tmux attach -t hack",
   ]

    #hack_path = "/home/cs/mysrc/tmux-startup/tmux-hack"
    #output, _ = call_command("tmux new -d")
    #call_command(hack_path)

    for command in command_list:
        output, _ = call_command(command)

# Global variable for implemented session functions. Has to be after functions.
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
