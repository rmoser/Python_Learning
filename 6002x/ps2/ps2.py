# 6.00.2x Problem Set 2: Simulating robots

import math
import random

import ps2_visualize
import pylab

import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
import numpy as np
import time
random.seed(0)

##################
## Comment/uncomment the relevant lines, depending on which version of Python you have
##################

# For Python 3.5:
#from ps2_verify_movement35 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.5 

# For Python 3.6:
from ps2_verify_movement36 import testRobotMovement
# If you get a "Bad magic number" ImportError, you are not using Python 3.6


# === Provided class Position
class Position(object):
    """
    A Position represents a location in a two-dimensional room.
    """
    def __init__(self, x, y):
        """
        Initializes a position with coordinates (x, y).
        """
        self.x = x
        self.y = y

    def __repr__(self):
        return str((self.x, self.y))

    def getX(self):
        return self.x
    
    def getY(self):
        return self.y
    
    def getNewPosition(self, angle, speed):
        """
        Computes and returns the new Position after a single clock-tick has
        passed, with this object as the current position, and with the
        specified angle and speed.

        Does NOT test whether the returned position fits inside the room.

        angle: number representing angle in degrees, 0 <= angle < 360
        speed: positive float representing speed

        Returns: a Position object representing the new position.
        """
        old_x, old_y = self.getX(), self.getY()
        angle = float(angle)
        # Compute the change in position
        delta_y = speed * math.cos(math.radians(angle))
        delta_x = speed * math.sin(math.radians(angle))
        # Add that to the existing position
        new_x = old_x + delta_x
        new_y = old_y + delta_y
        return Position(new_x, new_y)

    def __str__(self):  
        return "(%0.2f, %0.2f)" % (self.x, self.y)


# === Problem 1
class RectangularRoom(object):
    """
    A RectangularRoom represents a rectangular region containing clean or dirty
    tiles.

    A room has a width and a height and contains (width * height) tiles. At any
    particular time, each of these tiles is either clean or dirty.
    """
    def __init__(self, width, height):
        """
        Initializes a rectangular room with the specified width and height.

        Initially, no tiles in the room have been cleaned.

        width: an integer > 0
        height: an integer > 0
        """
        self.width = int(width)
        self.height = int(height)
        # Bool value indicates Clean (True) or Dirty (False)
        self.tiles = np.zeros(shape=(height, width), dtype=np.bool)
        self.xcoords = np.zeros(shape=self.tiles.shape, dtype=np.int)
        self.ycoords = np.zeros(shape=self.tiles.shape, dtype=np.int)
        for x in range(width):
            for y in range(height):
                # [y,x] because numpy array indices are row, column
                self.xcoords[y,x] = x
                self.ycoords[y,x] = y
        self.robots = []

    def __repr__(self):
        _tiles = self.tiles.astype(np.str)
        for robot in self.robots:
            _tiles[math.floor(robot.pos.y), math.floor(robot.pos.x)] = str(robot.direction)
        return str(_tiles[::-1, :])  # Print in standard coords, with y increasing to the north

    def cleanTileAtPosition(self, pos):
        """
        Mark the tile under the position POS as cleaned.

        Assumes that POS represents a valid position inside this room.

        pos: a Position
        """
        self.tiles[math.floor(pos.getY()), math.floor(pos.getX())] = True

    def isTileCleaned(self, m, n):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[n, m]

    def isTilePosCleaned(self, pos):
        """
        Return True if the tile (m, n) has been cleaned.

        Assumes that (m, n) represents a valid tile inside the room.

        m: an integer
        n: an integer
        returns: True if (m, n) is cleaned, False otherwise
        """
        return self.tiles[math.floor(pos.y), math.floor(pos.x)]

    def getNumTiles(self):
        """
        Return the total number of tiles in the room.

        returns: an integer
        """
        return self.width * self.height

    def getNumCleanedTiles(self):
        """
        Return the total number of clean tiles in the room.

        returns: an integer
        """
        return np.sum(self.tiles)

    def getRandomPosition(self):
        """
        Return a random position inside the room.

        returns: a Position object.
        """
        return Position(random.random() * self.width, random.random() * self.height)

    def isPositionInRoom(self, pos):
        """
        Return True if pos is inside the room.

        pos: a Position object.
        returns: True if pos is in the room, False otherwise.
        """
        return 0 <= pos.x < self.width and 0 <= pos.y < self.height


