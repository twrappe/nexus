"""Full NEXUS validation stack launch file.

Launches: nexus_stimulus_node, nexus_monitor_node, nexus_reporter_node,
          ai_event_detector_node (SUT), mode_controller_node (SUT).
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # TODO: populate node actions
    return LaunchDescription([])
