from direct.directbase import DirectStart
from direct.showbase import DirectObject
from panda3d.ode import *
from panda3d.core import BitMask32, CardMaker, Vec3, Vec4, Quat, AmbientLight, DirectionalLight
from random import randint, random
from direct.gui.OnscreenText import OnscreenText
import random
import math

numStairs = 10 # do not change, value is dependent on models
numLimbs = 5

agentInitX = 1
agentInitY= -3
agentInitZ = 0.5

class Actions:
    FLIPU = 0
    FLIPD = 1
    TWISTL = 2
    TWISTR = 3
    
Action = Actions()


agent1j1 = [0,1,0,1]
agent1j2 = [0,1,0,1]
agent1j3 = [0,1,0,1]
agent1j4 = [1,0,1,0]
agent1 = [agent1j1, agent1j2, agent1j3, agent1j4]

torques = [(0, 20000), (0, -20000), (20000, 0), (-20000, 0)]
    
class EventListener(DirectObject.DirectObject):
    def __init__(self, joints):
        self.accept('mouse1', self.addForce)
        self.accept('mouse3', self.addForce2)
        self.joints = joints
    def addForce(self):
        joints[0].add_torques(0, 20000)
        print 'Added Force'
    def addForce2(self):
        joints[0].add_torques(20000, 0)
        print 'Added Force 2'
        
    

def createLimb(limbs, x, y, z, model, r, g, b, world, rand):
    boxNP = model.copyTo(render)
    boxNP.setPos(x, y, z)
    boxNP.setColor(r, g, b, 1)
    if rand:
        boxNP.setHpr(randint(-45, 45), randint(-45, 45), randint(-45, 45))
    # Create the body and set the mass
    boxBody = OdeBody(world)
    M = OdeMass()
    M.setBox(50, 2, 1, 1)
    boxBody.setMass(M)
    boxBody.setPosition(boxNP.getPos(render))
    boxBody.setQuaternion(boxNP.getQuat(render))
    # Create a BoxGeom
    boxGeom = OdeBoxGeom(space, 2, 1, 1)
    boxGeom.setCollideBits(BitMask32(0x00000006))
    boxGeom.setCategoryBits(BitMask32(0x00000001))
    boxGeom.setBody(boxBody)
    limbs.append((boxNP, boxBody))
    
def createStair(stairs, model, x, y, z, height, r, g, b, prevStair):
    s1NP = model.copyTo(render)
    s1NP.setPos(x, y, z)
    s1NP.setColor(r, g, b, 1)
    
    s1Body = OdeBody(world)
    M = OdeMass()
    M.setBox(50, 100, 2, height)
    s1Body.setMass(M)
    #s1Body.setPosition(Vec3(x,y,z))
    s1Body.setPosition(s1NP.getPos(render))
    s1Body.setQuaternion(s1NP.getQuat(render))
    
    # Create a BoxGeom
    stair1Geom = OdeBoxGeom(space, 100, 2, height)
    stair1Geom.setBody(s1Body)
    #stairs.append(s1Body)
    stairs.append((s1NP, s1Body))

# Setup our physics world
world = OdeWorld()
world.setGravity(0, 0, -9.81)
 
# The surface table is needed for autoCollide
world.initSurfaceTable(2)
world.setSurfaceEntry(0, 0, 150, 0.2, 9.1, 0.9, 0.00001, 0.0, 0.002)

# Create a space and add a contactgroup to it to add the contact joints
space = OdeSimpleSpace()
space.setAutoCollideWorld(world)
contactgroup = OdeJointGroup()
space.setAutoCollideJointGroup(contactgroup)
 
# Load the box model
box = loader.loadModel("box")
# Make sure its center is at 0, 0, 0 like OdeBoxGeom
box.setPos(-.5, -.5, -.5)
box.flattenLight() # Apply transform
box.setTextureOff(1)# Set texture off

# Load the rectangle model
rect = loader.loadModel("rectangle")
# Make sure its center is at 0, 0, 0 like OdeBoxGeom
rect.setPos(-1, -.5, -.5)
rect.flattenLight() # Apply transform
rect.setTextureOff(1) # Set texture off

# Create Ambient Light
ambientLight = AmbientLight('ambientLight')
ambientLight.setColor(Vec4(0.7, 0.7, 0.7, 1))
ambientLightNP = render.attachNewNode(ambientLight)
render.setLight(ambientLightNP)

# Directional Light
directionalLight = DirectionalLight('directionalLight')
directionalLight.setColor(Vec4(1, 1, 1, 0.5))
directionalLightNP = render.attachNewNode(directionalLight)
# This light is facing backwards, towards the camera.
directionalLightNP.setHpr(180, -20, 0)
render.setLight(directionalLightNP)
 
# Add a number of limbs and joints
limbs = []
joints = []

