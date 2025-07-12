# Generated CMake Pico project file

cmake_minimum_required(VERSION 3.13)

set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Initialise pico_sdk from installed location

# == DO NOT EDIT THE FOLLOWING LINES for the Raspberry Pi Pico VS Code Extension to work ==
if(WIN32)
    set(USERHOME $ENV{USERPROFILE})
else()
    set(USERHOME $ENV{HOME})
endif()
set(sdkVersion 2.1.1)
set(toolchainVersion 14_2_Rel1)
set(picotoolVersion 2.1.1)
set(picoVscode ${USERHOME}/.pico-sdk/cmake/pico-vscode.cmake)
if (EXISTS ${picoVscode})
    include(${picoVscode})
endif()
# ====================================================================================

set(PICO_BOARD pico_w CACHE STRING "Board type")

# Pull in Raspberry Pi Pico SDK
include(pico_sdk_import.cmake)

project(main_project C CXX ASM)

# Initialise the Raspberry Pi Pico SDK
pico_sdk_init()

# Define executable and source files
add_executable(main
    main.c
    src/ili9225.c
)

# Set metadata
pico_set_program_name(main "main")
pico_set_program_version(main "0.1")

# Enable/disable standard I/O
pico_enable_stdio_uart(main 0)
pico_enable_stdio_usb(main 0)

# Link required libraries
target_link_libraries(main
    pico_stdlib
    hardware_spi
)

# Include headers from 'include' directory
target_include_directories(main PRIVATE
    ${CMAKE_CURRENT_LIST_DIR}/include
)

# Generate UF2, bin, hex, etc.
pico_add_extra_outputs(main)
