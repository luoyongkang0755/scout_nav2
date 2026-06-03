from setuptools import setup

package_name = 'scout_mini_dual_lidar_gazebo'

setup(
    name=package_name,
    version='0.1.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch',
            ['launch/scout_mini_gazebo.launch.py']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Agilex Robotics',
    maintainer_email='scout@agilex.ai',
    description='Gazebo simulation package for Scout Mini with dual LiDAR',
    license='BSD',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
