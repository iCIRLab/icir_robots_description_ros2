cmake_minimum_required(VERSION 3.8)
project(icir_panda_husky_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch meshes robots rviz
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
