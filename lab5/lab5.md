### 2019/6/21, lab 5. Robin Hong, hongz@rpi.edu.
# Open Source Build

## First Part

#### Step 1
CMakeLists.txt

```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_STANDARD_REQUIRED True)

configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

add_executable(Tutorial tutorial.cxx)

target_include_directories(Tutorial PUBLIC
  "${PROJECT_BINARY_DIR}"
  )
```

tutorial.cxx

```c
// A simple program that computes the square root of a number
#include <cmath>
#include <cstdlib>
#include <iostream>
#include <string>
#include <sstream>

#include  "TutorialConfig.h"

int main(int argc, char* argv[])
{
  if (argc < 2) {
    std::cout << "Usage: " << argv[0] << " number" << std::endl;
    return 1;
  }

  double inputValue = std::stod(argv[1]);

  double outputValue = sqrt(inputValue);
  std::cout << "The square root of " << inputValue << " is " << outputValue
            << std::endl;
  return 0;
}
```

Running results are:
![step1_running](./pictures/step1_running.png)


#### Step 2

CMakeLists.txt

```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 14)
# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

option (USE_MYMATH "Use tutorial provided math implementation" ON)

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
  list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )
```

tutorial.css

```c
// A simple program that computes the square root of a number
#include <cmath>
#include <iostream>
#include <string>

#include "TutorialConfig.h"

int main(int argc, char* argv[])
{
  if (argc < 2) {
    std::cout << argv[0] << " Version " << Tutorial_VERSION_MAJOR << "."
              << Tutorial_VERSION_MINOR << std::endl;
    std::cout << "Usage: " << argv[0] << " number" << std::endl;
    return 1;
  }

  double inputValue = std::stod(argv[1]);
#ifdef USE_MYPATH
  double outputValue = mysqrt(inputValue);
#else
  double outputValue = sqrt(inputValue);
#endif
  std::cout << "The square root of " << inputValue << " is " << outputValue
            << std::endl;
  return 0;
}
```

Running results are:
![step2_running](./pictures/step2_running.png)

#### Step 3

CMakeLists.txt

```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 14)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
  list(APPEND EXTRA_INCLUDES "${PROJECT_SOURCE_DIR}/MathFunctions")
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           ${EXTRA_INCLUDES}
                           )


target_include_directories(MathFunctions
  INTERFACE ${CMAKE_CURRENT_SOURCE_DIR})
```

MathFunctions/CMakeLists.txt

```
add_library(MathFunctions mysqrt.cxx)
```

Running results are:
![step3_running](./pictures/step3_running.png)

#### Step 4

CMakeLists.txt

```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 14)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
endif(USE_MYMATH)

# add the executable
add_executable(Tutorial tutorial.cxx)

target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )

install(TARGETS Tutorial DESTINATION bin)
install(FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
        DESTINATION include
        )

# enable testing
enable_testing()

# does the application run
add_test(NAME Runs COMMAND Tutorial 25)

# does the usage message work?
add_test(NAME Usage COMMAND Tutorial)
set_tests_properties(Usage
  PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number"
  )

# define a function to simplify adding tests
function(do_test target arg result)
  add_test(NAME Comp${arg} COMMAND ${target} ${arg})
  set_tests_properties(Comp${arg}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result}
  )
endfunction(do_test)

# do a bunch of result based tests
do_test(Tutorial 25 "25 is 5")
do_test(Tutorial -25 "-25 is [-nan|nan|0]")
do_test(Tutorial 0.0001 "0.0001 is 0.01")
```

MathFunctions/CMakeLists.txt

```
add_library(MathFunctions mysqrt.cxx)

# state that anybody linking to us needs to include the current source dir
# to find MathFunctions.h, while we don't.
target_include_directories(MathFunctions
          INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
          )

install (TARGETS MathFunctions DESTINATION bin)
install (FILES MathFunctions.h DESTINATION include)
```

Running results are:
![step4_running1](./pictures/step4_running1.png)
![step4_running2](./pictures/step4_running2.png)

#### Step 5

CMakeLists.txt