# === Problem 2
class Robot(object):
    """
    Represents a robot cleaning a particular room.

    At all times the robot has a particular position and direction in the room.
    The robot also has a fixed speed.

    Subclasses of Robot should provide movement strategies by implementing
    updatePositionAndClean(), which simulates a single time-step.
    """
    def __init__(self, room, speed):
        """
        Initializes a Robot with the given speed in the specified room. The
        robot initially has a random direction and a random position in the
        room. The robot cleans the tile it is on.

        room:  a RectangularRoom object.
        speed: a float (speed > 0)
        """
        self.room = room
        room.robots.append(self)
        self.speed = speed
#        self.direction = self.setRobotRandomDirection()
        self.direction = random.randint(0, 359)
        self.pos = room.getRandomPosition()
        room.cleanTileAtPosition(self.pos)

    def __repr__(self):
        return f"Robot pos: {self.pos}, dir: {self.direction}, speed: {self.speed}"

    def getRobotPosition(self):
        """
        Return the position of the robot.

        returns: a Position object giving the robot's position.
        """
        return self.pos
    
    def getRobotDirection(self):
        """
        Return the direction of the robot.

        returns: an integer d giving the direction of the robot as an angle in
        degrees, 0 <= d < 360.
        """
        return self.direction

    def setRobotPosition(self, position):
        """
        Set the position of the robot to POSITION.

        position: a Position object.
        """
        self.pos = position

    def setRobotDirection(self, direction):
        """
        Set the direction of the robot to DIRECTION.

        direction: integer representing an angle in degrees
        """
        self.direction = direction

    def setRobotRandomDirection(self):
        """
        Set a random direction for the robot
        """
        self.direction = random.randint(0, 359)

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        raise NotImplementedError # don't change this!


