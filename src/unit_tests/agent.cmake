# Find the shieldnetdefend shared library
find_library(SHIELDNETDEFENDEXT NAMES libshieldnetdefendext.dylib HINTS "${SRC_FOLDER}")
if(SHIELDNETDEFENDEXT)
  set(uname "Darwin")
else()
  set(uname "Linux")
endif()
find_library(SHIELDNETDEFENDEXT NAMES libwazuhext.so HINTS "${SRC_FOLDER}")

if(NOT SHIELDNETDEFENDEXT)
    message(FATAL_ERROR "libshieldnetdefendext not found! Aborting...")
endif()

# Add compiling flags and set tests dependencies
if(${uname} STREQUAL "Darwin")
    set(TEST_DEPS ${SHIELDNETDEFENDLIB} ${SHIELDNETDEFENDEXT} -lpthread -ldl -fprofile-arcs -ftest-coverage)
    add_compile_options(-ggdb -O0 -g -coverage -DTEST_AGENT -I/usr/local/include -DENABLE_SYSC -DSHIELDNET_DEFEND_UNIT_TESTING)
else()
    link_directories("${SRC_FOLDER}/syscheckd/build/lib/")
    add_compile_options(-ggdb -O0 -g -coverage -DTEST_AGENT -DENABLE_AUDIT -DINOTIFY_ENABLED -fsanitize=address -fsanitize=undefined)
    link_libraries(-fsanitize=address -fsanitize=undefined)
    set(TEST_DEPS ${SHIELDNETDEFENDLIB} ${SHIELDNETDEFENDEXT} -lpthread -lcmocka -ldl -lfimebpf -fprofile-arcs -ftest-coverage)
endif()

if(NOT ${uname} STREQUAL "Darwin")
  add_subdirectory(client-agent)
  add_subdirectory(logcollector)
  add_subdirectory(os_execd)
endif()

add_subdirectory(shieldnet_defend_modules)