```
cmake_minimum_required(VERSION 3.3)
project(Tutorial)

set(CMAKE_CXX_STANDARD 14)

# should we use our own math functions
option(USE_MYMATH "Use tutorial provided math implementation" ON)

# the version number.
set(Tutorial_VERSION_MAJOR 1)
set(Tutorial_VERSION_MINOR 0)

# configure a header file to pass some of the CMake settings
# to the source code
configure_file(
  "${PROJECT_SOURCE_DIR}/TutorialConfig.h.in"
  "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  )

# add the MathFunctions library?
if(USE_MYMATH)
  add_subdirectory(MathFunctions)
  list(APPEND EXTRA_LIBS MathFunctions)
endif()

# add the executable
add_executable(Tutorial tutorial.cxx)
target_link_libraries(Tutorial PUBLIC ${EXTRA_LIBS})

# add the binary tree to the search path for include files
# so that we will find TutorialConfig.h
target_include_directories(Tutorial PUBLIC
                           "${PROJECT_BINARY_DIR}"
                           )

# add the install targets
install(TARGETS Tutorial DESTINATION bin)
install(FILES "${PROJECT_BINARY_DIR}/TutorialConfig.h"
  DESTINATION include
  )

# enable testing
enable_testing()

# does the application run
add_test(NAME Runs COMMAND Tutorial 25)

# does the usage message work?
add_test(NAME Usage COMMAND Tutorial)
set_tests_properties(Usage
  PROPERTIES PASS_REGULAR_EXPRESSION "Usage:.*number"
  )

# define a function to simplify adding tests
function(do_test target arg result)
  add_test(NAME Comp${arg} COMMAND ${target} ${arg})
  set_tests_properties(Comp${arg}
    PROPERTIES PASS_REGULAR_EXPRESSION ${result}
    )
endfunction(do_test)

# do a bunch of result based tests
do_test(Tutorial 4 "4 is 2")
do_test(Tutorial 9 "9 is 3")
do_test(Tutorial 5 "5 is 2.236")
do_test(Tutorial 7 "7 is 2.645")
do_test(Tutorial 25 "25 is 5")
do_test(Tutorial -25 "-25 is [-nan|nan|0]")
do_test(Tutorial 0.0001 "0.0001 is 0.01")

# does this system provide the log and exp functions?
include(CheckSymbolExists)
set(CMAKE_REQUIRED_LIBRARIES "m")
check_symbol_exists(log "math.h" HAVE_LOG)
check_symbol_exists(exp "math.h" HAVE_EXP)
```

MathFunctions/CMakeLists.txt

```
add_library(MathFunctions mysqrt.cxx)

target_include_directories(MathFunctions
        INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}
        PRIVATE ${Tutorial_BINARY_DIR}
        )

install(TARGETS MathFunctions DESTINATION lib)
install(FILES MathFunctions.h DESTINATION include)
```

Running results are:
![step5_running](./pictures/step5_running.png)

## Second Part

I have wrote the Makefile:

```
all: static_program dynamic_program

# static library
static_program: static_program.o static_lib_block.a
	cc static_program.o static_lib_block.a -o static_program
static_program.o: program.c
	cc -c program.c -o static_program.o
static_lib_block.a: static_block.o
	ar qc static_lib_block.a static_block.o
static_block.o: ./source/block.c
	cc -c ./source/block.c -o static_block.o

# shared library
dynamic_program: shared_program.o shared_lib_block.so
	cc shared_program.o shared_lib_block.so -o dynamic_program -Wl,-rpath='$$ORIGIN'
shared_program.o: program.c
	cc -c program.c -o shared_program.o
shared_lib_block.so: dynamic_block.o
	cc -shared -o shared_lib_block.so dynamic_block.o
dynamic_block.o: ./source/block.c
	cc -fPIC -c ./source/block.c -o dynamic_block.o

```


Running the '''make''' command on terminal, the results are:
![make](./pictures/make.png)

For the CMakeLists.txt file:

