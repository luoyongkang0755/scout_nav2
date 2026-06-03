this is my scout_nav2_dual_lidar assignment,i will complete it

## 从 Docker 运行 GUI 工具

本仓库已支持在 Docker 容器中运行 ROS GUI 工具，如 `rviz2` 和 `gazebo`。请确保宿主机已经配置 X11 服务器，并打开了本地显示权限。

### 使用脚本运行
```bash
cd /scout_nav2/docker
bash run_container.sh
```

### 使用 Docker Compose 运行
```bash
cd /scout_nav2/docker
export DISPLAY=${DISPLAY}
export XAUTHORITY=${XAUTHORITY:-$HOME/.Xauthority}
docker compose up --build
```

### 启动 GUI 软件验证
容器内运行：
```bash
rviz2
gazebo  # 或 gz sim
```

如果宿主机使用 X11 访问控制，运行前可能需要：
```bash
xhost +local:root
```
