# coding: utf-8

"""
This code is part of a series of notebooks regarding  "Introduction to robot path planning".

License is based on Creative Commons: Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) (pls. check: http://creativecommons.org/licenses/by-nc/4.0/)
"""

from IPPerfMonitor import IPPerfMonitor

import matplotlib.pyplot as plt

import math

from shapely.geometry import Point, Polygon, LineString
from shapely import plotting
from shapely.affinity import translate, rotate

import numpy as np

class CollisionChecker(object):

    def __init__(self, scene, limits=[[0.0, 22.0], [0.0, 22.0]], statistic=None, robotDescription=None, robotType=1, degPerStep=None):
        self.scene = scene
        self.limits = limits
        self.robotDescription = robotDescription    # Form of robot
        self.robotType = robotType                  # 1D / 2D / 3D / ...
        try:
            self.robotCenter = self.robotDescription["center"]
        except:
            self.robotCenter = [0,0]
        if self.robotType == 3:
            assert (degPerStep != None)
            assert (len(self.limits) == 3)
            self.degPerStep = degPerStep
            self.limits[2][1] = math.floor(self.limits[2][1]/degPerStep)
        

    def getDim(self):
        """ Return dimension of Environment (Shapely should currently always be 2)"""
        return len(self.limits)

    def getEnvironmentLimits(self):
        """ Return limits of Environment"""
        return list(self.limits)

    @IPPerfMonitor
    def pointInCollision(self, pos):
        """ Return whether a configuration is
        inCollision -> True
        Free -> False """

        if self.robotType == 1:
            assert (len(pos) == self.getDim())
            for key, value in self.scene.items():
                if value.intersects(Point(pos[0], pos[1])):
                    return True
            return False
        
        elif self.robotType == 2:
            assert (len(pos) == self.getDim())
            # Verschiebe die Roboterform an die gegebene Position
            try:
                robotCenter = self.robotDescription["center"]
            except:
                robotCenter = [0,0]
            robot_shape_at_pos = translate(self.robotDescription["shape"], xoff=pos[0]-robotCenter[0], yoff=pos[1]-robotCenter[1])
            for key, value in self.scene.items():
                if value.intersects(robot_shape_at_pos):
                    return True
            return False
        
        elif self.robotType == 3:
            assert (len(pos) == self.getDim())
            # Verschiebe die Roboterform an die gegebene Position
            try:
                robotCenter = self.robotDescription["center"]
            except:
                robotCenter = [0,0]
            # print(pos)
            robot_shape_at_pos = translate(self.robotDescription["shape"], xoff=pos[0]-robotCenter[0], yoff=pos[1]-robotCenter[1])
            robot_shape_at_pos_turned = rotate(robot_shape_at_pos, pos[2]*self.degPerStep, origin=(pos[0], pos[1]))
            for key, value in self.scene.items():
                if value.intersects(robot_shape_at_pos_turned):
                    # print("intersects")
                    return True
            # print("no intersects")
            return False
            

    @IPPerfMonitor
    def lineInCollision(self, startPos, endPos):
        """ Check whether a line from startPos to endPos is colliding"""
        assert (len(startPos) == self.getDim())
        assert (len(endPos) == self.getDim())
        
        p1 = np.array(startPos)
        p2 = np.array(endPos)
        p12 = p2-p1
        k = 40
        #print("testing")
        for i in range(k):
            testPoint = p1 + (i+1)/k*p12
            if self.pointInCollision(testPoint)==True:
                return True
        
        return False
                

#        for key, value in self.scene.items():
#            if value.intersects(LineString([(startPos[0], startPos[1]), (endPos[0], endPos[1])])):
 #               return True
#        return False

    def drawObstacles(self, ax):
        for key, value in self.scene.items():
            plotting.plot_polygon(value, add_points=False, color='red')

    def drawRobot(self, ax, pos=None):
        if self.robotDescription and pos:
            for i in pos:
                act_pos = pos[i]
                robot_shape_at_pos = translate(self.robotDescription["shape"], xoff=act_pos[0]-self.robotCenter[0], yoff=act_pos[1]-self.robotCenter[1])
                if self.robotType == 3:
                    robot_shape_at_pos = rotate(robot_shape_at_pos, act_pos[2]*self.degPerStep, origin=(act_pos[0], act_pos[1]))
                plotting.plot_polygon(robot_shape_at_pos, add_points=False, color='blue')

            
