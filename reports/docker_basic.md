# Docker 基本说明

## 什么是 Docker
Docker 是一个开源的容器化平台，它将应用及其运行时依赖（库、配置、系统工具）打包到一个轻量级、可移植的镜像中，运行时在宿主机内核上以隔离的进程（容器）运行。容器提供了类似虚拟机的隔离性，但更节省资源、启动更快。

## 为何使用 Docker
- 环境一致性：开发、测试和生产使用相同镜像，避免“在我机器能跑”的问题。  
- 便捷部署：镜像可版本化、存储与分发，易于 CI/CD 集成。  
- 资源高效：比虚拟机更轻量，启动速度快。  
- 隔离性：不同服务或项目互相隔离，减少冲突与依赖污染。

## 本项目 `docker/Dockerfile` 安装了什么（要点）
- 基础镜像：`ros:humble-ros-base`（ROS 2 Humble 的基础运行镜像）。

- 系统级包（通过 apt 安装）：
  - 构建与开发工具：`build-essential`, `cmake`, `git`。  
  - Python 与打包工具：`python3-pip`。  
  - ROS 构建与依赖工具：`python3-colcon-common-extensions`, `python3-rosdep`（用于构建 ROS 工作区与解析 package 依赖）。
  - 其它工具：`curl`, `wget`, `lsb-release`, `gnupg2` 等。

- rosdep：
  - 在镜像中执行 `rosdep init`（如果尚未初始化）并运行 `rosdep update`，随后使用 `rosdep install` 根据 `package.xml` 自动安装系统依赖。

- Python 包管理：
  - 在镜像内显式升级并固定 `setuptools` 版本（当前固定为 `67.8.0`），并安装 `wheel`，以兼容项目中 `setup.py` 的可编辑/打包行为，避免构建时报 `--editable` 相关错误。  
  - 若 `src/requirements.txt` 存在，会在镜像构建阶段安装其中列出的 Python 依赖。

- 复制源码并构建工作区：
  - 将仓库根的 `src/` 复制到镜像的 `/ws/src`（构建上下文需为仓库根）。
  - 在镜像内运行 `colcon build --symlink-install` 构建 ROS 工作区并生成 `install/`。`--symlink-install` 对于开发镜像有利（使安装产物指向源码）。

- 入口脚本与默认命令：
  - 将 `docker/ros_entrypoint.sh` 复制为 `/ros_entrypoint.sh`，容器启动时会 `source /opt/ros/humble/setup.bash` 与工作区 `install/setup.bash`（若存在），默认进入 `bash`，或执行传入命令。

## 如何构建与运行
```bash
# 在项目根目录执行：
docker build -t scout_nav2:humble -f docker/Dockerfile .

# 运行容器
docker run --rm -it --network host -e DISPLAY="$DISPLAY" -v /tmp/.X11-unix:/tmp/.X11-unix -v "$PWD":/ws -w /ws scout_nav2:humble bash
```




