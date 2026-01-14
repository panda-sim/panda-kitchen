import pybullet as p
import pybullet_data
import time
import os
import config
from kitchen_assets.load_franka_kitchen import loadFrankaKitchen, updateFrankaKitchen


# create simulation and place camera
physicsClient = p.connect(p.GUI)
p.setGravity(0, 0, -9.81)
p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
p.resetDebugVisualizerCamera(cameraDistance=config.cameraDistance, 
                                cameraYaw=config.cameraYaw,
                                cameraPitch=config.cameraPitch, 
                                cameraTargetPosition=config.cameraTargetPosition)

# load the environment
kitchen, kettle = loadFrankaKitchen()
urdfRootPath = pybullet_data.getDataPath()
plane = p.loadURDF(os.path.join(urdfRootPath, "plane.urdf"))

# load the robot and set its home position
panda = p.loadURDF(os.path.join(urdfRootPath,"franka_panda/panda.urdf"), 
                        basePosition=config.baseStartPosition,
                        baseOrientation=p.getQuaternionFromEuler(config.baseStartOrientationE),
                        useFixedBase=True)
home_position = config.jointStartPositions
for idx in range(len(home_position)):
    p.resetJointState(panda, idx, home_position[idx])

# run simulation
while True:
    updateFrankaKitchen(kitchen)
    p.stepSimulation()
    time.sleep(config.control_dt)