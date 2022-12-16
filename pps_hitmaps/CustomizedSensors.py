from __future__ import annotations

from .Sensor import Sensor
from .SensorPad import SensorPad


class SimpleETLSensor(Sensor):
    def __init__(self, shifts:list = []):
        Sensor.__init__(self, shifts=shifts)

        PadSize = 1.3
        SensorSize = PadSize*16

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        for x in range(16):
            minX = -SensorSize/2 + x*PadSize
            maxX = -SensorSize/2 + (x+1)*PadSize
            for y in range(16):
                minY = -SensorSize/2 + y*PadSize
                maxY = -SensorSize/2 + (y+1)*PadSize
                self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=0)]

        self.numPads = len(self.padVec)

class RealisticETLSensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(16):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            for y in range(16):
                minY = SensitiveEdge + y*PadSize + PadSpacing/2
                maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid1Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(15):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 14:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(32):
                    minY = SensitiveEdge + y*PadSize/2 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/2 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid2Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(14):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 13:
                maxX = SensitiveEdge + (x+3)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(48):
                    minY = SensitiveEdge + y*PadSize/3 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/3 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid3Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(13):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 12:
                maxX = SensitiveEdge + (x+4)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(64):
                    minY = SensitiveEdge + y*PadSize/4 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/4 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid4Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(13):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 11:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 12:
                minX = SensitiveEdge + (x+1)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+4)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(64):
                    minY = SensitiveEdge + y*PadSize/4 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/4 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid5Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(13):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 12:
                maxX = SensitiveEdge + (x+4)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(32):
                    minY = SensitiveEdge + y*PadSize/2 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/2 - PadSpacing/2
                    for xi in range(2):
                        minX = SensitiveEdge + xi*PadSize/2 + PadSpacing/2
                        maxX = SensitiveEdge + (xi+1)*PadSize/2 - PadSpacing/2
                        self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid6Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(13):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 11:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 12:
                minX = SensitiveEdge + (x+1)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+4)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(32):
                    minY = SensitiveEdge + y*PadSize/2 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/2 - PadSpacing/2
                    for xi in range(2):
                        minX = SensitiveEdge + xi*PadSize/2 + PadSpacing/2
                        maxX = SensitiveEdge + (xi+1)*PadSize/2 - PadSpacing/2
                        self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid7Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(13):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 10:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 11:
                minX = SensitiveEdge + (x+1)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+3)*PadSize - PadSpacing/2
            if x == 12:
                minX = SensitiveEdge + (x+2)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+4)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(64):
                    minY = SensitiveEdge + y*PadSize/4 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/4 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid8Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(13):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 10:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 11:
                minX = SensitiveEdge + (x+1)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+3)*PadSize - PadSpacing/2
            if x == 12:
                minX = SensitiveEdge + (x+2)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+4)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(32):
                    minY = SensitiveEdge + y*PadSize/2 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/2 - PadSpacing/2
                    for xi in range(2):
                        minX = SensitiveEdge + xi*PadSize/2 + PadSpacing/2
                        maxX = SensitiveEdge + (xi+1)*PadSize/2 - PadSpacing/2
                        self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid9Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(14):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 12:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 13:
                minX = SensitiveEdge + (x+1)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+3)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(48):
                    minY = SensitiveEdge + y*PadSize/3 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/3 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(16):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid10Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(14):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 13:
                maxX = SensitiveEdge + (x+3)*PadSize - PadSpacing/2
            if x == 0:
                minX = SensitiveEdge + PadSpacing/2
                maxX = SensitiveEdge + (x+1)*PadSize/2 - PadSpacing/2
                for y in range(32):
                    minY = SensitiveEdge + y*PadSize/2 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/2 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
                minX = SensitiveEdge + PadSize/2 + PadSpacing/2
                maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            for y in range(16):
                minY = SensitiveEdge + y*PadSize + PadSpacing/2
                maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class PPSHybrid11Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.1, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*16 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*8

        for x in range(14):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 12:
                maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
            if x == 13:
                minX = SensitiveEdge + (x+1)*PadSize + PadSpacing/2
                maxX = SensitiveEdge + (x+3)*PadSize - PadSpacing/2
            if x == 0:
                minX = SensitiveEdge + PadSpacing/2
                maxX = SensitiveEdge + (x+1)*PadSize/2 - PadSpacing/2
                for y in range(32):
                    minY = SensitiveEdge + y*PadSize/2 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/2 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
                minX = SensitiveEdge + PadSize/2 + PadSpacing/2
                maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            for y in range(16):
                minY = SensitiveEdge + y*PadSize + PadSpacing/2
                maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class TIProduction1Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.03, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*3 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*1.5

        for x in range(3):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(12):
                    minY = SensitiveEdge + y*PadSize/4 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/4 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(3):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class TIProduction2Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.03, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSizeX = PadSize*2 + 2*GuardRing - PadSpacing
        SensorSizeY = PadSize*1 + 2*GuardRing - PadSpacing

        self.minX =-SensorSizeX/2
        self.maxX = SensorSizeX/2
        self.minY =-SensorSizeY/2
        self.maxY = SensorSizeY/2

        SensitiveEdgeX = -PadSize
        SensitiveEdgeY = -PadSize*0.5

        for x in range(2):
            minX = SensitiveEdgeX + x*PadSize + PadSpacing/2
            maxX = SensitiveEdgeX + (x+1)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(4):
                    minY = SensitiveEdgeY + y*PadSize/4 + PadSpacing/2
                    maxY = SensitiveEdgeY + (y+1)*PadSize/4 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                for y in range(1):
                    minY = SensitiveEdgeY + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdgeY + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)

class TIProduction3Sensor(Sensor):
    def __init__(self, shifts:list = [], PadSize = 1.3, PadSpacing = 0.03, GuardRing = 0.3):
        """
        PadSize - design size of the square pads, neglecting the interpad distance
        PadSpacing - the interpad distance
        GuardRing - the size of the guard ring
        """
        Sensor.__init__(self, shifts=shifts)

        self.padSize = PadSize
        self.padSpacing = PadSpacing
        self.guardRing = GuardRing

        SensorSize = PadSize*5 + 2*GuardRing - PadSpacing

        self.minX =-SensorSize/2
        self.maxX = SensorSize/2
        self.minY =-SensorSize/2
        self.maxY = SensorSize/2

        SensitiveEdge = -PadSize*2.5

        for x in range(4):
            minX = SensitiveEdge + x*PadSize + PadSpacing/2
            maxX = SensitiveEdge + (x+1)*PadSize - PadSpacing/2
            if x == 0:
                for y in range(20):
                    minY = SensitiveEdge + y*PadSize/4 + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize/4 - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]
            else:
                if x == 3:
                    maxX = SensitiveEdge + (x+2)*PadSize - PadSpacing/2
                for y in range(5):
                    minY = SensitiveEdge + y*PadSize + PadSpacing/2
                    maxY = SensitiveEdge + (y+1)*PadSize - PadSpacing/2
                    self.padVec += [SensorPad(epochs = len(shifts), minX=minX, maxX=maxX, minY=minY, maxY=maxY, extra=PadSpacing/2)]

        self.numPads = len(self.padVec)
