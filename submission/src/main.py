from direct.directbase import DirectStart
from panda3d.ode import *
from panda3d.core import BitMask32, CardMaker, Vec3, Vec4, Quat, AmbientLight, DirectionalLight
from random import randint, random
from direct.gui.OnscreenText import OnscreenText
import random

def createLimb(limbs, r, g, b, model, x, y, z, world, rand):
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

def createStair(stair, r, g, b, model, x, y, z, world, rand):
	boxNP = model.copyTo(render)
	boxNP.setPos(x, y, z)
	boxNP.setColor(r, g, b, 1)
	if rand:
		boxNP.setHpr(randint(-45, 45), randint(-45, 45), randint(-45, 45))
    # Create the body and set the mass
	boxBody = OdeBody(world)
	M = OdeMass()
	M.setBox(5, 100, 2, 1)
	boxBody.setMass(M)
	boxBody.setPosition(boxNP.getPos(render))
	boxBody.setQuaternion(boxNP.getQuat(render))
	# Create a BoxGeom
	boxGeom = OdeBoxGeom(space, 50, 2, 1)
	boxGeom.setCollideBits(BitMask32(0x00000003))
	boxGeom.setCategoryBits(BitMask32(0x00000004))
	boxGeom.setBody(boxBody)
	stair.append((boxNP, boxBody))
	

def createStairs(stairs, model, x, y, z, length, world):
	stair = []
	for i in range (0, length):
		createStair(stair, 0.7, 0.7, 0.7, model, x, y, z+i, world, False)	
	for j in range (1, len(stair)):
		joint = OdeUniversalJoint(world)
		joint.attachBodies(stair[j-1][1], stair[j][1])
		joint.setParamLoStop(0, 0)
		joint.setParamLoStop(1, 0)
		joint.setParamHiStop(0, 0)
		joint.setParamHiStop(1, 0)
	stairs.append(stair)
	

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

# Load the stair model
stair = loader.loadModel("stair")
# Make sure its center is at 0, 0, 0 like OdeBoxGeom
stair.setPos(-50, -1, -.5)
stair.flattenLight() # Apply transform
stair.setTextureOff(1) # Set texture off

# Create Ambient Light
ambientLight = AmbientLight('ambientLight')
ambientLight.setColor(Vec4(0.7, 0.7, 0.7, 1))
ambientLightNP = render.attachNewNode(ambientLight)
render.setLight(ambientLightNP)

# Directional light 01
directionalLight = DirectionalLight('directionalLight')
directionalLight.setColor(Vec4(1, 1, 1, 0.5))
directionalLightNP = render.attachNewNode(directionalLight)
# This light is facing backwards, towards the camera.
directionalLightNP.setHpr(180, -20, 0)
render.setLight(directionalLightNP)
 
# Add a number of limbs
limbs = []
createLimb(limbs, 1, 0, 0, rect, 1, 0, 3, world, False)
createLimb(limbs, 0, 0, 1, rect, 2.75, 0, 3, world, False)

# Setup joint between limbs 
joint = OdeUniversalJoint(world)
joint.attach(limbs[0][1], limbs[1][1])
joint.setAnchor(limbs[0][0].getX()+1, limbs[0][0].getY(), limbs[0][0].getZ())
joint.setParamLoStop(0, -1)
joint.setParamLoStop(1, -1)
joint.setParamHiStop(0, 1)
joint.setParamHiStop(1, 1)

'''
stairs = []
stairJoints = [] # not used right now, but can be used to attach stair parts together
for i in range(1, 11):
	createStairs(stairs, stair, 0, (i-1)*2, 0.5, i, world)
'''

s1 = CardMaker("stair1")
s1.setFrame(-50, 50, -1, 1)
stair1 = render.attachNewNode(s1.generate())
stair1.setPos(0, 0, 1); stair1.lookAt(0, 0, -1)
stair1.setColor(1, 0, 0, 1)

