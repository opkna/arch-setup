#!/usr/bin/env python

import subprocess as sp


def main():
    # Verify archinstall exists
    cmd = sp.Popen(
        ["command", "-v", "archinstall"],
        shell=True,
        stdout=sp.DEVNULL,
    )
    if cmd.wait(5) != 0:
        print("Not a arch install boot")
        exit(1)

    # Validate platform size
    cmd = sp.Popen(
        ["/usr/bin/cat", "/sys/firmware/efi/fw_platform_size"],
        stdout=sp.PIPE,
    )
    if cmd.wait(5) != 0 or str(cmd.stdout.read(2), encoding="utf-8") != "64":
        print("Not a 64-bit iso")
        exit(1)

    # Check internet connection
    cmd = sp.Popen(
        ["ping", "-c", "1", "google.com"],
        stdout=sp.DEVNULL,
    )
    if cmd.wait(5) != 0:
        print("Not internet connection")
        exit(1)

    # Partition disk
    fdisk_commands = [
        "g",
        "n",
        "1",
        "\n",  # default first sector
        "+300M",
        "n",
        "2",
        "\n",  # default first sector
        "-0K",
        "w",
    ]
    input = "\n".join(fdisk_commands).encode()
    cmd = sp.Popen(
        ["fdisk", "/dev/sda"],
        stdin=sp.PIPE,
        stdout=sp.PIPE,
    )
    output = cmd.communicate(input)
    print(f"status: {cmd.returncode}")
    if output[0]:
        print("stdout:")
        print(output[0].decode())
    if output[1]:
        print("stderr:")
        print(output[1].decode())


if __name__ == "__main__":
    main()
