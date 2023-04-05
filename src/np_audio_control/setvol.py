from __future__ import annotations

import doctest
import functools
import logging
import pathlib
from typing import Any, Callable, Optional

import fabric
import np_logging

import np_audio_control.utils as utils

logging.getLogger('paramiko').setLevel(logging.WARNING)
logging.getLogger('invoke').setLevel(logging.WARNING)
logging.getLogger('fabric').setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

LOCAL_SETVOL = pathlib.Path(utils.CONFIG['setvol_path'])


connect: Callable = functools.partial(
    fabric.Connection,
    user=utils.CREDENTIALS['user'],
    connect_kwargs=dict(password=utils.CREDENTIALS['password']),
)
"""Fabric connection to a host (str, required input)."""


def test() -> None:
    raise AssertionError('Not implemented.')


def send_setvol_cmd(host: str, *args, hide_output=True) -> Any:
    """Run setvol command on host with `args`.

    >>> send_setvol_cmd(TEST_HOST, '?').exited # help
    0
    """
    command = f'"{LOCAL_SETVOL}" {" ".join(args)}'
    with connect(host) as ssh:
        logger.debug(
            'Sending command to %s via fabric as %s: %r',
            ssh.host,
            ssh.user,
            command,
        )
        result = ssh.run(
            command, hide=hide_output, warn=True
        )   # warn suppresses bad exit code error
        logger.debug('Return code: %s', result.return_code)
    return result


def add_device_name(
    cmds: list[str], device_name: Optional[str] = None
) -> None:
    """Add `device_name` to `cmds` in place,  if `device_name` is not None or empty."""
    if device_name:
        cmds.extend(['device', device_name])


def mute(host, device_name: Optional[str] = None) -> None:
    """Mute system audio on host.

    >>> mute(TEST_HOST)
    """
    cmds = ['mute']
    add_device_name(cmds, device_name)
    _ = send_setvol_cmd(host, *cmds)


def unmute(host, device_name: Optional[str] = None) -> None:
    """Unmute system audio on host.

    >>> unmute(TEST_HOST)
    """
    cmds = ['unmute']
    add_device_name(cmds, device_name)
    _ = send_setvol_cmd(host, *cmds)


def set_volume(
    volume: int | str, host: str, device_name: Optional[str] = None
) -> None:
    """Set system volume on host.

    >>> unmute(TEST_HOST)
    >>> set_volume(0, TEST_HOST)
    >>> get_volume(TEST_HOST)
    0
    """
    volume = int(volume)
    if not 0 <= volume <= 100:
        raise ValueError(f'`volume` must be between 0 and 100: {volume=}')
    cmds = [str(volume)]
    add_device_name(cmds, device_name)
    _ = send_setvol_cmd(host, *cmds)


def get_volume(host, device_name: Optional[str] = None) -> int:
    """Get current system volume on host.

    >>> unmute(TEST_HOST)
    >>> set_volume(0, TEST_HOST)
    >>> get_volume(TEST_HOST)
    0
    """
    cmds = ['report']
    add_device_name(cmds, device_name)
    result = send_setvol_cmd(host, *cmds)
    if 0 <= result.return_code <= 100:
        return result.return_code
    raise Exception(
        f'Unexpected return code: {result.return_code}', result.stderr
    )


if __name__ == '__main__':
    # TEST_HOST: str = utils.STIM_HOSTS['NP2']
    logger = np_logging.getLogger()
    doctest.testmod(verbose=True, optionflags=doctest.IGNORE_EXCEPTION_DETAIL)
