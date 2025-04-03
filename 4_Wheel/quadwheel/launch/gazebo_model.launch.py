# Gazebo Launch File for Quadwheel Base
# Created By Bastian Weiss
#---------------------------------------------
# Desired Output: Creates quadwheel model in rviz and gazebo.
#---------------------------------------------

# Imports
# For os path commands
import os

# Importing Model and world and launch files
from ament_index_python.packages import get_package_share_directory

# Import Ros Launch
import launch_ros
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

# Core structure
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, TextSubstitution

# Gazebo
from ros_gz_bridge.actions import RosGzBridge
from ros_gz_sim.actions import GzServer

# Xacro
import xacro

#----------------------------------------------------------------------------
# Launch
def generate_launch_description():

	# Names
	package_name = 'quadwheel'
	robot_name = '4_wheel_omni'
	world_name = 'lab_world.world'
	urdf_name = 'main.xacro'
	urdf_folder_name = 'model'

	#-------------------------------------------------------------------------------
	# Variables
	world = LaunchConfiguration('world') 
	
	# Paths
	path_to_urdf = os.path.join(get_package_share_directory(package_name),urdf_folder_name,urdf_name)
	path_to_world = os.path.join(get_package_share_directory(package_name),urdf_folder_name,world_name)

	# Robot Description 
	robot_description = xacro.process_file(path_to_urdf).toxml()
	
	#Find ros_gz_sim package
	pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
	gz_launch_path = PythonLaunchDescriptionSource(os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'))

	#Launch Configs
	declare_world_cmd = DeclareLaunchArgument(
    		name='world',
    		default_value=path_to_world,
    		description='Full path to the world model file to load'
	)

	# Launch Gazebo
	gz_server = IncludeLaunchDescription(gz_launch_path,
		launch_arguments={'gz_args':path_to_world}.items(),
	)

	# Spawn Gazebo Model
	spawn_model_node = Node(package='ros_gz_sim', executable='create',
		arguments=['-topic','robot_description','-name', robot_name],output='screen')

	# Publishers
	# Robot State Publisher
	robot_state_publisher_node = launch_ros.actions.Node(
   		package='robot_state_publisher',
        	executable='robot_state_publisher',
		output='screen',
        	parameters=[{'robot_description': robot_description,
			     'use_sim_time': True,
		           }],     
	)
		
	# Joint State Publisher
	joint_state_publisher_node = launch_ros.actions.Node(
       		package='joint_state_publisher',
        	executable='joint_state_publisher',
        	name='joint_state_publisher',
        	parameters=[{'robot_description': robot_description,
			     'use_sim_time': True,
		           }],
      
   	)

	joint_state_publisher_gui_node = launch_ros.actions.Node(
        	package='joint_state_publisher_gui',
        	executable='joint_state_publisher_gui',
        	name='joint_state_publisher_gui',
	)
	
	# RVIZ
	rviz_node = Node(
    		package='rviz2',
        	executable='rviz2',
        	name='rviz2',
        	output='screen'
    	)
       
	# here we create an empty launch description object
	ld = LaunchDescription()

	# Add Launch Nodes
	ld.add_action(declare_world_cmd)
	ld.add_action(gz_server)
	ld.add_action(spawn_model_node)
	ld.add_action(robot_state_publisher_node)
	ld.add_action(joint_state_publisher_node)
	ld.add_action(joint_state_publisher_gui_node)
	ld.add_action(rviz_node)

	return ld
