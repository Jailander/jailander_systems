strands_uol_sim
===============

This package contains files that are necessary for running STRANDS simulations on the University of Lincoln environments.


### Setting up Autonomous Patrolling Simulation

1. Calibrate charging station parameters:
   * Launch strands_datacentre:
           ```
           roslaunch ros_datacentre datacentre.launch
           
           ```
   * Launch UOL_MHT simulation:
           ```
           roslaunch strands_morse uol_mht_morse.launch
           
           ```
   * Launch scitos_docking:
           ```
           roslaunch scitos_docking charging.launch
           
           ```
   * Drive the robot to the charging station
   * Calibrate charging parameters running:
           ```
           rosrun scitos_docking visual_charging_client calibrate 100
           
           ```
2. Insert waypoints on database:
   * Launch strands_datacentre:
           ```
           roslaunch ros_datacentre datacentre.launch
           
           ```
   * Insert waypoints in DB
           ```
            rosrun topological_utils insert_map.py $(rospack find strands_uol_sim)/resources/mht.tpl robolab mht
           ```
   NOTE: You can also create your own topological map following the instructions on: https://github.com/strands-project/strands_navigation/tree/hydro-devel/topological_navigation

### Launching Autonomous Patrolling Simulation

If all previous steps are done launch simulation by running:

       ```
       roslaunch strands_uol_sim mht_sim.launch
   
       ```
