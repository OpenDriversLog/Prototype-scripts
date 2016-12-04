#!/bin/sh

#mount USB device  under /mnt/sda1 first
dd if=/dev/mtd0 of=/mnt/sda1/wrtnode_u-boot.backup
dd if=/dev/mtd1 of=/mnt/sda1/wrtnode_u-boot-env.backup
dd if=/dev/mtd2 of=/mnt/sda1/wrtnode_factory.backup
dd if=/dev/mtd3 of=/mnt/sda1/wrtnode_firmware.backup