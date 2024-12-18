IMPORTANT NOTES
- Catkin_make is for ROS 1, we use colcon now
- If you forget where you are, use pwd to find where the files are being made on your windows. They are usually in Linux/Ubuntu-24.04/home/NAME/HERE.

INSTALLS
- ROS 2 Jazzy
https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
- Gazebo Ionic
https://gazebosim.org/docs/latest/install_ubuntu/

STEPS
- Source ros 2 in terminal
  
`source /opt/ros/jazzy/setup.bash`

- Make build - FIX ERRORS HERE
  
`colcon build`

- Launch Gazebo
  
Empty Room

`gz sim empty.sdf`

Launch URDF

`gz service -s /world/empty/create --reqtype gz.msgs.EntityFactory --reptype gz.msgs.Boolean --timeout 1000 --req 'sdf_filename: "/home/USERHERE/FILEHERE/modelgaz.urdf", name: "urdf_model"'`
