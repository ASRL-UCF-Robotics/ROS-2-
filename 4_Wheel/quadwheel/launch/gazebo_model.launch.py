import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ros_gz_bridge.actions import RosGzBridge
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import Command, LaunchConfiguration
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
import xacro
import launch
import launch_ros

#Launching
def generate_launch_description():
    
    # this name has to match the robot name in the Xacro file
    robotXacroName='4_wheel_omni'
    
    # this is the name of our package, at the same time this is the name of the 
    # folder that will be used to define the paths
    namePackage = 'quadwheel'
    
    # this is a relative path to the xacro file defining the model
    modelFileRelativePath = 'model/main.xacro'
    # this is a relative path to the Gazebo world file
    worldFileRelativePath = 'model/empty_world.world'
    
    # this is the absolute path to the model
    pathModelFile = os.path.join(get_package_share_directory(namePackage),modelFileRelativePath)

    # this is the absolute path to the world model
    pathWorldFile = os.path.join(get_package_share_directory(namePackage),worldFileRelativePath)
    # get the robot description from the xacro model file
    robotDescription = xacro.process_file(pathModelFile).toxml()

    # Find Package Possibly
    ros_gz_sim = get_package_share_directory('ros_gz_sim')    

    # this is the launch file from the ros_gz package
    ros_gzPackageLaunch=PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'),
                                                                       'launch','gz_sim.launch.py'))
    # this is the launch description   
    gazeboLaunch=IncludeLaunchDescription(ros_gzPackageLaunch,launch_arguments={'world': pathWorldFile}.items())
  
    # here, we create a ros_gz Node 
    spawnModelNode = Node(package='ros_gz_sim', executable='create',
                          arguments=['-topic','robot_description','-name', robotXacroName],output='screen')
    
    # Robot State Publisher Node
    nodeRobotStatePublisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robotDescription,
        'use_sim_time': True}] 
    )

    ##RVIZ2 Component
    #Joint State Publisher Node
    joint_state_publisher_node = launch_ros.actions.Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        name='joint_state_publisher',
        parameters=[{'robot_description': robotDescription,'use_sim_time': True}],
        
    )
    joint_state_publisher_gui_node = launch_ros.actions.Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher_gui',
        
    )
    #RVIZ2 Launch
    rviz = os.path.join(get_package_share_directory('quadwheel'), 'model.rviz')
    nodeRVIZ2 = Node(
    	package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen'
    
    )
    # here we create an empty launch description object
    launchDescriptionObject = LaunchDescription()
     
    # we add gazeboLaunch 
    launchDescriptionObject.add_action(gazeboLaunch)
    
    # we add the nodes
    launchDescriptionObject.add_action(spawnModelNode)
    launchDescriptionObject.add_action(nodeRobotStatePublisher)
    launchDescriptionObject.add_action(joint_state_publisher_node)
    launchDescriptionObject.add_action(joint_state_publisher_gui_node)
    launchDescriptionObject.add_action(nodeRVIZ2)
    

    return launchDescriptionObject


