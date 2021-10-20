#!/bin/sh
cd /home/kosenctfx/infected/challenge/kernel/
timeout --foreground 300 qemu-system-x86_64 \
    -m 64M \
    -kernel ./bzImage \
    -initrd ./rootfs.cpio \
    -append "root=/dev/ram rw console=ttyS0 oops=panic panic=1 kaslr quiet" \
    -cpu kvm64,+smap,+smap \
    -monitor /dev/null \
    -nographic
