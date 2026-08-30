cmake_minimum_required(VERSION 3.8)
project(icir_robotiq_2f_85_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch meshes meshes_aprice urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
