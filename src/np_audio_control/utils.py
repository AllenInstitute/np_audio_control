import doctest
import pathlib
import subprocess
import sys
from typing import Literal

import np_config
import np_logging

logger = np_logging.get_logger(__name__)

CONFIG: dict = np_config.fetch(
    f'/projects/{__package__ or pathlib.Path(__file__).parent.name}'
)
"""Package config dict with paths etc."""

STIM_HOSTS: dict[str, str] = CONFIG['stim_hosts']
"""Sam's dict of stim hosts: `NP3: w10DTSM118296, B1: wxvs-syslogic7`, etc."""

ON_WINDOWS: bool = 'win' in sys.platform
"""True if running on Windows."""

CREDENTIALS: dict[Literal['user', 'password'], str] = np_config.fetch(
    '/logins'
)['svc_neuropix']


def assert_cli_tool(executable: str) -> None:
    """Assert that `executable` can be found and used.

    >>> if ON_WINDOWS: assert_cli_tool("robocopy") == None
    True

    >>> assert_cli_tool("not-robocopy")
    Traceback (most recent call last):
    ...
    AssertionError

    """
    try:
        process = subprocess.run(
            [executable, '/?'],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except FileNotFoundError:
        if not ON_WINDOWS and executable == 'robocopy':
            raise AssertionError(
                f'robocopy is only available on Windows: running on {sys.platform}'
            )
        raise AssertionError(f'{executable!r} could not be found in PATH.')
    else:
        if process.returncode != 16:
            raise AssertionError(
                f'{executable!r} returned exit status {process.returncode}.'
            )


if __name__ == '__main__':
    doctest.testmod(verbose=True, optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
