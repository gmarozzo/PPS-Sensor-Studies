from __future__ import annotations

from .ClassFields import *

def cleanEdges(edgeList, threshold=0.000001):
    newEdges = []

    for edge in edgeList:
        if len(newEdges) == 0:
            newEdges = [edge]
        else:
            if abs(edge - newEdges[-1]) > threshold:
                newEdges += [edge]

    return newEdges

def summariseEdges(edgeListVector, threshold=0.000001):
    allEdges = []

    for edgelist in edgeListVector:
        allEdges += edgelist

    allEdges.sort()

    return cleanEdges(allEdges, threshold=threshold)

# Pad dimensions in mm
# Assume a default pad size of 1.3 mm
defaultPadSize = 1.3
class SensorPad:
    epochs = NonNegativeIntField()

    minX = FloatField()
    maxX = FloatField()
    minY = FloatField()
    maxY = FloatField()
    #doses = FloatListField()

    minX_extra = FloatField()
    maxX_extra = FloatField()
    minY_extra = FloatField()
    maxY_extra = FloatField()
    #doses_extra = FloatListField()

    def __init__(self,
                    epochs:int=1,
                    minX:float=-defaultPadSize/2,
                    maxX:float= defaultPadSize/2,
                    minY:float=-defaultPadSize/2,
                    maxY:float= defaultPadSize/2,
                    extra:float=0 # Extra space is for considering the interpad distance when accounting doses
                ):
        self.epochs = epochs

        self.minX = minX
        self.maxX = maxX
        self.minY = minY
        self.maxY = maxY

        self.minX_extra = minX - extra
        self.maxX_extra = maxX + extra
        self.minY_extra = minY - extra
        self.maxY_extra = maxY + extra

        self.doses = []
        self.doses_extra = []

    def setEpochs(self, epochs:int):
        self.epochs = epochs

    def calculateFlux(self, shifts, hitmap): # Remember PPSHitmap is in m, sensor is in mm
        if len(shifts) != self.epochs:
            raise ValueError(f'Expected the number of shift positions to match the number of epochs')

        self.doses = []
        self.doses_extra = []

        for epoch in range(self.epochs):
            minX = self.minX + shifts[epoch][0]
            maxX = self.maxX + shifts[epoch][0]
            minY = self.minY + shifts[epoch][1]
            maxY = self.maxY + shifts[epoch][1]

            centerPadX = (minX + maxX)/2
            centerPadY = (minY + maxY)/2

            minX_extra = self.minX_extra + shifts[epoch][0]
            maxX_extra = self.maxX_extra + shifts[epoch][0]
            minY_extra = self.minY_extra + shifts[epoch][1]
            maxY_extra = self.maxY_extra + shifts[epoch][1]

            centerPadX_extra = (minX_extra + maxX_extra)/2
            centerPadY_extra = (minY_extra + maxY_extra)/2

            flux = 0
            flux_extra = 0
            maxFlux = None
            maxFlux_extra = None
            fluxMap = []
            fluxMap_extra = []

            for x in hitmap.map:
                xVal = x*1000
                left = xVal - hitmap.xStep*1000/2
                right = xVal + hitmap.xStep*1000/2

                inSensitiveArea = True
                inSensitiveArea_extra = True

                if ((left < minX and right < minX) or
                    (left > maxX and right > maxX)):
                    inSensitiveArea = False

                if ((left < minX_extra and right < minX_extra) or
                    (left > maxX_extra and right > maxX_extra)):
                    inSensitiveArea_extra = False

                contributionX = 0
                if inSensitiveArea:
                    contributionX = 1
                    if right > maxX:
                        contributionX -= (right - maxX)/(hitmap.xStep*1000)
                    if left < minX:
                        contributionX -= (minX - left)/(hitmap.xStep*1000)

                contributionX_extra = 0
                if inSensitiveArea_extra:
                    contributionX_extra = 1
                    if right > maxX_extra:
                        contributionX_extra -= (right - maxX_extra)/(hitmap.xStep*1000)
                    if left < minX_extra:
                        contributionX_extra -= (minX_extra - left)/(hitmap.xStep*1000)

                if not (inSensitiveArea or inSensitiveArea_extra):
                    continue

                for y in hitmap.map[x]:
                    yVal = y*1000
                    bottom = yVal - hitmap.yStep*1000/2
                    top = yVal + hitmap.yStep*1000/2

                    inSensitiveAreaY = True
                    inSensitiveAreaY_extra = True

                    if ((bottom < minY and top < minY) or
                        (bottom > maxY and top > maxY)):
                        inSensitiveAreaY = False

                    if ((bottom < minY_extra and top < minY_extra) or
                        (bottom > maxY_extra and top > maxY_extra)):
                        inSensitiveAreaY_extra = False

                    if inSensitiveArea and inSensitiveAreaY:
                        contributionY = 1
                        if top > maxY:
                            contributionY -= (top - maxY)/(hitmap.yStep*1000)
                        if bottom < minY:
                            contributionY -= (minY - bottom)/(hitmap.yStep*1000)

                        flux += hitmap.map[x][y] * contributionX * contributionY

                        if maxFlux is None or hitmap.map[x][y] > maxFlux:
                            maxFlux = hitmap.map[x][y]

                        fluxMap += [{
                            'flux': hitmap.map[x][y],
                            'x': xVal,
                            'y': yVal,
                            'xLocal': xVal - centerPadX,
                            'yLocal': yVal - centerPadY,
                            'leftLocal': left - centerPadX,
                            'rightLocal': right - centerPadX,
                            'topLocal': top - centerPadY,
                            'bottomLocal': bottom - centerPadY,
                        }]

                    if inSensitiveArea_extra and inSensitiveAreaY_extra:
                        contributionY_extra = 1
                        if top > maxY_extra:
                            contributionY_extra -= (top - maxY_extra)/(hitmap.yStep*1000)
                        if bottom < minY_extra:
                            contributionY_extra -= (minY_extra - bottom)/(hitmap.yStep*1000)

                        flux_extra += hitmap.map[x][y] * contributionX_extra * contributionY_extra

                        if maxFlux_extra is None or hitmap.map[x][y] > maxFlux_extra:
                            maxFlux_extra = hitmap.map[x][y]

                        fluxMap_extra += [{
                            'flux': hitmap.map[x][y],
                            'x': xVal,
                            'y': yVal,
                            'xLocal': xVal - centerPadX_extra,
                            'yLocal': yVal - centerPadY_extra,
                            'leftLocal': left - centerPadX_extra,
                            'rightLocal': right - centerPadX_extra,
                            'topLocal': top - centerPadY_extra,
                            'bottomLocal': bottom - centerPadY_extra,
                        }]

            occupancyNorm = (hitmap.xStep *
                             hitmap.yStep * 1.0E4) # in cm^2

            self.doses += [{
                'totalFlux': flux,
                'maxFlux': maxFlux,
                'occupancyNorm': occupancyNorm,
                'occupancy': flux * 1.6E-12 * occupancyNorm,
                'fluxMap': fluxMap,
                }]
            self.doses_extra += [{
                'totalFlux': flux_extra,
                'maxFlux': maxFlux_extra,
                'occupancyNorm': occupancyNorm,
                'occupancy': flux_extra * 1.6E-12 * occupancyNorm,
                'fluxMap': fluxMap_extra,
                }]
            
    def calculatepartialFlux(self, shifts, integratedLuminosity, hitmap): # Remember PPSHitmap is in m, sensor is in mm
        #if len(shifts) != self.epochs:
        #    raise ValueError(f'Expected the number of shift positions to match the number of epochs')
            
        relevantShifts = float(len(shifts))*float(integratedLuminosity)/300.0 
        intpart,floatpart = divmod(relevantShifts,1)
        isfractionary = floatpart>0.0001
        cutshifts = []
        if isfractionary:
            cutshifts = shifts[:int(intpart)+1]
        else:
            cutshifts = shifts[:int(intpart)]
            floatpart = 1

        self.doses = []
        self.doses_extra = []

        for epoch in range(len(cutshifts)):
            minX = self.minX + shifts[epoch][0]
            maxX = self.maxX + shifts[epoch][0]
            minY = self.minY + shifts[epoch][1]
            maxY = self.maxY + shifts[epoch][1]

            centerPadX = (minX + maxX)/2
            centerPadY = (minY + maxY)/2

            minX_extra = self.minX_extra + shifts[epoch][0]
            maxX_extra = self.maxX_extra + shifts[epoch][0]
            minY_extra = self.minY_extra + shifts[epoch][1]
            maxY_extra = self.maxY_extra + shifts[epoch][1]

            centerPadX_extra = (minX_extra + maxX_extra)/2
            centerPadY_extra = (minY_extra + maxY_extra)/2

            flux = 0
            flux_extra = 0
            maxFlux = None
            maxFlux_extra = None
            fluxMap = []
            fluxMap_extra = []

            for x in hitmap.map:
                xVal = x*1000
                left = xVal - hitmap.xStep*1000/2
                right = xVal + hitmap.xStep*1000/2

                inSensitiveArea = True
                inSensitiveArea_extra = True

                if ((left < minX and right < minX) or
                    (left > maxX and right > maxX)):
                    inSensitiveArea = False

                if ((left < minX_extra and right < minX_extra) or
                    (left > maxX_extra and right > maxX_extra)):
                    inSensitiveArea_extra = False

                contributionX = 0
                if inSensitiveArea:
                    contributionX = 1
                    if right > maxX:
                        contributionX -= (right - maxX)/(hitmap.xStep*1000)
                    if left < minX:
                        contributionX -= (minX - left)/(hitmap.xStep*1000)

                contributionX_extra = 0
                if inSensitiveArea_extra:
                    contributionX_extra = 1
                    if right > maxX_extra:
                        contributionX_extra -= (right - maxX_extra)/(hitmap.xStep*1000)
                    if left < minX_extra:
                        contributionX_extra -= (minX_extra - left)/(hitmap.xStep*1000)

                if not (inSensitiveArea or inSensitiveArea_extra):
                    continue

                for y in hitmap.map[x]:
                    yVal = y*1000
                    bottom = yVal - hitmap.yStep*1000/2
                    top = yVal + hitmap.yStep*1000/2

                    inSensitiveAreaY = True
                    inSensitiveAreaY_extra = True

                    if ((bottom < minY and top < minY) or
                        (bottom > maxY and top > maxY)):
                        inSensitiveAreaY = False

                    if ((bottom < minY_extra and top < minY_extra) or
                        (bottom > maxY_extra and top > maxY_extra)):
                        inSensitiveAreaY_extra = False

                    if inSensitiveArea and inSensitiveAreaY:
                        contributionY = 1
                        if top > maxY:
                            contributionY -= (top - maxY)/(hitmap.yStep*1000)
                        if bottom < minY:
                            contributionY -= (minY - bottom)/(hitmap.yStep*1000)

                        if epoch==len(cutshifts)-1:
                            flux += hitmap.map[x][y] * contributionX * contributionY * floatpart
                        else:
                            flux += hitmap.map[x][y] * contributionX * contributionY

                        if maxFlux is None or hitmap.map[x][y] > maxFlux:
                            maxFlux = hitmap.map[x][y]
                            
                        if epoch==len(cutshifts)-1:
                            fluxMap += [{
                                'flux': hitmap.map[x][y]*floatpart,
                                'x': xVal,
                                'y': yVal,
                                'xLocal': xVal - centerPadX,
                                'yLocal': yVal - centerPadY,
                                'leftLocal': left - centerPadX,
                                'rightLocal': right - centerPadX,
                                'topLocal': top - centerPadY,
                                'bottomLocal': bottom - centerPadY,
                            }]
                        else:
                            fluxMap += [{
                                'flux': hitmap.map[x][y],
                                'x': xVal,
                                'y': yVal,
                                'xLocal': xVal - centerPadX,
                                'yLocal': yVal - centerPadY,
                                'leftLocal': left - centerPadX,
                                'rightLocal': right - centerPadX,
                                'topLocal': top - centerPadY,
                                'bottomLocal': bottom - centerPadY,
                            }]
                            

                    if inSensitiveArea_extra and inSensitiveAreaY_extra:
                        contributionY_extra = 1
                        if top > maxY_extra:
                            contributionY_extra -= (top - maxY_extra)/(hitmap.yStep*1000)
                        if bottom < minY_extra:
                            contributionY_extra -= (minY_extra - bottom)/(hitmap.yStep*1000)

                        flux_extra += hitmap.map[x][y] * contributionX_extra * contributionY_extra

                        if maxFlux_extra is None or hitmap.map[x][y] > maxFlux_extra:
                            maxFlux_extra = hitmap.map[x][y]

                        fluxMap_extra += [{
                            'flux': hitmap.map[x][y],
                            'x': xVal,
                            'y': yVal,
                            'xLocal': xVal - centerPadX_extra,
                            'yLocal': yVal - centerPadY_extra,
                            'leftLocal': left - centerPadX_extra,
                            'rightLocal': right - centerPadX_extra,
                            'topLocal': top - centerPadY_extra,
                            'bottomLocal': bottom - centerPadY_extra,
                        }]

            occupancyNorm = (hitmap.xStep *
                             hitmap.yStep * 1.0E4) # in cm^2

            self.doses += [{
                'totalFlux': flux,
                'maxFlux': maxFlux,
                'occupancyNorm': occupancyNorm,
                'occupancy': flux * 1.6E-12 * occupancyNorm,
                'fluxMap': fluxMap,
                }]
            self.doses_extra += [{
                'totalFlux': flux_extra,
                'maxFlux': maxFlux_extra,
                'occupancyNorm': occupancyNorm,
                'occupancy': flux_extra * 1.6E-12 * occupancyNorm,
                'fluxMap': fluxMap_extra,
                }]

    def plotFlux(self, usePadSpacing = True, printEpoch = None):
        from math import ceil

        doses = self.doses
        if not usePadSpacing:
            doses = self.doses_extra

        numTPads = len(doses)
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
        from ROOT import TLine  # type: ignore
        from ROOT import kRed, kBlue  # type: ignore
        from array import array

        persistance = {}
        canv = TCanvas("flux", "Flux", padX * 400, padY * 400)
        canv.Divide(padX, padY)

        minX = self.minX
        maxX = self.maxX
        minY = self.minY
        maxY = self.maxY
        if not usePadSpacing:
            minX = self.minX_extra
            maxX = self.maxX_extra
            minY = self.minY_extra
            maxY = self.maxY_extra

        medX = (minX + maxX)/2
        medY = (minY + maxY)/2

        minX -= medX
        maxX -= medX
        minY -= medY
        maxY -= medY

        persistance["leftEdge"]   = TLine(minX, minY, minX, maxY)
        persistance["rightEdge"]  = TLine(maxX, minY, maxX, maxY)
        persistance["topEdge"]    = TLine(minX, minY, maxX, minY)
        persistance["bottomEdge"] = TLine(minX, maxY, maxX, maxY)

        persistance["leftEdge"].SetLineColor(kRed)
        persistance["rightEdge"].SetLineColor(kRed)
        persistance["topEdge"].SetLineColor(kRed)
        persistance["bottomEdge"].SetLineColor(kRed)

        if not usePadSpacing:
            padMinX = self.minX
            padMaxX = self.maxX
            padMinY = self.minY
            padMaxY = self.maxY

            padMedX = (padMinX + padMaxX)/2
            padMedY = (padMinY + padMaxY)/2

            padMinX -= padMedX
            padMaxX -= padMedX
            padMinY -= padMedY
            padMaxY -= padMedY

            persistance["pad_leftEdge"]   = TLine(padMinX, padMinY, padMinX, padMaxY)
            persistance["pad_rightEdge"]  = TLine(padMaxX, padMinY, padMaxX, padMaxY)
            persistance["pad_topEdge"]    = TLine(padMinX, padMinY, padMaxX, padMinY)
            persistance["pad_bottomEdge"] = TLine(padMinX, padMaxY, padMaxX, padMaxY)

            persistance["pad_leftEdge"].SetLineColor(kBlue)
            persistance["pad_rightEdge"].SetLineColor(kBlue)
            persistance["pad_topEdge"].SetLineColor(kBlue)
            persistance["pad_bottomEdge"].SetLineColor(kBlue)

        idx = 0
        for epoch in doses:
            idx += 1
            pad = canv.cd(idx)
            pad.SetLogz()
            pad.SetTicks()
            pad.SetLeftMargin(0.11)
            pad.SetRightMargin(0.17)
            pad.SetTopMargin(0.07)
            pad.SetBottomMargin(0.09)#0.14

            if printEpoch is not None and idx == printEpoch:
                print("Printing the epoch {}".format(idx))
                print("There are {} flux points".format(len(epoch['fluxMap'])))

            xEdges = []
            yEdges = []
            for point in epoch['fluxMap']:
                if point['leftLocal'] not in xEdges:
                    xEdges += [point['leftLocal']]
                if point['rightLocal'] not in xEdges:
                    xEdges += [point['rightLocal']]
                if point['topLocal'] not in yEdges:
                    yEdges += [point['topLocal']]
                if point['bottomLocal'] not in yEdges:
                    yEdges += [point['bottomLocal']]
            xEdges.sort()
            yEdges.sort()

            xEdges = cleanEdges(xEdges)
            yEdges = cleanEdges(yEdges)

            if printEpoch is not None and idx == printEpoch:
                print("There are {} x edges, they are:".format(len(xEdges)))
                for edge in xEdges:
                    print("  - {}".format(edge))
                print("")
                print("There are {} y edges, they are:".format(len(yEdges)))
                for edge in yEdges:
                    print("  - {}".format(edge))

            xArr, yArr = array( 'd' ), array( 'd' )
            for edge in xEdges:
                xArr.append(edge)
            for edge in yEdges:
                yArr.append(edge)

            hist = TH2D("pad_flux_{}".format(idx), "Pad Flux - Position {}".format(idx), len(xArr)-1, xArr, len(yArr)-1, yArr)
            for point in epoch['fluxMap']:
                binx = hist.GetXaxis().FindBin(point['xLocal'])
                biny = hist.GetYaxis().FindBin(point['yLocal'])
                hist.SetBinContent(binx, biny, point['flux'])
                if printEpoch is not None and idx == printEpoch:
                    print("Flux point:")
                    print("  - local coords: ({},{})".format(point['xLocal'], point['yLocal']))
                    print("  - bin idx: ({}, {})".format(binx, biny))
                    print("  - flux: {}".format(point['flux']))
                #bin = hist.FindBin(point['xLocal'], point['yLocal'])
                #hist.SetBinContent(bin, point['flux'])

            hist.SetStats(False)
            hist.GetXaxis().SetTitle( "x [mm]" )
            hist.GetYaxis().SetTitle( "y [mm]" )
            hist.GetZaxis().SetTitle( "#Phi [p / (cm^{2} fb^{-1})]" )
            hist.GetZaxis().SetTitleOffset(1.8)

            hist.Draw('colz')
            persistance[idx] = {}
            persistance[idx]['hist'] = hist

            persistance["leftEdge"].Draw("same")
            persistance["rightEdge"].Draw("same")
            persistance["topEdge"].Draw("same")
            persistance["bottomEdge"].Draw("same")

            if not usePadSpacing:
                persistance["pad_leftEdge"].Draw("same")
                persistance["pad_rightEdge"].Draw("same")
                persistance["pad_topEdge"].Draw("same")
                persistance["pad_bottomEdge"].Draw("same")

        return (canv, persistance)

    def plotDose(self, maxTime=365, integratedLuminosity=300, usePadSpacing = True):
        """
        maxTime in days
        integratedLuminosity in fb-1
        """
        doses = self.doses
        padArea = (self.maxX - self.minX) * (self.maxY - self.minY)
        if not usePadSpacing:
            doses = self.doses_extra
            padArea = (self.maxX_extra - self.minX_extra) * (self.maxY_extra - self.minY_extra)

        # self.epochs for the number of epochs

        from ROOT import TCanvas, TH1D  # type: ignore
        from ROOT import TLine  # type: ignore
        from ROOT import kRed, kBlue  # type: ignore

        epochLumi = float(integratedLuminosity)/self.epochs
        epochTime = float(maxTime)/self.epochs
        maxDose = 0
        for epoch in range(self.epochs):
            maxDose += (doses[epoch]["totalFlux"] * doses[epoch]["occupancyNorm"] * epochLumi)/(padArea/100) # convert mm^2 to cm^2

        persistance = {}
        canv = TCanvas("dose_vs_time", "Dose over time", 600 * self.epochs, 800)

        persistance["hist"] = TH1D("dose_vs_time_hist", "Dose over time - {}={}{};t [day];#Phi [p / {}]".format("L_{int}", integratedLuminosity, " fb^{-1}", "cm^{2}"), self.epochs, 0, maxTime)
        persistance["hist"].SetStats(False)
        persistance["hist"].GetYaxis().SetRangeUser(0, maxDose*1.1)
        persistance["hist"].Draw()

        for epoch in range(self.epochs-1):
            lineName = "epoch-{}".format(epoch)
            x = (epoch + 1) * epochTime
            persistance[lineName] = TLine(x, 0, x, maxDose*1.1)
            persistance[lineName].SetLineColor(kRed)
            persistance[lineName].SetLineStyle(2)
            persistance[lineName].Draw("same")

        startDose = 0
        endDose = 0
        startT = 0
        endT = 0
        for epoch in range(self.epochs):
            endDose = startDose + (doses[epoch]["totalFlux"] * doses[epoch]["occupancyNorm"] * epochLumi)/(padArea/100)
            endT = startT + epochTime

            epochName = "dose-{}".format(epoch)
            persistance[epochName] = TLine(startT, startDose, endT, endDose)
            persistance[epochName].SetLineColor(kBlue)
            persistance[epochName].Draw("same")

            startDose = endDose
            startT = endT

        return (canv, persistance)

    def plotDoseEOL(self, integratedLuminosity=300, usePadSpacing = True):
        """
        maxTime in days
        integratedLuminosity in fb-1
        """
        doses = self.doses
        if not usePadSpacing:
            doses = self.doses_extra

        from ROOT import TCanvas, TH2D  # type: ignore
        from ROOT import TLine  # type: ignore
        from ROOT import kRed, kBlue  # type: ignore
        from array import array

        epochLumi = float(integratedLuminosity)/self.epochs
        #epochTime = float(maxTime)/self.epochs

        persistance = {}
        canv = TCanvas("dose_eol", "Dose EOL", 800, 800)

        canv.SetLogz()
        canv.SetTicks()
        canv.SetLeftMargin(0.11)
        canv.SetRightMargin(0.17)
        canv.SetTopMargin(0.07)
        canv.SetBottomMargin(0.09)#0.14

        minX = self.minX
        maxX = self.maxX
        minY = self.minY
        maxY = self.maxY
        if not usePadSpacing:
            minX = self.minX_extra
            maxX = self.maxX_extra
            minY = self.minY_extra
            maxY = self.maxY_extra

        medX = (minX + maxX)/2
        medY = (minY + maxY)/2

        minX -= medX
        maxX -= medX
        minY -= medY
        maxY -= medY

        persistance["leftEdge"]   = TLine(minX, minY, minX, maxY)
        persistance["rightEdge"]  = TLine(maxX, minY, maxX, maxY)
        persistance["topEdge"]    = TLine(minX, minY, maxX, minY)
        persistance["bottomEdge"] = TLine(minX, maxY, maxX, maxY)

        persistance["leftEdge"].SetLineColor(kRed)
        persistance["rightEdge"].SetLineColor(kRed)
        persistance["topEdge"].SetLineColor(kRed)
        persistance["bottomEdge"].SetLineColor(kRed)

        if not usePadSpacing:
            padMinX = self.minX
            padMaxX = self.maxX
            padMinY = self.minY
            padMaxY = self.maxY

            padMedX = (padMinX + padMaxX)/2
            padMedY = (padMinY + padMaxY)/2

            padMinX -= padMedX
            padMaxX -= padMedX
            padMinY -= padMedY
            padMaxY -= padMedY

            persistance["pad_leftEdge"]   = TLine(padMinX, padMinY, padMinX, padMaxY)
            persistance["pad_rightEdge"]  = TLine(padMaxX, padMinY, padMaxX, padMaxY)
            persistance["pad_topEdge"]    = TLine(padMinX, padMinY, padMaxX, padMinY)
            persistance["pad_bottomEdge"] = TLine(padMinX, padMaxY, padMaxX, padMaxY)

            persistance["pad_leftEdge"].SetLineColor(kBlue)
            persistance["pad_rightEdge"].SetLineColor(kBlue)
            persistance["pad_topEdge"].SetLineColor(kBlue)
            persistance["pad_bottomEdge"].SetLineColor(kBlue)

        edgesX = []
        edgesY = []
        for epoch in doses:
            xEdges = []
            yEdges = []
            for point in epoch['fluxMap']:
                if point['leftLocal'] not in xEdges:
                    xEdges += [point['leftLocal']]
                if point['rightLocal'] not in xEdges:
                    xEdges += [point['rightLocal']]
                if point['topLocal'] not in yEdges:
                    yEdges += [point['topLocal']]
                if point['bottomLocal'] not in yEdges:
                    yEdges += [point['bottomLocal']]
            xEdges.sort()
            yEdges.sort()

            xEdges = cleanEdges(xEdges)
            yEdges = cleanEdges(yEdges)

            edgesX += [xEdges]
            edgesY += [yEdges]

        edgesX = summariseEdges(edgesX)
        edgesY = summariseEdges(edgesY)

        isEmpty = False
        if len(edgesX) <= 1 or len(edgesY) <= 1:
            isEmpty = True
            edgesX = [minX, maxX]
            edgesY = [minY, maxY]

        xArr, yArr = array( 'd' ), array( 'd' )
        for edge in edgesX:
            xArr.append(edge)
        for edge in edgesY:
            yArr.append(edge)

        numBinsX = len(xArr)-1
        numBinsY = len(yArr)-1
        try:
            hist = TH2D("pad_dose_eol", "Pad Dose - End of Life ({}{})".format(integratedLuminosity, " fb^{-1}"), numBinsX, xArr, numBinsY, yArr)
        except TypeError as e:
            print("Pad position: ({}, {})".format((self.maxX + self.minX)/2, (self.maxY + self.minY)/2))
            print("There are {} epochs in doses".format(len(doses)))
            for epoch in doses:
                print(epoch)
            print(" bins x: {}".format(numBinsX))
            print(" bins y: {}".format(numBinsY))
            raise e

        if not isEmpty:
            for binX in range(numBinsX):
                binXPos = (edgesX[binX] + edgesX[binX+1])/2
                for binY in range(numBinsY):
                    binYPos = (edgesY[binY] + edgesY[binY+1])/2
                    dose = 0
                    for epoch in doses:
                        for point in epoch['fluxMap']:
                            if (binXPos > point['leftLocal']   and binXPos < point['rightLocal'] and
                                binYPos > point['bottomLocal'] and binYPos < point['topLocal']):
                                dose += point['flux'] * epochLumi
                                break
                    binx = hist.GetXaxis().FindBin(binXPos)
                    biny = hist.GetYaxis().FindBin(binYPos)
                    hist.SetBinContent(binx, biny, dose)

        hist.SetStats(False)
        hist.GetXaxis().SetTitle( "x [mm]" )
        hist.GetYaxis().SetTitle( "y [mm]" )
        hist.GetZaxis().SetTitle( "#Phi [p / cm^{2}]" )

        hist.Draw('colz')
        persistance['hist'] = hist

        persistance["leftEdge"].Draw("same")
        persistance["rightEdge"].Draw("same")
        persistance["topEdge"].Draw("same")
        persistance["bottomEdge"].Draw("same")

        if not usePadSpacing:
            persistance["pad_leftEdge"].Draw("same")
            persistance["pad_rightEdge"].Draw("same")
            persistance["pad_topEdge"].Draw("same")
            persistance["pad_bottomEdge"].Draw("same")

        return (canv, persistance)

    def maxDoseEOL(self, integratedLuminosity=300, usePadSpacing = True, reuse=None):
        if reuse is not None:
            canv = reuse[0]
            persistance = reuse[1]
        else:
            canv, persistance = self.plotDoseEOL(integratedLuminosity=integratedLuminosity, usePadSpacing=usePadSpacing)

        hist = persistance['hist']

        return hist.GetBinContent(hist.GetMaximumBin())

    def getVoltageEOL(self, chargeFunc, integratedLuminosity=300, usePadSpacing=True, minCharge=10, maxCharge=100, maxVolt=700):
        """
        integratedLuminosity in fb-1
        minCharge in fC - Remember that lower charge typically carries a worse time resolution
        maxCharge in fC - Remember that lower charge typically carries a worse time resolution
        """
        canv, persistance = self.plotDoseEOL(integratedLuminosity=integratedLuminosity, usePadSpacing=usePadSpacing)

        hist = persistance['hist']

        binsX = hist.GetNbinsX()
        binsY = hist.GetNbinsY()

        minV = None
        maxV = None

        allCellsWork = True
        for x in range(1, binsX+1):
            for y in range(1, binsY+1):
                # TODO: add check that bin is in coverage of pad
                phi = hist.GetBinContent(x, y)/2 # Convert from p/cm^2 to neq/cm^2

                minVCell = None
                maxVCell = None

                for Volt in range(1, maxVolt+1):
                    charge = chargeFunc(Volt, phi)
                    if minVCell is None and charge >= minCharge:
                        minVCell = Volt
                    if maxVCell is None and charge > maxCharge:
                        maxVCell = Volt - 1
                        break

                if minVCell is None:
                    allCellsWork = False

                if minV is None:
                    minV = minVCell
                if maxV is None:
                    maxV = maxVCell

                if minVCell is not None and minV is not None:
                    if minVCell > minV:
                        minV = minVCell
                if maxVCell is not None and maxV is not None:
                    if maxVCell < maxV:
                        maxV = maxVCell

        if not allCellsWork:
            minV = None
            maxV = None

        return (minV, maxV)