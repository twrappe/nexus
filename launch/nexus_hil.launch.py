"""Hardware-in-the-loop NEXUS validation launch file (FM-02, FM-08).

Adds micro-ROS agent bridge and STM32 edge node to the validation stack.

Usage:
    ros2 launch nexus nexus_hil.launch.py port:=/dev/ttyUSB0
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    port_arg = DeclareLaunchArgument("port", default_value="/dev/ttyUSB0")
    # TODO: add micro-ROS agent node and remaining nodes
    return LaunchDescription([port_arg])
