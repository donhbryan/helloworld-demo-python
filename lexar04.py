import subprocess
import shlex
import sys

def parse_fdisk(fdisk_output):
    result = {}
    for line in fdisk_output.split("\n"):
        if not line.startswith("/"): continue
        parts = line.split()

        inf = {}
        if parts[1] == "*":
            inf['bootable'] = True
            del parts[1]

        else:
            inf['bootable'] = False

        inf['start'] = int(parts[1])
        inf['end'] = int(parts[2])
        inf['blocks'] = int(parts[3].rstrip("+"))
        inf['partition_id'] = int(parts[4], 16)
        inf['partition_id_string'] = " ".join(parts[5:])

        result[parts[0]] = inf
    return result

def main():
    proc = subprocess.Popen(shlex.split("fdisk -l"),
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    fdisk_output, fdisk_error = proc.communicate()
    fdisk_output = fdisk_output.decode(sys.stdout.encoding)
    for disk, info in parse_fdisk(fdisk_output).items():
        print(disk, " ".join(["%s=%r" % i for i in info.items()]))

main()