# FPGA Odysseus with ULX3S - Workshop materials

This repo contains all needed material for participation at FPGA Odysseus with ULX3S Workshop at Radiona event in Zagreb 9th of March 2019.

# For all environments

You probably already have a favorite text editor on your computer ready, but in case it does not 
have Verilog language syntax hightlight, that could help you at least at start, install Visual Studio Code or
Atom or any similar editor supporting it.

For Visual Studio Code use:

```console
ext install mshr-h.VerilogHDL
```
For Atom use:

```console
apm install language-verilog
```

# Linux Install

First install required packages.

For Ubuntu use :
```console
sudo apt install python3-pip python3-setuptools make git gtkwave
```

Download prepared package, and install APIO
```console
cd ~

wget https://github.com/mmicko/fpga-odysseus/releases/download/v1.0/fpga-tools-linux-x64.tar.gz

tar xvfz fpga-tools-linux-x64.tar.gz

cd fpga_tools

source fpga.sh

cd apio

sudo pip install -e .
```

# Windows Install

TBD

# Workshop materials

To be able to test environment and to have starting point for workshop you also need to download this repository.

```console
git clone https://github.com/mmicko/fpga-odysseus
```

# Testing

For Linux and macOS always make sure you have tools setup and initialized first.

```console
source fpga.sh
```

## Testing APIO environment

To test if all is setup correctly.

```console

cd tests/led

apio build

```
response should be

```console
[xxx xxx x hh:mm:ss yyyy] Processing ulx3s-45f
--------------------------------------------------------------------------------
yosys -p "synth_ecp5 -json hardware.json" -q top.v
Warning: Wire top.cnt has an unprocessed 'init' attribute.
nextpnr-ecp5 --45k --package CABGA381 --json hardware.json --textcfg hardware.config --lpf ulx3s_v20.lpf -q --timing-allow-fail
ecppack --db /home/xxx/fpga_tools/apio_data/packages/toolchain-ecp5/share/trellis/database hardware.config hardware.bit
========================= [SUCCESS] Took 1.92 seconds =========================
```

## Testing Risc-V compiler

```console
cd tests/riscv
make
```
response should be

```console
riscv64-unknown-elf-gcc -mabi=ilp32 -march=rv32i -Wl,-Bstatic,-T,sections.lds,--strip-debug -ffreestanding -nostdlib -o firmware.elf start.s firmware.c
riscv64-unknown-elf-objcopy -O binary firmware.elf /dev/stdout > firmware.bin
python3 makehex.py firmware.bin 8192 > firmware.hex
```

