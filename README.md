# DROK_CK

ROS 2 및 Gazebo Classic 환경에서 동작하는 DROK_CK 트랙형 로봇 시뮬레이션 패키지입니다.

이 저장소는 로봇 모델(URDF), 메시(mesh), Gazebo 설정, 런치 파일을 포함하며, 실제 로봇 제어 파이프라인을 시뮬레이션 환경에서 미리 검증하는 데 사용합니다.

## 포함 내용

- URDF 기반 로봇 모델
- Gazebo 시뮬레이션용 launch 파일
- STL 메시 및 텍스처 자원
- 제어 및 시뮬레이션 설정 파일

## 디렉터리 구조

- `src/drok_gazebo/` : 메인 패키지 폴더
- `build/` : colcon 빌드 결과
- `install/` : 설치 결과물
- `log/` : 빌드/실행 로그

## 요구사항

- Ubuntu 22.04
- ROS 2 Humble
- Gazebo Classic 11
- colcon

## 빌드

```bash
source /opt/ros/humble/setup.bash
cd /home/ams7725/yunjae/Gazebo/DROK_CK
colcon build --packages-select drok_gazebo
source install/setup.bash
```

## 실행

```bash
ros2 launch drok_gazebo <launch_file_name>.launch.py
```

예시:

```bash
ros2 launch drok_gazebo gazebo.launch.py
```

## 참고

자세한 패키지 설명과 사용 예시는 다음 경로를 참고하세요.

- `src/drok_gazebo/README.md`