```
cmake_minimum_required(VERSION 1.0)
project(program)

set(program_VERSION_MAJOR 1)
set(program_VERSION_MINOR 0)

add_library(cmake_shared_block SHARED ./source/block.c ./headers/block.h)
add_library(cmake_static_block STATIC ./source/block.c ./headers/block.h)

add_executable(cmake_dynamic_program program.c)
target_link_libraries(cmake_dynamic_program cmake_shared_block)

add_executable(cmake_static_program program.c)
target_link_libraries(cmake_static_program cmake_static_block)
```

The Makefile created by cmake is:

```
# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.10

# Default target executed when no arguments are given to make.
default_target: all

.PHONY : default_target

# Allow only one "make -f Makefile2" at a time, but pass parallelism.
.NOTPARALLEL:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/robindebkl/Git/OpenSourceSoftware-19u/CSCI-49XX-OpenSource/Modules/BuildSystems/Lab-Example

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/robindebkl/Git/OpenSourceSoftware-19u/CSCI-49XX-OpenSource/Modules/BuildSystems/Lab-Example/build

#=============================================================================
# Targets provided globally by CMake.

# Special rule for the target rebuild_cache
rebuild_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "Running CMake to regenerate build system..."
	/usr/bin/cmake -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR)
.PHONY : rebuild_cache

# Special rule for the target rebuild_cache
rebuild_cache/fast: rebuild_cache

.PHONY : rebuild_cache/fast

# Special rule for the target edit_cache
edit_cache:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --cyan "No interactive CMake dialog available..."
	/usr/bin/cmake -E echo No\ interactive\ CMake\ dialog\ available.
.PHONY : edit_cache

# Special rule for the target edit_cache
edit_cache/fast: edit_cache

.PHONY : edit_cache/fast

# The main all target
all: cmake_check_build_system
	$(CMAKE_COMMAND) -E cmake_progress_start /home/robindebkl/Git/OpenSourceSoftware-19u/CSCI-49XX-OpenSource/Modules/BuildSystems/Lab-Example/build/CMakeFiles /home/robindebkl/Git/OpenSourceSoftware-19u/CSCI-49XX-OpenSource/Modules/BuildSystems/Lab-Example/build/CMakeFiles/progress.marks
	$(MAKE) -f CMakeFiles/Makefile2 all
	$(CMAKE_COMMAND) -E cmake_progress_start /home/robindebkl/Git/OpenSourceSoftware-19u/CSCI-49XX-OpenSource/Modules/BuildSystems/Lab-Example/build/CMakeFiles 0
.PHONY : all

# The main clean target
clean:
	$(MAKE) -f CMakeFiles/Makefile2 clean
.PHONY : clean

# The main clean target
clean/fast: clean

.PHONY : clean/fast

# Prepare targets for installation.
preinstall: all
	$(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall

# Prepare targets for installation.
preinstall/fast:
	$(MAKE) -f CMakeFiles/Makefile2 preinstall
.PHONY : preinstall/fast

# clear depends
depend:
	$(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 1
.PHONY : depend

#=============================================================================
# Target rules for targets named cmake_static_program

# Build rule for target.
cmake_static_program: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 cmake_static_program
.PHONY : cmake_static_program

# fast build rule for target.
cmake_static_program/fast:
	$(MAKE) -f CMakeFiles/cmake_static_program.dir/build.make CMakeFiles/cmake_static_program.dir/build
.PHONY : cmake_static_program/fast

#=============================================================================
# Target rules for targets named cmake_shared_block

# Build rule for target.
cmake_shared_block: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 cmake_shared_block
.PHONY : cmake_shared_block

# fast build rule for target.
cmake_shared_block/fast:
	$(MAKE) -f CMakeFiles/cmake_shared_block.dir/build.make CMakeFiles/cmake_shared_block.dir/build
.PHONY : cmake_shared_block/fast

#=============================================================================
# Target rules for targets named cmake_dynamic_program

# Build rule for target.
cmake_dynamic_program: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 cmake_dynamic_program
.PHONY : cmake_dynamic_program

# fast build rule for target.
cmake_dynamic_program/fast:
	$(MAKE) -f CMakeFiles/cmake_dynamic_program.dir/build.make CMakeFiles/cmake_dynamic_program.dir/build
.PHONY : cmake_dynamic_program/fast

#=============================================================================
# Target rules for targets named cmake_static_block

# Build rule for target.
cmake_static_block: cmake_check_build_system
	$(MAKE) -f CMakeFiles/Makefile2 cmake_static_block
.PHONY : cmake_static_block

# fast build rule for target.
cmake_static_block/fast:
	$(MAKE) -f CMakeFiles/cmake_static_block.dir/build.make CMakeFiles/cmake_static_block.dir/build
.PHONY : cmake_static_block/fast

# target to build an object file
program.o:
	$(MAKE) -f CMakeFiles/cmake_static_program.dir/build.make CMakeFiles/cmake_static_program.dir/program.o
	$(MAKE) -f CMakeFiles/cmake_dynamic_program.dir/build.make CMakeFiles/cmake_dynamic_program.dir/program.o
.PHONY : program.o

# target to preprocess a source file
program.i:
	$(MAKE) -f CMakeFiles/cmake_static_program.dir/build.make CMakeFiles/cmake_static_program.dir/program.i
	$(MAKE) -f CMakeFiles/cmake_dynamic_program.dir/build.make CMakeFiles/cmake_dynamic_program.dir/program.i
.PHONY : program.i

# target to generate assembly for a file
program.s:
	$(MAKE) -f CMakeFiles/cmake_static_program.dir/build.make CMakeFiles/cmake_static_program.dir/program.s
	$(MAKE) -f CMakeFiles/cmake_dynamic_program.dir/build.make CMakeFiles/cmake_dynamic_program.dir/program.s
.PHONY : program.s

# target to build an object file
source/block.o:
	$(MAKE) -f CMakeFiles/cmake_shared_block.dir/build.make CMakeFiles/cmake_shared_block.dir/source/block.o
	$(MAKE) -f CMakeFiles/cmake_static_block.dir/build.make CMakeFiles/cmake_static_block.dir/source/block.o
.PHONY : source/block.o

# target to preprocess a source file
source/block.i:
	$(MAKE) -f CMakeFiles/cmake_shared_block.dir/build.make CMakeFiles/cmake_shared_block.dir/source/block.i
	$(MAKE) -f CMakeFiles/cmake_static_block.dir/build.make CMakeFiles/cmake_static_block.dir/source/block.i
.PHONY : source/block.i

# target to generate assembly for a file
source/block.s:
	$(MAKE) -f CMakeFiles/cmake_shared_block.dir/build.make CMakeFiles/cmake_shared_block.dir/source/block.s
	$(MAKE) -f CMakeFiles/cmake_static_block.dir/build.make CMakeFiles/cmake_static_block.dir/source/block.s
.PHONY : source/block.s

# Help Target
help:
	@echo "The following are some of the valid targets for this Makefile:"
	@echo "... all (the default if no target is provided)"
	@echo "... clean"
	@echo "... depend"
	@echo "... rebuild_cache"
	@echo "... cmake_static_program"
	@echo "... edit_cache"
	@echo "... cmake_shared_block"
	@echo "... cmake_dynamic_program"
	@echo "... cmake_static_block"
	@echo "... program.o"
	@echo "... program.i"
	@echo "... program.s"
	@echo "... source/block.o"
	@echo "... source/block.i"
	@echo "... source/block.s"
.PHONY : help



#=============================================================================
# Special targets to cleanup operation of make.

# Special rule to run CMake to check the build system integrity.
# No rule that depends on this can have commands that come from listfiles
# because they might be regenerated.
cmake_check_build_system:
	$(CMAKE_COMMAND) -H$(CMAKE_SOURCE_DIR) -B$(CMAKE_BINARY_DIR) --check-build-system CMakeFiles/Makefile.cmake 0
.PHONY : cmake_check_build_system
```

Running the '''cmake ../''' in the dircetory ```./build/``` will give:
![cmake1](./pictures/cmake1.png)
![cmake2](./pictures/cmake2.png)

**Compare** the sizes of shared and static versions of my program, we have:
![size](./pictures/size.png)
The dynamic program has the size of 8296 bytes, and the static program has 8464 (which is slightly larger). Both CMakeLists.txt and Make give the consistent result.
