import enum
from flask import flash


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class MsgType(enum.Enum):
    HEADER = 1
    OKBLUE = 2
    OKCYAN = 3
    OKGREEN = 4
    WARNING = 5
    FAIL = 6
    ENDC = 7
    BOLD = 8
    UNDERLINE = 9





def prettyprint(msg_text, msg_type):
    if msg_type == MsgType.HEADER:
        flash(f"{msg_text}")
    elif msg_type == MsgType.OKBLUE:
        flash(f"{msg_text}")
    elif msg_type == MsgType.OKCYAN:
        flash(f"{msg_text}")
    elif msg_type == MsgType.OKGREEN:
        flash(f"{msg_text}")
    elif msg_type == MsgType.WARNING:
        flash(f"{msg_text}")
    elif msg_type == MsgType.FAIL:
        flash(f"{msg_text}")
    elif msg_type == MsgType.BOLD:
        flash(f"{msg_text}")
    elif msg_type == MsgType.UNDERLINE:
        flash(f"{msg_text}")
