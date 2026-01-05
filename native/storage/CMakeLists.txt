cmake_minimum_required(VERSION 3.10)
project(JoinlyStorage)

set(CMAKE_CXX_STANDARD 17)

add_library(joinly_storage SHARED joinly_storage.cpp)

if(WIN32)
    set_target_properties(joinly_storage PROPERTIES
        SUFFIX ".dll"
    )
endif()

install(TARGETS joinly_storage
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)