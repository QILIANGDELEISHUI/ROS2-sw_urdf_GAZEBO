import launch
import launch_ros.actions
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                name="world_name",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("move_cpp"), "worlds", "wpb_simple.world"]
                ),
                description="World file to load",
            ),
            DeclareLaunchArgument(
                name="paused",
                default_value="false",
                description="Start simulation paused",
            ),
            DeclareLaunchArgument(
                name="use_sim_time",
                default_value="true",
                description="Use simulation (Gazebo) clock",
            ),
            DeclareLaunchArgument(
                name="gui", default_value="true", description="Enable Gazebo GUI"
            ),
            DeclareLaunchArgument(
                name="recording",
                default_value="false",
                description="Enable Gazebo recording",
            ),
            DeclareLaunchArgument(
                name="debug", default_value="false", description="Enable debug mode"
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    [
                        PathJoinSubstitution(
                            [
                                FindPackageShare("gazebo_ros"),
                                "launch",
                                "gazebo.launch.py",
                            ]
                        )
                    ]
                ),
                launch_arguments={
                    "world": LaunchConfiguration("world_name"),
                    "paused": LaunchConfiguration("paused"),
                    "use_sim_time": LaunchConfiguration("use_sim_time"),
                    "gui": LaunchConfiguration("gui"),
                    "recording": LaunchConfiguration("recording"),
                    "debug": LaunchConfiguration("debug"),
                }.items(),
            ),
        ]
    )
