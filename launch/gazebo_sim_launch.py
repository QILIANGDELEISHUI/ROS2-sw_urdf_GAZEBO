import launch
import launch_ros
from launch.actions import SetEnvironmentVariable,ExecuteProcess
from ament_index_python.packages import (
    get_package_share_directory,
)  # 通过包名称返回包的路径
import os


def generate_launch_description():

    # 获取默认的urdf路径
    # 通过工具函数获取‘move_cpp’包的共享目录路径。共享目录是指install安装目录，所需要的内容需要早CMakeList中进行配置
    urdf_package_path = get_package_share_directory("move_cpp")
    # 使用os进行路径拼接
    default_urdf_path = os.path.join(urdf_package_path, "urdf", "move_cpp.urdf")
    default_gazebo_world_path = os.path.join(urdf_package_path, "world", "room.world")

    # os.environ['WORKON_HOME']=["value"]
    # 设置 GAZEBO_MODEL_PATH 环境变量
    # /home/star/ros2_ws/install/move_cpp/share/move_cpp/meshes
    # os.environ["GAZEBO_MODEL_PATH"] = os.path.join(urdf_package_path, "meshes")

    set_model_path = SetEnvironmentVariable(
        name="GAZEBO_MODEL_PATH",
        value=os.path.join(urdf_package_path, "meshes"),
    )
    # set_resource_path = SetEnvironmentVariable(name="GAZEBO_RESOURCE_PATH", value="")
    # 通过文件路径获取内容 并转换成参数值对象，以供传入robot_state_publisher
    # 替换命令函数。执行命令行指令cat，并将输出使用字符串替换。该函数的返回值是一个函数对象/操作，而非具体的值
    # LaunchConfiguration是参数替换，在运行时，model会被替换为实际的urdf路径
    substitutions_command_result = launch.substitutions.Command(
        ["cat ", default_urdf_path]
    )

    # 节点启动参数parameters在传参的时候需要一个确定的值，所以使用ParameterValue方法进行类型转换
    robot_descriptions_value = launch_ros.parameter_descriptions.ParameterValue(
        substitutions_command_result, value_type=str
    )

    # 启动节点robot_state_publisher urdf内容发布
    action_robot_state_publisher = launch_ros.actions.Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_descriptions_value}],
    )
    # start_gazebo_cmd=ExecuteProcess(
    #     cmd=["gazebo","--verbose","-s","libgazebo_ros_init.so","-s","libgazebo_ros_factory.so"],
    #     output="screen"
    # )
    # 在launch文件中启动其他launch文件
    # IncludeLaunchDescription只有一个关键参数 launch_description_sources 用于指定包含的launch文件的位置和格式
    action_launch_gazebo = launch.actions.IncludeLaunchDescription(
        # 由于在ROS2中支持多种launch格式，所以此处需要使用launch_description_sources下的特定方法
        # 使用PythonLaunchDescriptionSource来指定此次传递的launch_description_sources为python启动描述源
        launch.launch_description_sources.PythonLaunchDescriptionSource(
            # 如果传递的参数是字符串列表，Python会自动拼接列表中的所有字符串
            [get_package_share_directory("gazebo_ros"), "/launch", "/gazebo.launch.py"]
        ),
        launch_arguments=[("world", default_gazebo_world_path), ("verbose", "true")],
    )
    # 启动节点spawn_entity内容发布
    action_spawn_entity = launch_ros.actions.Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "/robot_description", "-entity", "Robot"],
    )

    return launch.LaunchDescription(
        [
            set_model_path,
            # set_resource_path,
            # 启动节点robot_state_publisher
            action_robot_state_publisher,
            # 启动gazebo的launch文件
            action_launch_gazebo,
            # 启动 spawn_entity将机器人加载到gazebo中
            action_spawn_entity,
        ]
    )
