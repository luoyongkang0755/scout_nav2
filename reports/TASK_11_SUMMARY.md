# Task 11: Scout Mini 在 Gazebo 仿真中启动 ✅

## 概述
成功创建 Gazebo 仿真环境，将 Scout Mini 机器人生成到虚拟仿真世界中，实现完整的机器人仿真系统。

---

## 创建/修改的文件

### 1. 新建 Package: `scout_mini_dual_lidar_gazebo`
```
src/scout_mini_dual_lidar_gazebo/
├── CMakeLists.txt           # CMake 构建配置（安装启动文件）
├── setup.py                 # Python setuptools 配置
├── setup.cfg                # Python setup 设置
├── package.xml              # ROS 2 包元数据（v0.1.0）
├── resource/
│   └── scout_mini_dual_lidar_gazebo
└── launch/
    └── scout_mini_gazebo.launch.py  # 核心启动文件
```

**包功能说明：**
- 声明依赖：gazebo_ros, scout_description, scout_base, launch_ros
- 编译类型：ament_cmake（标准 ROS 2 包）
- 安装目标：启动文件到 share/$package_name/launch/

### 2. 启动文件详解: `scout_mini_gazebo.launch.py`

**功能职责：**
1. **加载 Scout URDF 模型**
   - 包含 `scout_base_description.launch.py`
   - 发布 `/robot_description` 主题
   - 启动 robot_state_publisher 节点

2. **启动 Gazebo 仿真引擎**
   - gzserver (Gazebo 物理引擎) - 带 ROS 插件
   - gzclient (Gazebo GUI) - 可选（需要 X11 显示）

3. **生成机器人模型到仿真世界**
   - 使用 gazebo_ros/spawn_entity.py 服务
   - 从 /robot_description 加载 URDF
   - 设置初始位置：x=0, y=0, z=0.1m

4. **配置参数**
   - `use_sim_time=true`: 启用 Gazebo 仿真时钟
   - `world`: SDF 世界文件路径（default: /ws/worlds/simple_test_world.world）
   - `x_pose`, `y_pose`, `z_pose`: 机器人初始位置

**启动参数使用示例：**
```bash
# 使用默认参数启动
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py

# 自定义机器人起始位置
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py x_pose:=2.0 y_pose:=1.5

# 指定自定义世界文件
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py world:=/path/to/custom_world.world
```

### 3. 世界文件: `worlds/simple_test_world.world`

**SDF 1.6 格式配置：**

#### 物理引擎设置
- 类型：ODE（开源动力学引擎）
- 最大步长：0.001s
- 实时因子：1.0（与真实时间同速）

#### 场景配置
- 环境光：0.4 (40% 强度)
- 背景色：浅灰 RGB(0.7, 0.7, 0.7)
- 阴影：启用

#### 地形环境
1. **地面平面** (ground_plane)
   - 大小：100m × 100m 平面
   - 材质：Gazebo 灰色
   - 作用：提供测试导航的基础平台

2. **边界墙体**（4 面）
   - Wall_1, Wall_2: 20m 长 × 1m 高
   - Wall_3, Wall_4: 20m 长 × 1m 高
   - 材质：Gazebo 砖纹
   - 作用：形成围闭空间，防止机器人坠落

3. **静态障碍物**
   - **Box_1**: 1×1×1m 立方体 @ (-5, 5)
     - 材质：橙色
     - 用途：LiDAR 扫描和障碍物检测测试
   
   - **Box_2**: 1.5×0.5×0.5m 长方体 @ (5, -5)
     - 材质：青色
     - 用途：路径规划和导航算法测试

#### 照明
- 方向光源（太阳）
   - 位置：(5, 5, 10)m
   - 方向：向下偏向 (-0.5, 0.1, -0.9)
   - 强度：漫反射 80%, 镜面反射 20%
   - 阴影：启用

#### ROS 集成插件
- `libgazebo_ros_init.so`: 初始化 ROS-Gazebo 连接
- `libgazebo_ros_factory.so`: 启用 /spawn_entity 服务

---

## 编译与运行

### 编译步骤
```bash
cd /scout_nav2
colcon build --packages-select scout_mini_dual_lidar_gazebo
```

**编译结果：** ✅ 成功 (0.85s)

