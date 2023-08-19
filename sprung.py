import subprocess
import re


class Device:
    def __init__(self, serial_number: str, device: str) -> None:
        self.serial_number = serial_number
        self.device = device

    def check_device(self) -> None:
        found = False
        continue_loop = True

        while continue_loop is True:
            device_info = subprocess.Popen(['/usr/bin/udevadm', 'info', self.device], stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
            if "No such device" in device_info.stderr.readline().decode():
                found = False

            for line in device_info.stdout.readlines():
                line = line.decode()

                device_serial_number = re.search('(?<=ID_USB_SERIAL_SHORT=).*', line)

                if device_serial_number is not None:
                    if device_serial_number.group(0) == self.serial_number:
                        found = True
                        continue_loop = True
                    else:
                        found = False

            if found is False:
                continue_loop = False

        if not found:
            self.panic()

    def panic(self) -> None:
        cmd = 'echo b > /proc/sysrq-trigger'
        subprocess.check_output(cmd, shell=True)


def main() -> None:
    device = Device("AAZK98GWCSAYYIV9", "/dev/sdb")  # <serial number>, <device ID>
    device.check_device()


if __name__ == "__main__":
    main()
