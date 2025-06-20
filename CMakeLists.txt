cmake_minimum_required(VERSION 3.10)
project(MyProject)

set(CMAKE_CXX_STANDARD 17)

include_directories(${CMAKE_SOURCE_DIR}/include)

set(main
    ${CMAKE_SOURCE_DIR}/src/Airport.cpp
    ${CMAKE_SOURCE_DIR}/src/Graph.cpp
    ${CMAKE_SOURCE_DIR}/src/utility_functions.cpp
    ${CMAKE_SOURCE_DIR}/src/FlightPathOptimizer.cpp
)

add_executable(flightPathOptimizer ${main})