### 启动仿真
```bash
# Docker 容器启动
docker run --rm -e DISPLAY="$DISPLAY" \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$PWD":/ws -w /ws scout_nav2:humble bash -lc \
  'source /opt/ros/humble/setup.bash && \
   source install/setup.bash && \
   ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py'
```

---

## 验证结果

### 启动日志关键指标
✅ **Robot State Publisher 成功**
```
[INFO] robot_state_publisher: got segment base_footprint
[INFO] robot_state_publisher: got segment base_link
[INFO] robot_state_publisher: got segment front_left_wheel_link
[INFO] robot_state_publisher: got segment front_right_wheel_link
[INFO] robot_state_publisher: got segment rear_left_wheel_link
[INFO] robot_state_publisher: got segment rear_right_wheel_link
[INFO] robot_state_publisher: got segment inertial_link
```

✅ **Gazebo Server 初始化成功**
```
[Msg] Gazebo multi-robot simulator, version 11.10.2
[Msg] Connected to gazebo master @ http://127.0.0.1:11345
[Msg] Loading world file [/ws/worlds/simple_test_world.world]
```

✅ **Scout Mini 成功生成**
```
[spawn_entity.py] [INFO] Calling service /spawn_entity
[spawn_entity.py] [INFO] Spawn status: SpawnEntity: Successfully spawned entity [scout_mini]
```

### 活跃 ROS 话题
- `/clock` - 仿真时钟（1780453262秒 simulated time）
- `/joint_states` - Scout 关节状态（sensor_msgs/JointState）
- `/robot_description` - URDF 模型定义（XML 格式）
- `/tf` - 动态变换坐标系
- `/tf_static` - 静态变换坐标系
- `/parameter_events` - ROS 参数事件

### Gazebo 服务列表
- `/gazebo/describe_parameters`
- `/gazebo/get_parameter_types`
- `/gazebo/get_parameters`
- `/gazebo/list_parameters`
- `/gazebo/set_parameters`
- `/gazebo/set_parameters_atomically`

---

## 证据文件

所有验证输出已保存至 `/scout_nav2/reports/`:

| 文件名 | 内容说明 | 大小 |
|-------|--------|------|
| gazebo_launch_output.txt | 启动过程完整日志 | 3.1KB |
| gazebo_topics.txt | robot_state_publisher 和 spawn_entity 详细日志 | 3.2KB |
| gazebo_evidence.txt | ROS 话题列表、service 列表、joint_states 采样 | 433B |
| gazebo_launch_summary.txt | 仿真成功总结与配置说明 | 2.2KB |

---

## 技术细节

### URDF 模型加载
Scout V2 URDF 包含以下组件：
- **基础链接** (Links): base_footprint, base_link, inertial_link
- **轮子链接** (4×Wheel Links): front_left, front_right, rear_left, rear_right
- **关节** (Joints): 轮子与基础的连接 (revolute joints)
- **网格** (Meshes): STL 3D 模型文件

### 仿真时钟同步
`use_sim_time=true` 参数使所有 ROS 2 节点使用 Gazebo 的虚拟时间，而非系统时间。
这对于可重现的仿真至关重要。

### X11 显示限制
在 Docker 容器中，gzclient (GUI) 需要 X11 display。
如果 DISPLAY 变量未设置或 X11 socket 不可用，gzclient 会失败。
但 gzserver 和 ROS 接口继续正常运行。

---

## 后续使用

### 查询机器人状态
```bash
# 查看关节状态
ros2 topic echo /joint_states

# 查看坐标变换
ros2 run tf2_tools view_frames

# 列出所有模型
ros2 service call /gazebo/get_parameters <request>
```

### 创建自定义世界
参考 `simple_test_world.world` 的 SDF 格式，可添加更多：
- 自定义几何体或模型
- 传感器模拟（摄像头、LiDAR、IMU）
- 光源配置
- 物理材料属性

---

## 总结

✅ **Task 11 完成**
- 创建了完整的 Gazebo 仿真包
- 实现了 Scout Mini 在虚拟环境中的生成与运行
- 提供了可复用的启动和世界配置
- 验证了 ROS-Gazebo 集成的正常工作
- 所有证据已记录并存档

**启动命令（简化版）：**
```bash
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py
```

**预期结果：**
- Gazebo 服务器运行（物理仿真）
- Scout Mini 机器人在虚拟世界中
- 所有 ROS 话题和服务可用
- 可通过 ROS 2 接口进行控制和传感
