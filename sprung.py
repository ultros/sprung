import subprocess
import re


class Device:
    def __init__(self, serial_number: str, device: str):
        self.serial_number = serial_number
        self.device = device

    def check_device(self):
        found = False
        device_info = subprocess.Popen(['/usr/bin/udevadm', 'info', self.device], stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)

        for line in device_info.stdout.readlines():
            line = line.decode()

            device_serial_number = re.search('(?<=ID_USB_SERIAL_SHORT=).*', line)

            if device_serial_number is not None:
                if device_serial_number.group(0) == self.serial_number:
                    found = True
                    break

        if found:
            print("FOUND")
        else:
            print("NOT FOUND")
            self.panic()


    def panic(self):
        cmd = 'echo 1 > /proc/sys/kernel/sysrq'
        subprocess.check_output(cmd, shell=True)

        cmd = 'echo b > /proc/sysrq-trigger'
        subprocess.check_output(cmd, shell=True)


def main():
    device = Device("AAZK98GWCSAYYIV9", "/dev/sdb")
    device.check_device()

if __name__ == "__main__":
    main()
