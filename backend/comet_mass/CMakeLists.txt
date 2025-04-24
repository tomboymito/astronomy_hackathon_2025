cmake_minimum_required(VERSION 3.12)
project(comet_mass)

# Настройки компилятора
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Поиск Python и PyBind11
find_package(Python REQUIRED COMPONENTS Development)
find_package(pybind11 REQUIRED)

# Поиск GoogleTest
find_package(GTest REQUIRED)
include_directories(${GTEST_INCLUDE_DIRS})

# Создание модуля
pybind11_add_module(comet_mass src/comet_mass.cpp)

# Добавление тестов
enable_testing()
add_executable(test_mass tests/test_mass.cpp src/comet_mass.cpp)
target_link_libraries(test_mass ${GTEST_LIBRARIES} pthread)
add_test(NAME test_mass COMMAND test_mass)

# Настройки оптимизации
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_options(comet_mass PRIVATE -O3)
endif()

# Установка модуля
install(TARGETS comet_mass DESTINATION .)
