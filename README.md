# FaDAS
## Team AOHW-154
### Team members :
#### Murat Tokez              (m.tokez2019@gtu.edu.tr)
#### Ilker Acar               (i.acar2020@gtu.edu.tr)
#### Duygu Zeynep Tuncel      (d.tuncel2020@gtu.edu.tr)
#### Mehmet Salih Turhan      (m.turhan2020@gtu.edu.tr)
#### Beyzanur Cam             (b.cam2021@gtu.edu.tr)
### Supervisor:
#### İhsan Cicek

# Introduction
This project is about running and accelerating vehicle detection and mapping ADAS applications in parking lot using Deep Learning Unit (DPU) on KV260 FPGA board. 

## Documentation
[Documentation]()

## Prerequires

- **[Vitis-AI](https://github.com/Xilinx/Vitis-AI/tree/3.0):** High-level libraries and APIs for AI inference with DPU cores.
- **[Deep Learning Unit (DPUCZDX8G)](https://github.com/Xilinx/Vitis-AI/tree/3.0/dpu):** A configurable computation engine optimized for convolutional neural networks.
- **[PetaLinux](https://docs.amd.com/r/2022.2-English/ug1144-petalinux-tools-reference-guide/Installation-Requirements):** An embedded Linux SDK targeting FPGA-based SoC designs.

## System Architecture

The system includes:
- Kria KV260
- A 2D LiDAR
- A camera
- A rotary encoder and Arduino to provide the third axis to the 2D LiDAR, creating a 3D point cloud

### Steps Involved:

1. **Vivado Project:** Create hardware design.
2. **Linux Project:** Integrate hardware with PetaLinux.
3. **Model Reconstruction:** Utilize models from the model zoo.
4. **Device Tree Overlay:** Configure hardware settings.
5. **Application Deployment:** Load and run the application code on the development board.

## Prerequires
1. Kria KV260 FPGA Board
2. SD Card
3. RPLIDAR A1M8
4. Camera
5. Rotary Encoder
6. Arduino nano


## Hardware Design

![hardware](https://github.com/DELTAICLAB/FaDAS/blob/main/images/overlay.jpg)

### Connections:

- I2C pins connected to KV260 Pmod pins
- Necessary pull-up resistors enabled for I2C communication

## PetaLinux Configuration and Compilation

### Steps:

1. **Project Creation:**
   ```sh
   petalinux-create -t project -s <path_to_bsp_file> --name dpuOS

   ## Configuration

### 1. Enable FPGA Manager
### 2. Disable TFTPboot Copy
### 3. Select EXT4 as Root Filesystem Type

## Kernel Configuration

### 1. Enable DPU Driver
### 2. Enable USB-to-Serial Converter Driver

## Build Project
\`\`\`bash
petalinux-build
\`\`\`

## Packaging and Booting
Prepare SD card and boot the system.

## Device Tree Overlay
Generate and compile the device tree overlay to specify hardware configuration.

## Running the Application

### Install AI Library
1. Download and install Vitis AI Runtime.
2. Optimize DPU for ZynqMP SoCs.
3. Install Vitis AI library and model files.

### Run ADAS Application
\`\`\`bash
cd ~/examples/vai_runtime/adas_detection
bash -x build.sh
./adas_detection /dev/video0 /usr/share/vitis_ai_library/models/yolov3_adas_pruned_0_9/yolov3_adas_pruned_0_9.xmodel
\`\`\`

   


