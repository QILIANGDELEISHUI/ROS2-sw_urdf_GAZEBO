import launch
import launch_ros
from ament_index_python.packages import (
    get_package_share_directory,
)  # 通过包名称返回包的路径
import os


def generate_launch_description():
    """
    目标 启动robot_state_publisher、joint_state_publisher、rviz
    robot_state_publisher启动需要urdf文件的内容,获取内容就需要cat和文件路径
    所以先获取urdf文件路径
    """
    # 获取默认的urdf路径
    # 通过工具函数获取‘move_cpp’包的共享目录路径。共享目录是指install安装目录，所需要的内容需要早CMakeList中进行配置
    urdf_package_path = get_package_share_directory("move_cpp")
    # 使用os进行路径拼接
    default_urdf_path = os.path.join(urdf_package_path, "urdf", "move_cpp.urdf")
    # 使用launch文件启动后，将Rviz保存为文件后在添加
    # default_rviz_path = os.path.join(
    #     urdf_package_path, "config", "display_robot_mode.rviz"
    # )

    # 声明一个launch文件参数，该参数可在启动launch文件时从外部传入，这种参数在文件内部使用的时候需要使用参数替换来使用。
    # 声明一个urdf目录的参数,方便修改
    action_declare_arg_model_path = launch.actions.DeclareLaunchArgument(
        name="model",
        default_value=str(default_urdf_path),
        description="加载的模型文件路径",
    )

    # 通过文件路径获取内容 并转换成参数值对象，以供传入robot_state_publisher
    # 替换命令函数。执行命令行指令cat，并将输出使用字符串替换。该函数的返回值是一个函数对象/操作，而非具体的值
    # LaunchConfiguration是参数替换，在运行时，model会被替换为实际的urdf路径
    # 这里cat后面的空格很重要！！！
    substitutions_command_result = launch.substitutions.Command(
        ["cat ", launch.substitutions.LaunchConfiguration("model")]
    )

    # 节点启动参数parameters在传参的时候需要一个确定的值，所以使用ParameterValue方法进行类型转换
    robot_descriptions_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result, value_type=str
    )

    # 启动节点robot_state_publisher
    action_robot_state_publisher = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        # parameters 是内部参数传递
        parameters=[{"robot_description": robot_descriptions_value}],
    )
    # 启动节点joint_state_publisher
    action_joint_state_publisher = launch_ros.actions.Node(
        package="joint_state_publisher", executable="joint_state_publisher"
    )
    # 启动rviz
    action_rviz_node = launch_ros.actions.Node(
        package="rviz2",
        executable="rviz2",
        # arguments 参数使用launch文件启动后，将Rviz保存为文件后在添加
        # arguments 是命令行选项
        # arguments=["-d", default_urdf_path],
    )

    return launch.LaunchDescription(
        [
            # launch启动参数，使用时传入，或使用内部默认参数
            action_declare_arg_model_path,
            # 启动节点robot_state_publisher
            action_robot_state_publisher,
            # 启动joint_state_publisher
            action_joint_state_publisher,
            # 启动Rviz
            action_rviz_node,
        ]
    )