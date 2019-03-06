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

sudo pip3 install -e .
```

We also need to add support for programming over FTDI, so just run:
```console
sudo apio drivers --ftdi-enable
```

To be able to test environment and to have starting point for workshop you also need to download this repository.

```console
cd ~
git clone https://github.com/mmicko/fpga-odysseus
```

# Windows Install

Download file from [this link](https://github.com/mmicko/fpga-odysseus/releases/download/v1.0/fpga-tools-windows-x64.7z) first.

Uze 7zip (can be downloaded from [here](https://www.7-zip.org/download.html)) to unpack file (using right click -> 7-Zip -> Extract here )

Move that folder to root of C drive (mandatory due to location being hardcoded in part of msys install)

Go to c:\msys64  and click ConEmu.exe to get console.

Your profile will be generated and you will be greeted by next prompt.

```console
[FPGA] C:\msys64\src>
```

If you do not already have installed you favorite terminal console for serial access, please install [PuTTY](https://www.putty.org/) or similar.
You can even install it from command line by using:

```console
pacman -S mingw-w64-x86_64-putty
```

Now pull materials for workshop.

```console
git clone https://github.com/mmicko/fpga-odysseus -c core.symlinks=true
```
You will get some errors here, due to issues with specific git version on windows, but do not worry, just execute :
```console
cd fpga-odysseus 
git reset --hard
```
Now you have all setup, not need for additional testing on Windows side.

**NOTE** In case you are getting error starting git on Windows, first run msys but just leave it open at side, and try again in main window:
```console
c:\msys64\msys2.exe
```

# Testing (needed for Linux only)

For Linux always make sure you have tools setup and initialized first.

```console
cd ~/fpga_tools
source fpga.sh
```

## Testing APIO environment

To test if all is setup correctly.

```console

cd ~/fpga_tools/tests/led

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
cd ~/fpga_tools/tests/riscv
make
```
response should be

```console
riscv64-unknown-elf-gcc -mabi=ilp32 -march=rv32i -Wl,-Bstatic,-T,sections.lds,--strip-debug -ffreestanding -nostdlib -o firmware.elf start.s firmware.c
riscv64-unknown-elf-objcopy -O binary firmware.elf /dev/stdout > firmware.bin
python3 makehex.py firmware.bin 8192 > firmware.hex
```

