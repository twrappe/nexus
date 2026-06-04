"""Scenario-driven NEXUS validation launch file.

Loads a YAML scenario file and drives the full validation stack through it.

Usage:
    ros2 launch nexus nexus_scenario.launch.py scenario:=scenarios/critical_event.yaml
"""
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    scenario_arg = DeclareLaunchArgument(
        "scenario", default_value="scenarios/nominal_steady_state.yaml"
    )
    # TODO: pass scenario path to scenario_player node
    return LaunchDescription([scenario_arg])
