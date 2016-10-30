# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 A. Ophagen
#
# Experiment with dynamically creating a labyyrinth

import MalmoPython
import os
import sys
import time

sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately

def GenCuboid(x1, y1, z1, x2, y2, z2, blocktype):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(
        y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'
#
# Generate the labyrinth, starting from the initial coordinates of the bot
# which is standing just outside the entry to the labyrinth, facing north.
#
# Remember: X increments eastwards (right in a norded system)
#           Y increments upwards (towards the sky)
#           Z increments southwards (down in a norded sytem)
#
# This labyrinth is built acc. to a labyrinth provided by "CookieFreakHD"

def GenLabyrinth(x, y, z):
    # default floor is quarz (correct path colour)
    string = GenCuboid(x-1, y-1, z-1, x+31, y-1, z-33, "quartz_block")
    # line from the left-front of the bot to the far-left end of the grid
    string += GenCuboid(x-1, y, z-1, x-1, y, z-33, "prismarine")
    # line from the far-front of the bot to the far-right end of the grid
    string += GenCuboid(x, y, z-33, x+31, y, z-33, "prismarine")
    # line from the far-left end of the grid to the near-left end of the grid
    string += GenCuboid(x+31, y, z-32, x+31, y, z-1, "prismarine")
    # line from the far-left end of the grid to the left-front of the bot
    string += GenCuboid(x+30, y, z-1, x+1, y, z-1, "prismarine")
    # left-forward cul-de-sac
    string += GenCuboid(x, y, z-4, x+2, y, z-9, "prismarine")
    string += GenCuboid(x+1, y-1, z-5, x+1, y-1, z-9, "hardened_clay")
    string += GenCuboid(x+1, y, z-5, x+1, y, z-9, "air")
    string += GenCuboid(x, y-1, z-8, x+2, y-1, z-8, "hardened_clay")
    string += GenCuboid(x, y, z-8, x+2, y, z-8, "air")
    string += GenCuboid(x, y-1, z-6, x, y-1, z-6, "hardened_clay")
    string += GenCuboid(x, y, z-6, x, y, z-6, "air")
    # left detour
    string += GenCuboid(x, y, z-10, x+3, y, z-13, "prismarine")
    string += GenCuboid(x, y-1, z-11, x+2, y-1, z-13, "sandstone")
    string += GenCuboid(x, y, z-11, x+2, y, z-13, "air")
    string += GenCuboid(x+1, y, z-12, x+1, y, z-13, "prismarine")
    # left-center mini cul-de-sacs
    string += GenCuboid(x, y, z-17, x+5, y, z-18, "prismarine")
    string += GenCuboid(x+3, y-1, z-17, x+3, y-1, z-17, "hardened_clay")
    string += GenCuboid(x+3, y, z-17, x+3, y, z-17, "air")
    string += GenCuboid(x+2, y-1, z-18, x+2, y-1, z-18, "hardened_clay")
    string += GenCuboid(x+2, y, z-18, x+2, y, z-18, "air")
    string += GenCuboid(x+4, y-1, z-18, x+5, y-1, z-18, "hardened_clay")
    string += GenCuboid(x+4, y, z-18, x+5, y, z-18, "air")
    # left-top cul-de-sac
    string += GenCuboid(x, y, z-24, x+4, y, z-31, "prismarine")
    string += GenCuboid(x, y-1, z-24, x+4, y-1, z-32, "hardened_clay")
    string += GenCuboid(x, y, z-30, x, y, z-31, "air")
    string += GenCuboid(x+1, y, z-30, x+2, y, z-30, "air")
    string += GenCuboid(x+2, y, z-28, x+2, y, z-29, "air")
    string += GenCuboid(x+1, y, z-26, x+1, y, z-28, "air")
    string += GenCuboid(x, y, z-27, x, y, z-27, "air")
    string += GenCuboid(x+2, y, z-26, x+4, y, z-26, "air")
    # dividing walls bottom left
    string += GenCuboid(x+1, y, z-2, x+6, y, z-2, "prismarine")
    string += GenCuboid(x+1, y, z-15, x+7, y, z-15, "prismarine")
    string += GenCuboid(x+4, y, z-3, x+4, y, z-8, "prismarine")
    string += GenCuboid(x+5, y, z-9, x+5, y, z-14, "prismarine")
    string += GenCuboid(x+6, y, z-4, x+6, y, z-7, "prismarine")
    string += GenCuboid(x+7, y, z-8, x+7, y, z-13, "prismarine")
    string += GenCuboid(x+8, y, z-3, x+8, y, z-6, "prismarine")
    string += GenCuboid(x+9, y, z-2, x+9, y, z-5, "prismarine")
    string += GenCuboid(x+9, y, z-7, x+9, y, z-8, "prismarine")
    return string

missionXML = '''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
            <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

              <About>
                <Summary>CookieFreakHD-Labyrinth</Summary>
              </About>

                <ServerSection>
                  <ServerInitialConditions>
                    <Time>
                        <StartTime>1000</StartTime>
                        <AllowPassageOfTime>false</AllowPassageOfTime>
                    </Time>
                    <Weather>clear</Weather>
                  </ServerInitialConditions>
                  <ServerHandlers>
                      <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
                      <DrawingDecorator>
                          ''' + GenLabyrinth(0, 56, 0) + '''
                      </DrawingDecorator>
                      <ServerQuitFromTimeUp timeLimitMs="30000"/>
                      <ServerQuitWhenAnyAgentFinishes/>
                  </ServerHandlers>
                </ServerSection>

              <AgentSection mode="Survival">
                <Name>MalmoTutorialBot</Name>
                <AgentStart>
                    <Placement x="0.5" y="56.0" z="0.5" yaw="180"/>
                    <Inventory>
                        <InventoryItem slot="8" type="diamond_pickaxe"/>
                    </Inventory>
                </AgentStart>
                <AgentHandlers>
                  <ObservationFromFullStats/>
                  <ContinuousMovementCommands turnSpeedDegs="180"/>
                  <InventoryCommands/>
                  <AgentQuitFromReachingPosition>
                    <Marker x="0.5" y="56.0" z="-33.5" tolerance="0.5" description="Goal_found"/>
                  </AgentQuitFromReachingPosition>
                </AgentHandlers>
              </AgentSection>
            </Mission>'''

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
    agent_host.parse( sys.argv )
except RuntimeError as e:
    print 'ERROR:',e
    print agent_host.getUsage()
    exit(1)
if agent_host.receivedArgument("help"):
    print agent_host.getUsage()
    exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print "Error starting mission:",e
            exit(1)
        else:
            time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission running ",

# ADD YOUR CODE HERE
# TO GET YOUR AGENT TO THE DIAMOND BLOCK

# grab diamond pick, just so Steve looks businesslike
agent_host.sendCommand("hotbar.9 1")
agent_host.sendCommand("hotbar.9 0")
# walk ahead full speed
agent_host.sendCommand("move 1")

# Loop until mission ends:
while world_state.is_mission_running:
    sys.stdout.write(".")
    time.sleep(0.1)
    world_state = agent_host.getWorldState()
    for error in world_state.errors:
        print "Error:",error.text

print
print "Mission ended"
# Mission has ended.
