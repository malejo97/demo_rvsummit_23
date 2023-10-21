#!/bin/bash

make -C bao-baremetal-guest clean
make -C bao-baremetal-guest CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=cva6

make -C bao-hypervisor clean
make -C bao-hypervisor CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=cva6 CONFIG=cva6-baremetal CONFIG_BUILTIN=y

make -C opensbi clean
make -C opensbi CROSS_COMPILE=riscv64-unknown-linux-gnu- PLATFORM=fpga/ariane FW_PAYLOAD=y FW_PAYLOAD_PATH=/home/manuale97/my_repositories/demo_rvsummit_23/bao-hypervisor/bin/cva6/cva6-baremetal/bao.bin