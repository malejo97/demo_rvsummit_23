#!/bin/bash

ROOT="/home/manuale97/my_repositories/demo_rvsummit_23"

BAREMETAL_DIR="${ROOT}/bao-baremetal-guest"
BAO_DIR="${ROOT}/bao-hypervisor"
CONFIG_DIR="${ROOT}/configs"
OPENSBI_DIR="${ROOT}/opensbi"

OUTPUT_DIR="${ROOT}/output"

if [ ! -e ${OUTPUT_DIR} ]; then
    mkdir ${OUTPUT_DIR}
fi

rm -f -r ${OUTPUT_DIR}/*

make -C ${BAREMETAL_DIR} clean
make -C ${BAREMETAL_DIR} CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=cva6

if [ ! -e ${BAREMETAL_DIR}/build/cva6/baremetal.bin ]; then
    echo "$0: ${BAREMETAL_DIR}/build/cva6/baremetal.bin not found"
    exit 1
else
    cp ${BAREMETAL_DIR}/build/cva6/baremetal.bin ${OUTPUT_DIR}
fi

make -C ${BAO_DIR} clean
make -C ${BAO_DIR} CROSS_COMPILE=riscv64-unknown-elf- PLATFORM=cva6 CONFIG_REPO=${CONFIG_DIR} CONFIG=cva6-baremetal CONFIG_BUILTIN=y
if [ ! -e ${BAO_DIR}/bin/cva6/cva6-baremetal/bao.bin ]; then
    echo "$0: ${BAO_DIR}/bin/cva6/cva6-baremetal/bao.bin not found"
    exit 1
else
    cp ${BAO_DIR}/bin/cva6/cva6-baremetal/bao.bin ${OUTPUT_DIR}
fi

make -C ${OPENSBI_DIR} clean
make -C ${OPENSBI_DIR} CROSS_COMPILE=riscv64-unknown-linux-gnu- PLATFORM=fpga/ariane FW_PAYLOAD=y FW_PAYLOAD_PATH=${OUTPUT_DIR}/bao.bin
if [ ! -e ${OPENSBI_DIR}/build/platform/fpga/ariane/firmware/fw_payload.elf ]; then
    echo "$0: ${OPENSBI_DIR}/build/platform/fpga/ariane/firmware/fw_payload.elf not found"
    exit 1
else
    cp ${OPENSBI_DIR}/build/platform/fpga/ariane/firmware/fw_payload.elf ${OPENSBI_DIR}/build/platform/fpga/ariane/firmware/fw_payload.bin ${OUTPUT_DIR}
fi