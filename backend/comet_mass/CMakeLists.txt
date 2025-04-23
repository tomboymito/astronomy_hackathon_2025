find_package(pybind11 REQUIRED)
cmake_minimum_required(VERSION 3.12)
project(comet_mass)

# Настройки компилятора
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Поиск Python и PyBind11
find_package(Python REQUIRED COMPONENTS Development)
find_package(pybind11 REQUIRED)

# Создание модуля
pybind11_add_module(comet_mass src/comet_mass.cpp)

# Настройки оптимизации
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(comet_mass PRIVATE -O3)
endif()

# Установка модуля
install(TARGETS comet_mass DESTINATION .)