cmake_minimum_required(VERSION 3.8)
project(icir_panda_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config meshes robots
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
