IMPORTANT NOTES
- All done in Xml
- Catkin_make is for ROS 1, we use colcon now
- If you forget where you are, use pwd to find where the files are being made on your windows. They are usually in Linux/Ubuntu-24.04/home/NAME/HERE.

STEPS
- Source ros 2 in terminal
source /opt/ros/jazzy/setup.bash

- Make build - FIX ERRORS HERE
colcon build

- Launch Gazebo
ros2 launch omni_gazebo gazebo.launch
