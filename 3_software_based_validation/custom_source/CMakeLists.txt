cmake_minimum_required(VERSION 3.3 FATAL_ERROR)
project(openmc_sources CXX)
add_library(source SHARED disc_source.cpp)
find_package(OpenMC REQUIRED HINTS /usr/bin/local/openmc)
if (OpenMC_FOUND)
  message(STATUS "Found OpenMC: ${OpenMC_DIR}")
endif()

