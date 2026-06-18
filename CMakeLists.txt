cmake_minimum_required(VERSION 3.8)

project(drok_gazebo)

find_package(ament_cmake REQUIRED)

# config, launch, meshes, urdf 폴더 안의 모든 파일을 share 공간으로 복사
install(
  DIRECTORY config launch meshes urdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
