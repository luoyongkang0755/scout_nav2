# Task 11 快速启动指南

## 🎯 目标完成状态
✅ **TASK 11 完成** - Scout Mini 在 Gazebo 仿真中成功启动

---

## 📦 新建文件清单

### 主要文件（7个）
1. **src/scout_mini_dual_lidar_gazebo/** - 完整的 ROS 2 包
   - `package.xml` - 包依赖声明
   - `CMakeLists.txt` - 构建配置
   - `setup.py` / `setup.cfg` - Python 配置
   - `launch/scout_mini_gazebo.launch.py` - 启动脚本

2. **worlds/simple_test_world.world** - Gazebo SDF 世界文件

### 证据文件（6个）
- `reports/gazebo_launch_output.txt` - 启动日志
- `reports/gazebo_topics.txt` - 主题日志
- `reports/gazebo_evidence.txt` - 验证证据
- `reports/gazebo_launch_summary.txt` - 总结
- `reports/TASK_11_SUMMARY.md` - 完整文档
- `reports/TASK_11_FILES.txt` - 文件清单

---

## 🚀 快速启动

### 最简单的方式
```bash
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py
```

### 带 Docker
```bash
cd /scout_nav2
docker run --rm -e DISPLAY="$DISPLAY" \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v "$PWD":/ws -w /ws scout_nav2:humble bash -lc \
  'source /opt/ros/humble/setup.bash && \
   source install/setup.bash && \
   ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py'
```

---

## ✅ 启动文件功能

`scout_mini_gazebo.launch.py` 在启动时会：

1. **加载 Scout URDF 模型**
   - 源文件：scout_description/scout_v2.xacro
   - 发布话题：/robot_description
   
2. **启动 Gazebo 物理引擎**
   - gzserver - 仿真计算
   - gzclient - 可视化 (需要 X11)

3. **生成机器人到仿真世界**
   - 使用 gazebo_ros/spawn_entity 服务
   - 机器人名称：scout_mini
   - 初始位置：(0, 0, 0.1)

4. **启用仿真时钟**
   - use_sim_time=true
   - 发布 /clock 话题

---

## 📊 验证结果

启动后会看到这些关键消息：

```
✓ [robot_state_publisher] got segment base_link
✓ [robot_state_publisher] got segment front_left_wheel_link
✓ [robot_state_publisher] got segment rear_left_wheel_link
✓ [spawn_entity.py] Successfully spawned entity [scout_mini]
✓ /robot_description topic published
✓ /joint_states topic active
```

---

## 📡 可用的 ROS 话题

| 话题名 | 类型 | 说明 |
|-------|------|------|
| `/clock` | rosgraph_msgs/Clock | 仿真时间 |
| `/robot_description` | std_msgs/String | URDF 模型 |
| `/joint_states` | sensor_msgs/JointState | 关节位置/速度 |
| `/tf` | tf2_msgs/TFMessage | 变换树 |
| `/tf_static` | tf2_msgs/TFMessage | 静态变换 |

---

## 🎮 启动参数

| 参数名 | 默认值 | 说明 |
|-------|-------|------|
| `use_sim_time` | true | 使用仿真时钟 |
| `world` | /ws/worlds/simple_test_world.world | 世界文件路径 |
| `x_pose` | 0.0 | 机器人初始 X 坐标 |
| `y_pose` | 0.0 | 机器人初始 Y 坐标 |
| `z_pose` | 0.1 | 机器人初始 Z 坐标 |

### 参数使用示例
```bash
# 设置不同的初始位置
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py \
  x_pose:=2.0 y_pose:=3.0 z_pose:=0.2

# 使用自定义世界
ros2 launch scout_mini_dual_lidar_gazebo scout_mini_gazebo.launch.py \
  world:=/custom/path/world.world
```

---

## 🌍 世界环境

`simple_test_world.world` 包含：

- **地面** - 100m × 100m 平面
- **围墙** - 4 面 1m 高围闭墙
- **障碍物** - 2 个静态对象
  - Box 1: 1×1×1m 立方体 @ (-5, 5)
  - Box 2: 1.5×0.5×0.5m @ (5, -5)
- **照明** - 方向光源（太阳）
- **物理** - ODE 引擎，1000 Hz

---

## 📝 URDF 模型信息

Scout Mini URDF 包含：

**链接 (Links)**
- base_footprint - 底部参考点
- base_link - 车身
- inertial_link - 惯性参考
- front_left_wheel_link
- front_right_wheel_link
- rear_left_wheel_link
- rear_right_wheel_link

**关节 (Joints)**
- 4 个轮子革命关节 (revolute)
- 轮子与车身的连接

---

## 🔧 故障排除

### 问题：gzclient 失败
**原因** - 没有 X11 显示  
**解决** - 这是正常的。gzserver 仍在运行，可通过 ROS 2 使用

### 问题：/spawn_entity 服务不可用
**原因** - Gazebo ROS 插件未加载  
**解决** - 确保 simple_test_world.world 包含 ROS 插件

### 问题：机器人不显示
**原因** - URDF 加载失败  
**解决** - 检查 scout_description 是否正确编译

---

## 📚 更多命令

### 查看仿真中的话题
```bash
ros2 topic list
```

### 监听关节状态
```bash
ros2 topic echo /joint_states
```

### 可视化坐标变换
```bash
ros2 run tf2_tools view_frames
```

### 查看仿真参数
```bash
ros2 service call /gazebo/get_parameters
```

---

## 📄 完整文档

详细的技术文档见：`reports/TASK_11_SUMMARY.md`

---

## 🎉 总结

✅ **创建了** scout_mini_dual_lidar_gazebo ROS 2 包  
✅ **编写了** 完整的启动脚本  
✅ **创建了** Gazebo SDF 世界文件  
✅ **验证了** 仿真成功运行  
✅ **收集了** 所有证据文件  

**Scout Mini 已在 Gazebo 中成功运行！🤖**

