#!/usr/bin/env python3

# noinspection PyUnresolvedReferences
"""
Capture details of the current machine and runtime.

<h4>Usage:</h4>

```
python3 utilities/runtime.py OUTPUT_DIR
```

Arguments:
    OUTPUT_DIR (str): Directory where to write the output.
"""

import platform
import subprocess
import sys
from datetime import datetime
from os import makedirs
from os.path import join, exists
from typing import Any

# noinspection PyPackageRequirements
import psutil


def _size(bytes_, suffix="B") -> str:
    """Scales bytes to appropriate format.

    Example:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'

    Arguments:
          bytes_ : number of bytes
          suffix: "bytes" unit char [default: B]

    Returns:
          Formatted _size expression.
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_ < factor:
            return f"{bytes_:.2f}{unit}{suffix}"
        bytes_ /= factor


def _machine_details() -> dict[str, Any]:
    """Capture details of current machine."""
    uname, mem = platform.uname(), psutil.virtual_memory()
    return dict(
        operating_system=uname.system,
        operating_system_release=uname.release,
        operating_system_version=uname.version,
        machine_architecture=uname.machine,
        processor=uname.processor,
        cpu_physical_cores=psutil.cpu_count(logical=False),
        cpu_total_cores=psutil.cpu_count(logical=True),
        cpu_usage_per_core=psutil.cpu_percent(
            percpu=True, interval=1), **_cpu_freq(),
        cpu_total_usage=psutil.cpu_percent(),
        virtual_mem_total_size=_size(mem.total),
        virtual_mem_available=_size(mem.available),
        virtual_mem_used=_size(mem.used),
        virtual_mem_percentage=mem.percent,
        software_gcc_version=_gcc_version(),
        software_make_version=_make_version(),
        software_pymwp_version=_pymwp_version(),
        software_python_version=sys.version,
        time_now=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))


def _cpu_freq() -> dict:
    """Try to get details of CPU frequency."""
    try:
        return dict(
            cpu_max_frequency=psutil.cpu_freq().max,
            cpu_min_frequency=psutil.cpu_freq().min,
            cpu_current_frequency=psutil.cpu_freq().current)
    except FileNotFoundError:
        return dict(
            cpu_max_frequency='?',
            cpu_min_frequency='?',
            cpu_current_frequency='?')


# noinspection PyBroadException
def _run_cmd(*args):
    """Run system command and return stdout."""
    try:
        result = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT)
        return result.stdout.decode('utf-8') or ''
    except Exception:
        cmd = " ".join(args)
        return f"unavailable: command \"{cmd}\" failed"


def _pymwp_version():
    """pymwp version details."""
    cmd = 'python', '-m', 'pymwp', '--version'
    git = 'git', 'log', "--pretty=format:%h (%ai)", '-n 1'
    version = ("".join(_run_cmd(*cmd))).strip()
    sha = "".join(_run_cmd(*git))
    return f"{version}:{sha}"


def _make_version():
    """GNU make version."""
    str_out = _run_cmd('make', '--version')
    return "".join(str_out.split('\n')[:1])


def _gcc_version():
    """GCC compiler version."""
    str_out = _run_cmd('gcc', '--version')
    version = [line for line in str_out.split('\n') if line
               and line.count('/') + line.count('\\') < 3]
    return ', '.join(version)


def machine_info() -> str:
    """String representations of current machine."""
    md = _machine_details()
    values = map(lambda x: str(x).replace('\n', ' ').strip(), md.values())
    return "\n".join(map(lambda x: f'{x[0]}: {x[1]}', zip(md, values)))


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        content = machine_info()
        output_dir = sys.argv[1]
        if len(output_dir) > 0 and not exists(output_dir):
            makedirs(output_dir)
        fp = join(output_dir, '__machine_info')
        with open(fp, 'w') as mi:
            mi.write(content)
        print(f'Wrote machine details to {fp}')
    else:
        print('Output directory is required')
