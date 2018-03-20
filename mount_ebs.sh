#!/bin/bash
#attach the EBS to /dev/sdf before running it

#format EBS
mkfs -t ext4 /dev/xvdf

#copy original /var to /dev/xvdf
mkdir /mnt/new
mount /dev/xvdf /mnt/new
cd /var
cp -ax * /mnt/new
cd /
mv var var.old

#mount EBS as new /var
umount /dev/xvdf
mkdir /var
mount /dev/xvdf /var

#update fstab file to mount EBS on system startup
echo "/dev/xvdf /var ext4 noatime 0 0" >> /etc/fstab