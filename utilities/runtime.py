"""
Capture details of the current machine and runtime.

### Usage:

```
python3 utilities/runtime.py output_dir
```

Arguments:
    output_dir (str): Directory where to write the output.
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


def _machine_details() -> dict[str, Any]:
    """Capture relevant details of current machine."""
    result = {}
    uname = platform.uname()
    mem = psutil.virtual_memory()
    cpufreq = psutil.cpu_freq()
    result["operating_system"] = uname.system
    result["operating_system_release"] = uname.release
    result["operating_system_version"] = uname.version
    result["machine_architecture"] = uname.machine
    result["processor"] = uname.processor
    result["cpu_physical_cores"] = psutil.cpu_count(logical=False)
    result["cpu_total_cores"] = psutil.cpu_count(logical=True)
    result["cpu_max_frequency"] = cpufreq.max
    result["cpu_min_frequency"] = cpufreq.min
    result["cpu_current_frequency"] = cpufreq.current
    result["cpu_usage_per_core"] = psutil.cpu_percent(percpu=True, interval=1)
    result["cpu_total_usage"] = psutil.cpu_percent()
    result["virtual_mem_total_size"] = _size(mem.total)
    result["virtual_mem_available"] = _size(mem.available)
    result["virtual_mem_used"] = _size(mem.used)
    result["virtual_mem_percentage"] = mem.percent
    result["software_gcc_version"] = _gcc_version()
    result["software_make_version"] = _make_version()
    result["software_pymwp_version"] = _pymwp_version()
    result["software_python_version"] = sys.version
    result["time_now"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    return result


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


# noinspection PyBroadException
def _run_cmd(*args):
    """Run system command and return stdout."""
    try:
        result = subprocess.run(
            args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return result.stdout.decode('utf-8') or ''
    except Exception:
        cmd = " ".join(args)
        return f"unavailable: command \"{cmd}\" failed"


def _pymwp_version():
    """pymwp version details."""
    version = "".join(_run_cmd('python', '-m', 'pymwp', '--version'))
    sha = "".join(_run_cmd('git', 'log', "--pretty=format:%h (%ai)", '-n 1'))
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


def _machine_info() -> str:
    """String representations of current machine."""
    md = _machine_details()
    values = map(lambda x: str(x).replace('\n', ' ').strip(), md.values())
    return "\n".join(map(lambda x: f'{x[0]}: {x[1]}', zip(md, values)))


def write_file(content, output_dir: str):
    if len(output_dir) > 0 and not exists(output_dir):
        makedirs(output_dir)
    fp = join(output_dir, '__machine_info')
    with open(fp, 'w') as mi:
        mi.write(content)
    print(f'Wrote machine details to {fp}')


if __name__ == '__main__':
    """By default write the info."""
    if len(sys.argv) >= 2:
        write_file(_machine_info(), sys.argv[1])
    else:
        print('Output directory is required')
