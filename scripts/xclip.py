# Wrapper for `xclip` command

from enum import StrEnum
from subprocess import Popen, PIPE


class Selection(StrEnum):
    PRIMARY = 'primary'
    SECONDARY = 'secondary'
    CLIPBOARD = 'clipboard'


def get_selection_text(selection: Selection=Selection.PRIMARY) -> str:
    """ Returns the text from the selection or clipboard. """
    with Popen(['xclip', '-out', '-selection', selection], stdout=PIPE, stderr=PIPE) as process:
        out, err = process.communicate()
        if process.returncode == 0:
            return out.decode('utf-8')
        else:
            return '(error)'
