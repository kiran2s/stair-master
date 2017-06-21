import math
import random
from random import randint, random
import os

from direct.gui.OnscreenText import OnscreenText

from direct.showbase.ShowBase import ShowBase
from direct.showbase import DirectObject
from direct.task import Task
from panda3d.ode import *
from panda3d.core import BitMask32, CardMaker, Vec3, Vec4, Quat, AmbientLight, DirectionalLight

class Agent:
    NUM_LIMBS = 5
    NUM_JOINTS = NUM_LIMBS - 1
    INIT_X = 1
    INIT_Y = -11
    INIT_Z = 0.5
    INIT_ORIENTATION = [90, 0, 0]

    def __init__(self, render, world, space, model):
        self.limbs = []
        self.joints = []
        self.density = 50
        self.lx = 2
        self.ly = 1
        self.lz = 1

        # Add limbs
        for i in range(Agent.NUM_LIMBS):
            self.limbs.append(self.createLimb(render, world, space, model, Agent.INIT_X, i*1.75 + Agent.INIT_Y, Agent.INIT_Z, (i + 1) % 2, 0, i % 2))

        # Add joints
        for i in range(Agent.NUM_LIMBS - 1):
            self.joints.append(self.createJoint(world, self.limbs[i], self.limbs[i+1]))

    def createLimb(self, render, world, space, model, x, y, z, r, g, b):
        # Model to draw
        boxNP = model.copyTo(render)
        boxNP.setPos(x, y, z)
        boxNP.setColor(r, g, b, 1)
        boxNP.setHpr(Agent.INIT_ORIENTATION[0], Agent.INIT_ORIENTATION[1], Agent.INIT_ORIENTATION[2])

        # Create the body and set the mass
        boxBody = OdeBody(world)
        boxMass = OdeMass()
        boxMass.setBox(self.density, self.lx, self.ly, self.lz)
        boxBody.setMass(boxMass)
        boxBody.setPosition(boxNP.getPos(render))
        boxBody.setQuaternion(boxNP.getQuat(render))

        # Create box geometry
        boxGeom = OdeBoxGeom(space, self.lx, self.ly, self.lz)
        boxGeom.setCollideBits(BitMask32(0x00000006))
        boxGeom.setCategoryBits(BitMask32(0x00000001))
        boxGeom.setBody(boxBody)

        return (boxNP, boxBody)

    def createJoint(self, world, limb1, limb2):
        joint = OdeUniversalJoint(world)
        joint.attach(limb1[1], limb2[1])
        joint.setAnchor(limb1[0].getX(), limb1[0].getY() + 1, limb1[0].getZ())
        joint.setParamLoStop(0, -1)
        joint.setParamLoStop(1, -1)
        joint.setParamHiStop(0, 1)
        joint.setParamHiStop(1, 1)
        return joint

    def reset(self, render):
        limbCount = 0
        for np, body in self.limbs:
            np.setPos(Agent.INIT_X, limbCount*1.75 + Agent.INIT_Y, Agent.INIT_Z)
            np.setHpr(Agent.INIT_ORIENTATION[0], Agent.INIT_ORIENTATION[1], Agent.INIT_ORIENTATION[2])
            body.setPosition(np.getPos(render))
            body.setQuaternion(np.getQuat(render))
            limbCount += 1