# === Problem 3
class StandardRobot(Robot):
    """
    A StandardRobot is a Robot with the standard movement strategy.

    At each time-step, a StandardRobot attempts to move in its current
    direction; when it would hit a wall, it *instead* chooses a new direction
    randomly.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        if self.room.isPositionInRoom(nextPos):
            self.setRobotPosition(nextPos)
            self.room.cleanTileAtPosition(nextPos)
        else:
            self.setRobotRandomDirection()

# Uncomment this line to see your implementation of StandardRobot in action!
# testRobotMovement(StandardRobot, RectangularRoom)


# === Problem 4
def runSimulation(num_robots, speed, width, height, min_coverage, num_trials,
                  robot_type, visualize=False):
    """
    Runs NUM_TRIALS trials of the simulation and returns the mean number of
    time-steps needed to clean the fraction MIN_COVERAGE of the room.

    The simulation is run with NUM_ROBOTS robots of type ROBOT_TYPE, each with
    speed SPEED, in a room of dimensions WIDTH x HEIGHT.

    num_robots: an int (num_robots > 0)
    speed: a float (speed > 0)
    width: an int (width > 0)
    height: an int (height > 0)
    min_coverage: a float (0 <= min_coverage <= 1.0)
    num_trials: an int (num_trials > 0)
    robot_type: class of robot to be instantiated (e.g. StandardRobot or
                RandomWalkRobot)
    """

    # random.seed(0)
    results = []

    for t in range(num_trials):
        if visualize:
            anim=ps2_visualize.RobotVisualization(num_robots, width, height, delay=0.01)
        room = RectangularRoom(width, height)
        robots = [robot_type(room, speed) for i in range(num_robots)]
        steps = 0
        while room.getNumCleanedTiles() / room.getNumTiles() < min_coverage:
            for r in robots:
                r.updatePositionAndClean()
            steps += 1
            if visualize:
                anim.update(room, robots)
        results.append(steps)
        if visualize:
            anim.done()
    return sum(results) / len(results)

# Uncomment this line to see how much your simulation takes on average
# print(runSimulation(1, 1.0, 20, 20, 0.5, 1, StandardRobot, True))


# === Problem 5
class RandomWalkRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        if self.room.isPositionInRoom(nextPos):
            self.setRobotPosition(nextPos)
            self.room.cleanTileAtPosition(nextPos)

        self.setRobotRandomDirection()

# print(runSimulation(1, 1.0, 20, 20, 0.5, 1, RandomWalkRobot, True))

class OrthogonalRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def setRobotRandomDirection(self):
        """
        Set a random direction for the robot
        """
        self.direction = random.randint(0, 3) * 90

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        if self.room.isPositionInRoom(nextPos):
            self.setRobotPosition(nextPos)
            self.room.cleanTileAtPosition(nextPos)
        self.setRobotRandomDirection()

class SeekerRobot(Robot):
    """
    A RandomWalkRobot is a robot with the "random walk" movement strategy: it
    chooses a new direction at random at the end of each time-step.
    """
    def setRobotRandomDirection(self):
        """
        Set a random direction for the robot
        """
        self.direction = random.randint(0, 3) * 90

    def nearest_dirt_direction(self):
        # Calculate Manhattan distances to each dirty tile
        distances = np.logical_not(self.room.tiles) * (np.abs(np.floor(self.pos.x) - self.room.xcoords) + np.abs(np.floor(self.pos.y) - self.room.ycoords))
        y, x = np.where(distances == np.min(distances[np.nonzero(np.logical_not(self.room.tiles))]))
        # print(x, y)
        x = x[0]
        y = y[0]
        d = math.degrees(math.atan2(y - math.floor(self.pos.y), x - math.floor(self.pos.x)))
        # Transform from standard coords to NSEW coords
        direction = round((90 - d) % 360 / 90) * 90
        #print(f"\nRoom:\n{self.room}")
        #print(f"\ndistances:\n{distances}")
        #print(f"pos: {self.pos}  facing: {self.direction}  Nearest dirt: {(x,y)}  dir: {d}->{direction}")
        #input("Press Enter")
        return direction

    def updatePositionAndClean(self):
        """
        Simulate the passage of a single time-step.

        Move the robot to a new position and mark the tile it is on as having
        been cleaned.
        """
        # Patch for init to non-orthogonal directions
        self.setRobotDirection(self.direction // 90 * 90)
        #print(f"\npos: {(self.pos.x, self.pos.y)}  dir: {self.direction}")
        # Change direction if the next tile is a clean tile or a wall
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        found_dirt = False
        if not self.room.isPositionInRoom(nextPos) or self.room.isTilePosCleaned(nextPos):
            self.setRobotDirection(self.nearest_dirt_direction())
            if False:
                for direction in range(0, 360, 90):
                    nextPos = self.getRobotPosition().getNewPosition(direction, self.speed)
                    if self.room.isPositionInRoom(nextPos) and not self.room.isTilePosCleaned(nextPos):
                        self.setRobotDirection(direction)
                        found_dirt = True
                if not found_dirt:
                    # Pick a NEW direction
                    directions = [0, 90, 180, 270]
                    directions.remove(self.direction)
                    for d in directions:
                        nextPos = self.getRobotPosition().getNewPosition(d, self.speed)
                        if not self.room.isPositionInRoom(nextPos):
                            directions.remove(d)

                    self.setRobotDirection(random.choice(directions))

        #print(self.pos, self.direction)
        #input("Press Enter...")
        nextPos = self.getRobotPosition().getNewPosition(self.getRobotDirection(), self.speed)
        self.setRobotPosition(nextPos)
        self.room.cleanTileAtPosition(nextPos)


#print(runSimulation(1, 1.0, 20, 20, 0.5, 1, OrthogonalRobot, True))

print(runSimulation(2, 1.0, 50, 50, 1, 1, SeekerRobot, True))

def showPlot1(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    num_robot_range = range(1, 11)
    times1 = []
    times2 = []
    times3 = []
    for num_robots in num_robot_range:
        print("Plotting", num_robots, "robots...")
        times1.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, StandardRobot))
        times2.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, RandomWalkRobot))
        times3.append(runSimulation(num_robots, 1.0, 20, 20, 0.8, 20, OrthogonalRobot))
    pylab.plot(num_robot_range, times1)
    pylab.plot(num_robot_range, times2)
    pylab.plot(num_robot_range, times3)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot', 'OrthogonalRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()


    
def showPlot2(title, x_label, y_label):
    """
    What information does the plot produced by this function tell you?
    """
    aspect_ratios = []
    times1 = []
    times2 = []
    for width in [10, 20, 25, 50]:
        height = 300//width
        print("Plotting cleaning time for a room of width:", width, "by height:", height)
        aspect_ratios.append(float(width) / height)
        times1.append(runSimulation(2, 1.0, width, height, 0.8, 200, StandardRobot))
        times2.append(runSimulation(2, 1.0, width, height, 0.8, 200, RandomWalkRobot))
    pylab.plot(aspect_ratios, times1)
    pylab.plot(aspect_ratios, times2)
    pylab.title(title)
    pylab.legend(('StandardRobot', 'RandomWalkRobot'))
    pylab.xlabel(x_label)
    pylab.ylabel(y_label)
    pylab.show()
    

# === Problem 6
# NOTE: If you are running the simulation, you will have to close it 
# before the plot will show up.

#
# 1) Write a function call to showPlot1 that generates an appropriately-labeled
#     plot.
#
#showPlot1("Cleaning Time vs Number of Robots", "# Robots", "Time")

#
# 2) Write a function call to showPlot2 that generates an appropriately-labeled
#     plot.
#
#       (... your call here ...)
#
