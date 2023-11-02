# demo_rvsummit_23
RISC-V IOMMU Demo for the RISC-V Summit 2023

<!-- Table of contents -->
<!-- License -->
<!-- About this project -->
<!-- Interfaces -->
<!-- Usage -->
<!-- Features -->
<!-- Testing -->
<!-- Roadmap -->

## Table of Contents

- [License](#license)
- [About this Project](#about-this-project)
- [Repository Structure](#repository-structure)
- [IOMMU Features](#iommu-features)
- [Module Parameters](#module-parameters)
- [IP Interfaces](#ip-interfaces)
- [IP Usage](#ip-usage)
- [Validation](#validation)
- [Tools and versions](#tools-and-versions)
- [Roadmap and Contributions](#roadmap-and-contributions)

***

## License

This work is licensed under the Apache-2.0 License. See the [LICENSE](./LICENSE) file for details.

## About this Repository

![Demo Capture](./doc/demo_capture.png)

RISC-V IOMMU Demo for the RISC-V Summit 2023, presented in the [Technology Innovation Institute (TII)](https://www.tii.ae/) booth.

It consists of a game similar to the russian roulette, in which a DMA device is programmed to write zeros into critical memory regions of a single-core CVA6-based platform executing Bao hypervisor and one baremetal guest atop of it. The demo is carried out in a Genesys2 FPGA board and the user navigates through the demo using the five push buttons in the board.

An Input/Output Memory Management Unit (IOMMU) is integrated into the platform. It is enabled by default, but can be disabled using one of the eight switches in the board. However, the lethal switch is selected randomly on every attack. The user can iterate eight times trying switches individually to find the lethal one, or enable multiple switches in a single attack.

The user can select between two targets: [OpenSBI](https://github.com/riscv-software-src/opensbi) and [Bao hypervisor](https://github.com/bao-project/bao-hypervisor). The lethal attack will take down the system in both options.


## **GUI Dependencies**

In order to run the Graphical User Interface of the demo, you need to install the following python packages:

- PyQt5 v5.15.9
- pyserial v3.5

To install these packages:
```
python3 -m pip install <package_name>
```

## **Usage**

To compile Bao with the baremetal guest and OpenSBI, run in the top directory of the repository:
```
./build_all
```
The output files (.bin and .elf) will be at `opensbi/build/platform/fpga/ariane/firmware/fw_payload.bin`.
> Note: To execute the previous command, you need the `riscv64-unknown-elf-` and `riscv64-unknown-linux-gnu-` toolchains installed and defined in your `$PATH`.

To execute the GUI application, run:
```
python3 main.py <serial_port>
```
Where `<serial_port>` is the absolute path of the serial port connected to the FPGA board (e.g., /dev/ttyUSB0).