class Stairs:
    NUM_STEPS = 10

    def __init__(self, render, world, space):
        self.steps = []
        self.joints = []
        self.density = 5
        self.lx = 100
        self.ly = 5
        self.lz = 0.5

        # Add stairs
        for i in range(Stairs.NUM_STEPS):
            stairname = "s" + str(i)
            stairModel = loader.loadModel(stairname)
            stairModel.setPos(-50, -1, -((float(i) + 1) * self.lz) / 2)
            stairModel.setScale(float(self.lx)/100, float(self.ly)/2, self.lz)
            stairModel.flattenLight()
            stairModel.setTextureOff(1)
            
            stepHeight = (i + 1) * self.lz
            self.steps.append(self.createStep(render, world, space, stairModel, 0, i * self.ly, stepHeight * 0.5, stepHeight, 0.7, 0.7, 0.7))

        # Add joints
        for i in range(Stairs.NUM_STEPS - 1):
            self.joints.append(self.createJoint(world, self.steps[i], self.steps[i+1]))

    def createStep(self, render, world, space, model, x, y, z, height, r, g, b):
        # Model to draw
        stepNP = model.copyTo(render)
        stepNP.setPos(x, y, z)
        stepNP.setColor(r, g, b, 1)

        # Create the body and set the mass
        stepBody = OdeBody(world)
        stepMass = OdeMass()
        stepMass.setBox(self.density, self.lx, self.ly, height)
        stepBody.setMass(stepMass)
        stepBody.setPosition(stepNP.getPos(render))
        stepBody.setQuaternion(stepNP.getQuat(render))

        # Create box geometry
        stepGeom = OdeBoxGeom(space, self.lx, self.ly, height)
        stepGeom.setBody(stepBody)

        return (stepNP, stepBody)

    def createJoint(self, world, step1, step2):
        joint = OdeUniversalJoint(world)
        joint.attach(step1[1], step2[1])
        joint.setAnchor(step2[0].getX() + 1, step2[0].getY(), step2[0].getZ())
        joint.setParamLoStop(0, 0)
        joint.setParamLoStop(1, 0)
        joint.setParamHiStop(0, 0)
        joint.setParamHiStop(1, 0)
        return joint

class InputEventListener(DirectObject.DirectObject):
    def __init__(self, render, agent):
        self.render = render
        self.agent = agent

        self.force = 10000
        self.useNegativeForce = False

        self.accept("n", self.neg)
        self.accept("r", self.reset)
        self.accept("1", self.applyForce1)
        self.accept("2", self.applyForce2)
        self.accept("3", self.applyForce3)
        self.accept("4", self.applyForce4)
        self.accept("5", self.applyForce5)
        self.accept("6", self.applyForce6)
        self.accept("7", self.applyForce7)
        self.accept("8", self.applyForce8)

    def getSign(self):
        if (self.useNegativeForce): return -1
        else: return 1

    def neg(self):
        self.useNegativeForce = not self.useNegativeForce
        print self.useNegativeForce

    def reset(self):
        self.agent.reset(self.render)
        print "reset"

    def applyForce1(self):
        self.agent.joints[0].addTorques(self.getSign() * self.force, 0)
        print "applyForce1"

    def applyForce2(self):
        self.agent.joints[0].addTorques(0, self.getSign() * self.force)
        print "applyForce2"

    def applyForce3(self):
        self.agent.joints[1].addTorques(self.getSign() * self.force, 0)
        print "applyForce3"

    def applyForce4(self):
        self.agent.joints[1].addTorques(0, self.getSign() * self.force)
        print "applyForce4"

    def applyForce5(self):
        self.agent.joints[2].addTorques(self.getSign() * self.force, 0)
        print "applyForce5"

    def applyForce6(self):
        self.agent.joints[2].addTorques(0, self.getSign() * self.force)
        print "applyForce6"

    def applyForce7(self):
        self.agent.joints[3].addTorques(self.getSign() * self.force, 0)
        print "applyForce7"

    def applyForce8(self):
        self.agent.joints[3].addTorques(0, self.getSign() * self.force)
        print "applyForce8"

        
