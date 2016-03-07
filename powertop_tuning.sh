#!/bin/bash

# Autosuspend for USB device Touchscreen [ELAN]
echo 'auto' > '/sys/bus/usb/devices/1-1.5/power/control';
# Enable Audio codec power management
echo '1' > '/sys/module/snd_hda_intel/parameters/power_save';
# Enable SATA link power management for host4
echo 'min_power' > '/sys/class/scsi_host/host4/link_power_management_policy';
# Enable SATA link power management for host5
echo 'min_power' > '/sys/class/scsi_host/host5/link_power_management_policy';
# Enable SATA link power management for host2
echo 'min_power' > '/sys/class/scsi_host/host2/link_power_management_policy';
# Enable SATA link power management for host3
echo 'min_power' > '/sys/class/scsi_host/host3/link_power_management_policy';
# Enable SATA link power management for host0
echo 'min_power' > '/sys/class/scsi_host/host0/link_power_management_policy';
# Enable SATA link power management for host1
echo 'min_power' > '/sys/class/scsi_host/host1/link_power_management_policy';
# VM writeback timeout
echo '1500' > '/proc/sys/vm/dirty_writeback_centisecs';
# NMI watchdog should be turned off
echo '0' > '/proc/sys/kernel/nmi_watchdog';
# Runtime PM for I2C Adapter i2c-4 (i915 gmbus dpb)
echo 'auto' > '/sys/bus/i2c/devices/i2c-4/device/power/control';
# Autosuspend for USB device Touchscreen [ELAN]
echo 'auto' > '/sys/bus/usb/devices/3-1.5/power/control';
# Runtime PM for I2C Adapter i2c-3 (i915 gmbus dpc)
echo 'auto' > '/sys/bus/i2c/devices/i2c-3/device/power/control';
# Autosuspend for unknown USB device 4-1.5 (8087:07da)
echo 'auto' > '/sys/bus/usb/devices/4-1.5/power/control';
# Runtime PM for I2C Adapter i2c-0 (i915 gmbus ssc)
echo 'auto' > '/sys/bus/i2c/devices/i2c-0/device/power/control';
# Runtime PM for I2C Adapter i2c-1 (i915 gmbus vga)
echo 'auto' > '/sys/bus/i2c/devices/i2c-1/device/power/control';
# Runtime PM for I2C Adapter i2c-2 (i915 gmbus panel)
echo 'auto' > '/sys/bus/i2c/devices/i2c-2/device/power/control';
# Runtime PM for I2C Adapter i2c-5 (i915 gmbus dpd)
echo 'auto' > '/sys/bus/i2c/devices/i2c-5/device/power/control';
# Runtime PM for I2C Adapter i2c-6 (DPDDC-B)
echo 'auto' > '/sys/bus/i2c/devices/i2c-6/device/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family SMBus Controller
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.3/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family PCI Express Root Port 4
echo 'auto' > '/sys/bus/pci/devices/0000:00:1c.3/power/control';
# Runtime PM for PCI Device Intel Corporation 3rd Gen Core processor Graphics Controller
echo 'auto' > '/sys/bus/pci/devices/0000:00:02.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family USB xHCI Host Controller
echo 'auto' > '/sys/bus/pci/devices/0000:00:14.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family MEI Controller #1
echo 'auto' > '/sys/bus/pci/devices/0000:00:16.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family USB Enhanced Host Controller #2
echo 'auto' > '/sys/bus/pci/devices/0000:00:1a.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family High Definition Audio Controller
echo 'auto' > '/sys/bus/pci/devices/0000:00:1b.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family USB Enhanced Host Controller #1
echo 'auto' > '/sys/bus/pci/devices/0000:00:1d.0/power/control';
# Runtime PM for PCI Device Intel Corporation HM76 Express Chipset LPC Controller
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series Chipset Family 6-port SATA Controller [AHCI mode]
echo 'auto' > '/sys/bus/pci/devices/0000:00:1f.2/power/control';
# Runtime PM for PCI Device Intel Corporation Centrino Advanced-N 6235
echo 'auto' > '/sys/bus/pci/devices/0000:01:00.0/power/control';
# Runtime PM for PCI Device Realtek Semiconductor Co., Ltd. RTL8111/8168/8411 PCI Express Gigabit Ethernet Controller
echo 'auto' > '/sys/bus/pci/devices/0000:02:00.0/power/control';
# Runtime PM for PCI Device Intel Corporation 3rd Gen Core processor DRAM Controller
echo 'auto' > '/sys/bus/pci/devices/0000:00:00.0/power/control';
# Runtime PM for PCI Device Intel Corporation 7 Series/C210 Series Chipset Family PCI Express Root Port 1
echo 'auto' > '/sys/bus/pci/devices/0000:00:1c.0/power/control';
# Wake-on-lan status for device enp2s0
ethtool -s enp2s0 wol d;
