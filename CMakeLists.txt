cmake_minimum_required(VERSION 3.28)

project(miniposix_workshop VERSION 0.1.0 LANGUAGES C CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

add_library(miniposix
    src/unique_fd.cpp
    src/pipe.cpp
)
target_include_directories(miniposix PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)
target_compile_options(miniposix PRIVATE -Wall -Wextra -Wpedantic)

find_package(Threads REQUIRED)
add_executable(bench_pipe benchmarks/bench_pipe.cpp)
target_link_libraries(bench_pipe PRIVATE miniposix Threads::Threads)
target_compile_options(bench_pipe PRIVATE -Wall -Wextra -Wpedantic)

include(CTest)
if(BUILD_TESTING)
    find_package(GTest REQUIRED)

    add_executable(test_smoke tests/test_smoke.cpp)
    target_link_libraries(test_smoke PRIVATE GTest::gtest_main)
    add_test(NAME smoke COMMAND test_smoke)
    set_tests_properties(smoke PROPERTIES LABELS smoke)

    add_executable(test_unique_fd tests/test_unique_fd.cpp)
    target_link_libraries(test_unique_fd PRIVATE miniposix GTest::gtest_main)
    add_test(NAME unique_fd COMMAND test_unique_fd)
    set_tests_properties(unique_fd PROPERTIES LABELS functional)

    add_executable(test_pipe tests/test_pipe.cpp)
    target_link_libraries(test_pipe PRIVATE miniposix GTest::gtest_main)
    add_test(NAME pipe COMMAND test_pipe)
    set_tests_properties(pipe PROPERTIES LABELS functional)
endif()