for i in range(0, numLimbs):
    createLimb(limbs, i*1.75+agentInitX, agentInitY, agentInitZ, rect, (i+1)%2, 0, (i%2), world, False)

for i in range(0, numLimbs-1):
    joint = OdeUniversalJoint(world)
    joint.attach(limbs[i][1], limbs[i+1][1])
    joint.setAnchor(limbs[i][0].getX()+1, limbs[i][0].getY(), limbs[i][0].getZ())
    joint.setParamLoStop(0, -1)
    joint.setParamLoStop(1, -1)
    joint.setParamHiStop(0, 1)
    joint.setParamHiStop(1, 1)
    joints.append(joint)

# Add stairs
stairs = []
stairmodels = []

for i in range (0, numStairs):
    stairname = "s" + str(i)
    stair = loader.loadModel(stairname)
    # Make sure its center is at 0, 0, 0 like OdeBoxGeom
    stair.setPos(-50, -1, -(float(i)+1)/2)
    stair.flattenLight() # Apply transform
    stair.setTextureOff(1) # Set texture off
    stairmodels.append(stair)
    
    if(i > 0):
        createStair(stairs, stairmodels[i], 0, i*2, (i+1)*0.5, i+1, 0.7, 0.7, 0.7, None)
        joint = OdeUniversalJoint(world)
        joint.attach(stairs[i][1], stairs[i-1][1])
        joint.setAnchor(stairs[i][0].getX()+1, stairs[i][0].getY(), stairs[i][0].getZ())
        joint.setParamLoStop(0, 0)
        joint.setParamLoStop(1, 0)
        joint.setParamHiStop(0, 0)
        joint.setParamHiStop(1, 0)
        joints.append(joint)

    else:
        createStair(stairs, stairmodels[i], 0, i*2, (i+1)*0.5, i+1, 0.7, 0.7, 0.7, None)

# Add a plane to collide with
cm = CardMaker("ground")
cm.setFrame(-50, 50, -50, 50)
ground = render.attachNewNode(cm.generate())
ground.setPos(0, 0, 0); ground.lookAt(0, 0, -1)
groundGeom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
groundGeom.setCollideBits(BitMask32(0x00000005))
groundGeom.setCategoryBits(BitMask32(0x00000002))

# Set trackball position (can only have mouse or camera control, not both)
base.trackball.node().setPos(0, 70, 0)
base.trackball.node().setHpr(-50, 20, 20)

# Setup trackball onscreen text
TrackballLoc = OnscreenText(text = str(base.trackball.node().getPos()), pos = (-0.8, 0.8), scale = 0.06)
TrackballRot = OnscreenText(text = str(base.trackball.node().getHpr()), pos = (-0.8, 0.9), scale = 0.06)
# getPos is in the form: x, y, z. You can do limbs[1][1].getPosition().getZ() to get z for example
Pos = OnscreenText(text = str(limbs[1][1].getPosition()), pos = (-0.8, 0.7), scale = 0.06)

count = 0
moveCount = 0
# The task for our simulation
def simulationTask(count, moveCount, agent1, task):
    # Setup the contact joints
    space.autoCollide() 
    # Step the simulation and set the new positions
    world.quickStep(globalClock.getDt())
    for np, body in limbs:
        np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
        
    for np, body in stairs:
        np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
    
    
    if (count[0] % 50 == 0):    
        print "---------------------"
        print "iteration" + str(count[0]/50)
        print "---------------------"
    
    if count[0] == 500:
        quit()
    ''' 
    if (moveCount[0] == 200):
        joints[0].add_torques(torques[agent1[0][moveCount[0]%4]][0], torques[agent1[0][moveCount[0]%4]][1])
        joints[1].add_torques(torques[agent1[1][moveCount[0]%4]][0], torques[agent1[1][moveCount[0]%4]][1])
        joints[2].add_torques(torques[agent1[2][moveCount[0]%4]][0], torques[agent1[2][moveCount[0]%4]][1])
        joints[3].add_torques(torques[agent1[3][moveCount[0]%4]][0], torques[agent1[3][moveCount[0]%4]][1])
        moveCount[0] = 0
    '''
    for joint in joints:
        joint.add_torques(random.randint(-2000, 2000), random.randint(-2000, 2000))
    # Update text  
    TrackballLoc.setText(str(base.trackball.node().getPos()))
    TrackballRot.setText(str(base.trackball.node().getHpr()))
    Pos.setText(str(limbs[0][1].getPosition()))
    contactgroup.empty() 
    count[0] = count[0] + 1
    moveCount[0] = moveCount[0] + 1
    return task.cont

#eventListener = EventListener(joints)
# Wait a second, then start the simulation  
# vars are passed as list because this is super hacky way to pass by reference in python
taskMgr.doMethodLater(1.0, simulationTask, "Physics Simulation", extraArgs = [[count], [moveCount], agent1], appendTask = True)
 
base.run()
