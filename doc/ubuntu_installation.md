# Installing Ubuntu 20.04 alongside Windows

1. Create a free partition on Windows 10
Before installing Ubuntu, We need to create a free partition which can be used later to install Ubuntu 20.04. Open the "Device Manager" in Windows or Run "diskmgmt.msc", To create a separation for Ubuntu, we need to shrink the volume of C by right click on the volume and select 'Shrink' and provide the amount of space that you need to create, clicking "Shrink" on the dialogue, which will create an unallocated partition.

2. Create a bootable Linux USB Flash Drive
Download the [Ubuntu 20.04 ISO](https://ubuntu.com/download/desktop), and use [Universal USB Installer](https://www.pendrivelinux.com/universal-usb-installer-easy-as-1-2-3/) to make a Linux usb flash drive.

3. Change boot setting
Restart the system, and press 'F2' or 'F12' for bios setting, on "booting", select option 1 for booting from USB. Save the change and start the system

4. Install Ubuntu
Choose Install Ubuntu after system restarting, for the first time, select the installation type "something else". select the "free space" for creating new partitions: "/boot", "/home", "/var", "/", "swap area" with specific amount of space according to the disk space and using ext4. An example of 40 GB free space, "/boot" - 1 GB, "/home" = 22 GB, "/var" - 6 GB, "/" = 10 GB, "swap area" - 2 GB.
If old version Ubuntu is already installed, you can just erase the old verion of Ubuntu and install new version of uUuntu.    

## Reference
- [How to Dual Boot Ubuntu 20.04 LTS Aling with Windows 10](https://www.linuxtechi.com/dual-boot-ubuntu-20-04-lts-along-with-windows-10/)
