from __future__ import annotations

from .ClassFields import *
from .PPSHitmap import PPSHitmap
from .SensorPad import SensorPad

def calcLossProb(deadtime, occupancy, bunchSpacing=25.):
    from math import exp, floor
    timeStep = floor(deadtime/float(bunchSpacing))
    return 1 - (occupancy ** 2)/((1 - exp(-occupancy))**2) * exp(-2*occupancy * (timeStep + 1))

class Sensor:
    numPads = NonNegativeIntField()
    shifts = FloatPairListField()
    minX = FloatField()
    maxX = FloatField()
    minY = FloatField()
    maxY = FloatField()
    padVec : list[SensorPad]

    def __init__(self, shifts:list = []):
        self.shifts = shifts
        self.numPads = 0
        self.padVec = []

        self.minX = 0
        self.maxX = 0
        self.minY = 0
        self.maxY = 0

        self.hasFlux = False

    def setShifts(self, shifts:list):
        self.shifts = shifts
        for pad in self.padVec:
            pad.setEpochs(len(shifts))

        self.hasFlux = False

    def calculateFlux(self, hitmap:PPSHitmap):
        if not isinstance(hitmap, PPSHitmap):
            raise ValueError(f'expecting PPSHitmap to calculate the dose')

        hitmap._checkMap()

        for pad in self.padVec:
            pad.calculateFlux(self.shifts, hitmap) # Remember PPSHitmap is in m, sensor is in mm

        self.hasFlux = True

    def findMaxOccupancy(self, usePadSpacing=True):
        if not self.hasFlux:
            raise RuntimeError("You must calculate the fluxes before retrieving the max occupancy")

        occupancy = []
        for epoch in range(len(self.shifts)):
            padIdx = None

            for idx in range(len(self.padVec)):
                if padIdx is None:
                    padIdx = idx
                else:
                    if usePadSpacing:
                        if self.padVec[idx].doses[epoch]["occupancy"] > self.padVec[padIdx].doses[epoch]["occupancy"]:
                            padIdx = idx
                    else:
                        if self.padVec[idx].doses_extra[epoch]["occupancy"] > self.padVec[padIdx].doses_extra[epoch]["occupancy"]:
                            padIdx = idx

            if padIdx is None:
                raise RuntimeError("Unable to find pad with max occupancy for epoch {}".format(epoch))

            if usePadSpacing:
                occupancy += [self.padVec[padIdx].doses[epoch]["occupancy"]]
            else:
                occupancy += [self.padVec[padIdx].doses_extra[epoch]["occupancy"]]

        return occupancy

    def plotOccupancy(self, usePadSpacing=True):
        if not self.hasFlux:
            raise RuntimeError("You must calculate the fluxes before retrieving the max occupancy")
        #occupancy = self.findMaxOccupancy(usePadSpacing=usePadSpacing)
        numTPads = len(self.shifts)

        from math import ceil

        if numTPads <= 3:
            padX = numTPads
            padY = 1
        elif numTPads <= 6:
            padX = ceil(numTPads/2.)
            padY = 2
        else:
            padX = 3
            padY = ceil(numTPads/3.)

        from ROOT import TCanvas, TH2D  # type: ignore
        from array import array

        edgesX = []
        edgesY = []
        for pad in self.padVec:
            if pad.minX_extra not in edgesX:
                edgesX += [pad.minX_extra]
            if pad.maxX_extra not in edgesX:
                edgesX += [pad.maxX_extra]
            if pad.minY_extra not in edgesY:
                edgesY += [pad.minY_extra]
            if pad.maxY_extra not in edgesY:
                edgesY += [pad.maxY_extra]
        edgesX.sort()
        edgesY.sort()

        xArr, yArr = array( 'd' ), array( 'd' )
        for edge in edgesX:
            xArr.append(edge)
        for edge in edgesY:
            yArr.append(edge)

        persistance = {}
        canv = TCanvas("epoch_Occupancy", "Epoch Occupancy", padX * 400, padY * 400)
        canv.Divide(padX, padY)

        histTemplate = TH2D("template", "Sensor Occupancy", len(xArr)-1, xArr, len(yArr)-1, yArr)
        histTemplate.SetStats(False)
        histTemplate.GetXaxis().SetTitle("x [mm]")
        histTemplate.GetYaxis().SetTitle("y [mm]")
        histTemplate.GetZaxis().SetTitle("#mu")

        numBinsX = len(xArr)-1
        numBinsY = len(yArr)-1

        for epoch in range(len(self.shifts)):
            pad = canv.cd(epoch+1)
            #pad.SetLogz()
            pad.SetTicks()
            #pad.SetLeftMargin(0.11)
            pad.SetRightMargin(0.16)
            pad.SetTopMargin(0.07)
            #pad.SetBottomMargin(0.14)

            hist = histTemplate.Clone("occupancy-epoch{}".format(epoch))
            hist.SetTitle("Occupancy Position {}".format(self.shifts[epoch]))

            for binX in range(numBinsX):
                binXPos = (edgesX[binX] + edgesX[binX+1])/2
                for binY in range(numBinsY):
                    binYPos = (edgesY[binY] + edgesY[binY+1])/2

                    occupancy = 0
                    for pad in self.padVec:
                        padMinX = pad.minX_extra
                        padMaxX = pad.maxX_extra
                        padMinY = pad.minY_extra
                        padMaxY = pad.maxY_extra
                        if ((binXPos > padMinX and binXPos < padMaxX) and
                            (binYPos > padMinY and binYPos < padMaxY)):
                            if usePadSpacing:
                                occupancy = pad.doses[epoch]["occupancy"]
                            else:
                                occupancy = pad.doses_extra[epoch]["occupancy"]
                            break

                    binx = hist.GetXaxis().FindBin(binXPos)
                    biny = hist.GetYaxis().FindBin(binYPos)
                    hist.SetBinContent(binx, biny, occupancy)

            hist.Draw("colz")

            persistance["occupancy-{}".format(epoch)] = hist

        return (canv, persistance)

    def plotLossProbabilityVsDeadtime(self, timeSteps=1000, minTime=0, maxTime=10000, usePadSpacing=True): # Time in ns
        occupancy = self.findMaxOccupancy(usePadSpacing=usePadSpacing)
        numTPads = len(occupancy)

        from math import ceil

        if numTPads <= 3:
            padX = numTPads
            padY = 1
        elif numTPads <= 6:
            padX = ceil(numTPads/2.)
            padY = 2
        else:
            padX = 3
            padY = ceil(numTPads/3.)

        from ROOT import TCanvas, TH2D, TGraph  # type: ignore
        from array import array

        persistance = {}
        canv = TCanvas("epoch_loss_probability", "Epoch Loss Probability", padX * 400, padY * 400)
        canv.Divide(padX, padY)

        # Create an empty histogram to serve as the frame for the graphs
        frame = TH2D("frame", "", 100, minTime, maxTime, 100, 0.001, 1.1)
        frame.SetStats(False)
        frame.GetXaxis().SetTitle("#tau ns")
        frame.GetYaxis().SetTitle("Event Loss Probability")

        for epoch in range(len(self.shifts)):
            pad = canv.cd(epoch+1)
            if minTime != 0:
                pad.SetLogx()
            pad.SetLogy()
            pad.SetTicks()

            persistance[self.shifts[epoch]] = {}

            persistance[self.shifts[epoch]]["frame"] = frame.Clone("frame-{}".format(epoch))
            persistance[self.shifts[epoch]]["frame"].SetTitle("Position {}".format(self.shifts[epoch]))
            persistance[self.shifts[epoch]]["frame"].Draw()

            timeArr, lossProb = array( 'd' ), array( 'd' )
            for i in range(timeSteps):
                time = minTime + i * float(maxTime - minTime)/timeSteps
                timeArr.append(time)
                lossProb.append(calcLossProb(time, occupancy[epoch]))
            persistance[self.shifts[epoch]]["graph"] = TGraph(timeSteps, timeArr, lossProb)
            persistance[self.shifts[epoch]]["graph"].Draw("l same")

        return (canv, persistance)

    def preview(self, margin=0.8, fontscale=1.0, doSquare=False):
        if self.numPads == 0:
            return None

        import matplotlib.pyplot as plt
        import matplotlib.patches as patches

        fig = plt.figure(figsize=(9, 9))
        ax1 = plt.subplot2grid((1,1),(0,0))

        if doSquare:
            minV = min(self.minX-margin, self.minY-margin)
            maxV = max(self.maxX+margin, self.maxY+margin)
            plt.xlim([minV, maxV])
            plt.ylim([minV, maxV])
        else:
            plt.xlim([self.minX-margin, self.maxX+margin])
            plt.ylim([self.minY-margin, self.maxY+margin])

        rect = patches.Rectangle((self.minX, self.minY),
                                    self.maxX-self.minX,
                                    self.maxY-self.minY,
                                    linewidth=1,
                                    edgecolor='r',
                                    facecolor='none')
        ax1.add_patch(rect)

        pad_idx = 0
        for pad in self.padVec:
            rect = patches.Rectangle((pad.minX, pad.minY),
                                        pad.maxX-pad.minX,
                                        pad.maxY-pad.minY,
                                        linewidth = 1,
                                        edgecolor='b',
                                        facecolor='none'
                                    )
            ax1.add_patch(rect)
            ax1.text((pad.minX + pad.maxX)/2,
                        (pad.minY + pad.maxY)/2,
                        f'{pad_idx}',
                        ha='center',
                        va='center',
                        fontsize=10*fontscale
                    )
            pad_idx += 1

        return fig

    def maxDoseEOL(self, integratedLuminosity=300, usePadSpacing = True):
        maxDose = None

        for pad in self.padVec:
            padDose = pad.maxDoseEOL(integratedLuminosity=integratedLuminosity, usePadSpacing=usePadSpacing)
            if maxDose is None:
                maxDose = padDose
            else:
                if padDose > maxDose:
                    maxDose = padDose

        return maxDose