s2 = CardMaker("stair2")
s2.setFrame(-50, 50, -0.5, 0.5)
stair2 = render.attachNewNode(s2.generate())
stair2.setPos(0, -1, 0.5); stair2.lookAt(0, -1, 0.5)
stair2.setColor(1, 0, 0, 1)
stair2Geom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
stair2Geom.setCollideBits(BitMask32(0x00000005))
stair2Geom.setCategoryBits(BitMask32(0x00000002))

#sNP = stair.copyTo(render)
#sNP.setPos(0, 0, 1)
#sNP.setColor(1, 0, 0, 1)
	
s1Body = OdeBody(world)
M = OdeMass()
M.setBox(50, 100, 2, 1)
s1Body.setMass(M)
s1Body.setPosition(Vec3(0,0,0))
#s1Body.setQuaternion(stair1.getQuat(render))
# Create a BoxGeom
stair1Geom = OdeBoxGeom(space, 50, 2, 1)
#stair1Geom.setCollideBits(BitMask32(0x00000005))
#stair1Geom.setCategoryBits(BitMask32(0x00000002))
stair1Geom.setBody(s1Body)

#stair1Geom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
#stair1Geom.setCollideBits(BitMask32(0x00000005))
#stair1Geom.setCategoryBits(BitMask32(0x00000002))


s2 = CardMaker("stair2")
s2.setFrame(-50, 50, -0.5, 0.5)
stair2 = render.attachNewNode(s2.generate())
stair2.setPos(0, -1, 0.5); stair2.lookAt(0, -1, 0.5)
stair2.setColor(1, 0, 0, 1)
stair2Geom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
stair2Geom.setCollideBits(BitMask32(0x00000005))
stair2Geom.setCategoryBits(BitMask32(0x00000002))



# Add a plane to collide with
cm = CardMaker("ground")
cm.setFrame(-50, 50, -50, 50)
ground = render.attachNewNode(cm.generate())
ground.setPos(0, 0, 0); ground.lookAt(0, 0, -1)
groundGeom = OdePlaneGeom(space, Vec4(0, 0, 1, 0))
groundGeom.setCollideBits(BitMask32(0x00000005))
groundGeom.setCategoryBits(BitMask32(0x00000002))

# Set trackball position (can only have mouse or camera control, not both)
base.trackball.node().setPos(0, 30, 0)
base.trackball.node().setHpr(-50, 20, 20)

# Setup trackball onscreen text
TrackballLoc = OnscreenText(text = str(base.trackball.node().getPos()), pos = (-0.8, 0.8), scale = 0.06)
TrackballRot = OnscreenText(text = str(base.trackball.node().getHpr()), pos = (-0.8, 0.9), scale = 0.06)
# getPos is in the form: x, y, z. You can do limbs[1][1].getPosition().getZ() to get z for example
Pos = OnscreenText(text = str(limbs[1][1].getPosition()), pos = (-0.8, 0.7), scale = 0.06)

# The task for our simulation
def simulationTask(task):
    # Setup the contact joints
    space.autoCollide() 
    # Step the simulation and set the new positions
    world.quickStep(globalClock.getDt())
    for np, body in limbs:
        np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
	
	'''
	for s in stairs:
		for np, body in s:
			np.setPosQuat(render, body.getPosition(), Quat(body.getQuaternion()))
	'''
		
    # Update text  
	TrackballLoc.setText(str(base.trackball.node().getPos()))
	TrackballRot.setText(str(base.trackball.node().getHpr()))
	Pos.setText(str(limbs[0][1].getPosition()))
	joint.add_torques(random.randint(-2000, 2000), random.randint(-2000, 2000))
	# Clear the contact joints
    contactgroup.empty() 
    return task.cont

# Wait a second, then start the simulation  
taskMgr.doMethodLater(1.0, simulationTask, "Physics Simulation")
 
base.run()
