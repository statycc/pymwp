"""
Capture details of the current machine and runtime.

# Usage

python3 utilities/runtime.py [output_dir]

Where [output_dir] specifies where to write the output.
"""

# noinspection PyPackageRequirements
import psutil
import platform
import sys
from os.path import join, isdir


def size(bytes_, suffix="B") -> str:
    """Scales bytes to appropriate format.

    Example:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'

    Arguments:
          bytes_ : number of bytes
          suffix: "bytes" unit char [default: B]

    Returns:
          Formatted size expression.
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes_ < factor:
            return f"{bytes_:.2f}{unit}{suffix}"
        bytes_ /= factor


def machine_details() -> dict:
    """Capture relevant runtime props."""
    result = {}
    uname = platform.uname()
    mem = psutil.virtual_memory()
    result["system"] = uname.system
    result["release"] = uname.release
    result["version"] = uname.version
    result["machine"] = uname.machine
    result["processor"] = uname.processor
    result["cpu_physical_cores"] = psutil.cpu_count(logical=False)
    result["cpu_total_cores"] = psutil.cpu_count(logical=True)
    try:
        cpufreq = psutil.cpu_freq()
        result["cpu_max_frequency"] = cpufreq.max
        result["cpu_min_frequency"] = cpufreq.min
        result["cpu_current_frequency"] = cpufreq.current
    except FileNotFoundError:
        pass
    result["cpu_usage_per_core"] = \
        psutil.cpu_percent(percpu=True, interval=1)
    result["cpu_total_usage"] = psutil.cpu_percent()
    result["virtual_mem_total_size"] = size(mem.total)
    result["virtual_mem_available"] = size(mem.available)
    result["virtual_mem_used"] = size(mem.used)
    result["virtual_mem_percentage"] = mem.percent
    result["python_runtime"] = sys.version
    return result


def machine_info() -> str:
    """String representations of current machine."""
    value_fmt = lambda x: str(x).replace("\n", "")
    return "\n".join([
        f'{k}: {value_fmt(v)}'
        for (k, v) in machine_details().items()])


def write_info(output_dir: str):
    fp = join(output_dir, '__machine_info')
    with open(fp, 'w') as mi:
        mi.write(machine_info())
    print(f'Wrote machine details to {fp}')


if __name__ == '__main__':
    """By default write the info."""
    out_dir = sys.argv[1]
    if isdir(out_dir):
        write_info(out_dir)