class StairMaster(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)

        # Setup our physics world
        self.world = OdeWorld()
        self.world.setGravity(0, 0, -9.81)

        # Setup collidable surface table
        self.world.initSurfaceTable(2)
        self.world.setSurfaceEntry(0, 0, 150, 0.2, 9.1, 0.9, 0.00001, 0.0, 0.002)

        # Create a space and add a contact group to it to add the contact joints
        self.space = OdeSimpleSpace()
        self.space.setAutoCollideWorld(self.world)
        self.contactGroup = OdeJointGroup()
        self.space.setAutoCollideJointGroup(self.contactGroup)

        # Load the box model
        '''
        box = loader.loadModel("box")
        box.setPos(-.5, -.5, -.5)
        box.flattenLight()
        box.setTextureOff(1)
        '''

        # Load the rectangle model
        rect = loader.loadModel("rectangle")
        rect.setPos(-1, -.5, -.5)
        rect.flattenLight()
        rect.setTextureOff(1)

        # Create ambient light
        ambientLight = AmbientLight('ambientLight')
        ambientLight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        ambientLightNP = self.render.attachNewNode(ambientLight)
        self.render.setLight(ambientLightNP)

        # Create directional light
        directionalLight = DirectionalLight('directionalLight')
        directionalLight.setColor(Vec4(0.7, 0.7, 0.7, 1))
        directionalLightNP = self.render.attachNewNode(directionalLight)
        directionalLightNP.setHpr(180, -20, 0)
        self.render.setLight(directionalLightNP)

        # Create agent
        self.agent = Agent(self.render, self.world, self.space, rect)

        # Create stairs
        self.stairs = Stairs(self.render, self.world, self.space)

        # Create ground
        cm = CardMaker("ground")
        cm.setFrame(-50, 50, -50, 50)
        ground = self.render.attachNewNode(cm.generate())
        ground.setPos(0, 0, 0)
        ground.lookAt(0, 0, -1)
        groundGeom = OdePlaneGeom(self.space, Vec4(0, 0, 1, 0))
        groundGeom.setCollideBits(BitMask32(0x00000005))
        groundGeom.setCategoryBits(BitMask32(0x00000002))

        # Set trackball position (can only have mouse or camera control, not both)
        base.trackball.node().setPos(0, 70, 0)
        base.trackball.node().setHpr(-50, 20, 20)

        # Setup onscreen location text
        self.agentPos = OnscreenText(text = str(self.agent.limbs[Agent.NUM_LIMBS-1][1].getPosition()), pos = (-0.8, 0.9), scale = 0.06)

        # Read signals from file
        cwd = os.getcwd()
        inputSignalsPathname = cwd + "/initialSignals.txt"
        self.yvalsPathname = cwd + "/yvals.txt"

        # Parse signals
        self.signals = []
        f_in = open(inputSignalsPathname, 'r')
        for line in f_in:
            line = line.strip()
            self.signals.append(line.split(","))
        
        self.numSignals = len(self.signals)
        self.numForcesPerSignal = len(self.signals[0])
        self.forceCount = 0
        self.simulationCount = 0
        self.simLoopCount = 0

        self.lastSimulationTime = 0
        self.timeBetweenSimulationUpdates = 0.07

        # Setup keyboard inputs
        InputEventListener(self.render, self.agent)

        # Schedule simulation and render loop
        self.taskMgr.doMethodLater(1.0, self.simulate, "Simulation and Rendering", extraArgs = [], appendTask = True)

    def simulate(self, task):
        diffTime = globalClock.getDt()
        currTime = globalClock.getFrameTime()

        # Setup the contact joints
        self.space.autoCollide()

        # Step the simulation and set the new position
        self.world.quickStep(diffTime)
        for np, body in self.agent.limbs:
            np.setPosQuat(self.render, body.getPosition(), Quat(body.getQuaternion()))
        for np, body in self.stairs.steps:
            np.setPosQuat(self.render, body.getPosition(), Quat(body.getQuaternion()))

        # Check if we should apply forces now
        '''
        if currTime - self.lastSimulationTime > self.timeBetweenSimulationUpdates:
            print currTime
            if self.forceCount < self.numForcesPerSignal:
                # Apply forces to all joints of agent
                for i in range(Agent.NUM_JOINTS):
                    signalIndex = Agent.NUM_JOINTS * 2 * self.simulationCount + 2 * i
                    self.agent.joints[i].addTorques(float(self.signals[signalIndex][self.forceCount]), float(self.signals[signalIndex + 1][self.forceCount]))
                self.lastSimulationTime = currTime
                self.forceCount += 1
            # Current simulation is finished
            else:
                # Write fitness result to yvals file
                f_out = open(self.yvalsPathname, 'a')
                f_out.write(str(self.agent.limbs[Agent.NUM_LIMBS-1][1].getPosition().getY()) + "\n")
                f_out.close()

                # Reset agent
                self.agent.reset(self.render)
                self.forceCount = 0
                self.simulationCount += 1
                if self.simulationCount >= self.numSignals/(Agent.NUM_JOINTS * 2):
                    return Task.done
        '''

        # Update onscreen text
        self.agentPos.setText(str(self.agent.limbs[Agent.NUM_LIMBS-1][1].getPosition()))

        self.contactGroup.empty()
        self.simLoopCount += 1

        return Task.cont


app = StairMaster()
app.run()
