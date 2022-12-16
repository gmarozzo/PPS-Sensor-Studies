from __future__ import annotations

class PPSHitmap:
    map: dict
    maxFluence: dict
    def __init__(self,
                 filename,
                 station,
                 approximateDetectorEdge, # in mm
                 physics = True,
                 calib = False,
                 xMin = 0.0, # in m
                 xMax = 0.042, # in m
                 xStep = 0.00005, # in m
                 yMin = -0.042, # in m
                 yMax = 0.042, # in m
                 yStep = 0.00005, # in m
                 betastar = 0.15,
                 verbose = False,
                 addBackgroundFlux = None
                ):
        self.filename = filename
        self.station = station
        self.physics = physics
        self.calib = calib

        self.xMin = xMin
        self.xMax = xMax
        self.xStep = xStep

        self.yMin = yMin
        self.yMax = yMax
        self.yStep = yStep

        self.betastar = betastar
        if self.betastar != 0.15:
            raise Exception("Betastar {} not implemented".format(self.betastar)) # Copy from Mario

        self.verbose = verbose

        self.addBackgroundFlux = addBackgroundFlux

        if self.physics and self.calib:
            raise Exception("File {} has both physics and calibration set to true".format(self.filename))

        self.df = None

        self.map = {}

        self.validated = False

        self.nsigma = 15.9 # For physics
        if self.calib:
            self.nsigma = 7 # For calibration

        self.xmargin = 0.5e-3 # Window Thickness + gap
        ## Missing optics data in order to be able to compute detector edges...
        #self.detectorEdge = self.nsigma * sigma_x_15[i] + self.xmargin
        self.detectorEdge = approximateDetectorEdge/1000 # save the number in m for internal consistency

    def validate(self):
        self._checkMap()
        if self.verbose:
            print("From {} to {} every {}: Range of {} in {} steps (x-axis)".format(self.xMin, self.xMax, self.xStep, self.xMax - self.xMin, ((self.xMax - self.xMin)/self.xStep)))
            print("From {} to {} every {}: Range of {} in {} steps (y-axis)".format(self.yMin, self.yMax, self.yStep, self.yMax - self.yMin, ((self.yMax - self.yMin)/self.yStep)))
        edgeIdx = int((self.detectorEdge - self.xMin)/self.xStep)
        self.maxFluence = {}
        self.ridge = {}
        for xIdx in range(int((self.xMax - self.xMin)/self.xStep)):
            xVal = round(self.xMin + xIdx*self.xStep, 6)
            for yIdx in range(int((self.yMax - self.yMin)/self.yStep)):
                yVal = round(self.yMin + yIdx*self.yStep, 6)

                if not (xVal in self.map and yVal in self.map[xVal]):
                    raise Exception("Did not find a fluence entry for {} for x={}, y={}".format(self.filename, xVal, yVal))

                if xIdx >= edgeIdx:
                    if (self.maxFluence is None) or (self.map[xVal][yVal] > self.maxFluence["fluence"]):
                        self.maxFluence = {
                            "x": xVal,
                            "y": yVal,
                            "xIdx": xIdx,
                            "yIdx": yIdx,
                            "fluence": self.map[xVal][yVal]
                        }
                if (xIdx not in self.ridge) or (self.map[xVal][yVal] > self.ridge[xIdx]["fluence"]):
                    self.ridge[xIdx] = {
                        "x": xVal,
                        "y": yVal,
                        "xIdx": xIdx,
                        "yIdx": yIdx,
                        "fluence": self.map[xVal][yVal]
                    }
        self.validated = True
        #self._freeMap()

        if self.verbose and self.maxFluence is not None:
            print("Max fluence at x={}, y={}, fluence={}".format(self.maxFluence["x"], self.maxFluence["y"], self.maxFluence["fluence"]))
            print("Pad edge at x={}".format(edgeIdx * self.xStep + self.xMin))

    #def ___validate_old(self):
    #    seld._checkDF() if self.verbose:
    #        print("From {} to {} every {}: Range of {} in {} steps (x-axis)".format(self.xMin, self.xMax,
    #    self.xStep, self.xMax - self.xMin, ((self.xMax - self.xMin)/self.xStep))) print("From {} to {} every {}:
    #    Range of {} in {} steps (y-axis)".format(self.yMin, self.yMax, self.yStep, self.yMax - self.yMin,
    #    ((self.yMax - self.yMin)/self.yStep))) for xIdx in range(int((self.xMax - self.xMin)/self.xStep)):
    #        xVal = round(self.xMin + xIdx*self.xStep, 6)

    #        xRows = self.df.loc[self.df["xPos"] == xVal] for yIdx in range(int((self.yMax -
    #        self.yMin)/self.yStep)):
    #            yVal = round(self.yMin + yIdx*self.yStep, 6)

    #            #if len(self.df.loc[(self.df["xPos"] == xVal) & (self.df["yPos"] == yVal)]) != 1:
    #            if len(xRows.loc[xRows["yPos"] == yVal]) != 1:
    #                raise Exception("Did not find a fluence entry for {} for x={}, y={}".format(self.filename,
    #    xVal, yVal)) self.validated = True self._freeDF()

    def _checkValid(self):
        if not self.validated:
            print("The file {} has not yet been validated to contain all points, it will be validated now and may take some time, if the file has been previously validated, you can remove this check by setting the validated property to True".format(self.filename))
            self.validate()

            if not self.validated:
                raise Exception("There was a problem validatind the file {}".format(self.filename))

    #def _checkDF(self):
    #    if self.df is None:
    #        self._loadDF()

    #def _loadDF(self):
    #    self.df = pd.read_csv(self.filename, delim_whitespace=True, names=['xPos', 'yPos', 'fluence']) if
    #    self.verbose:
    #        self.df.info() print()

    #def _freeDF(self):
    #    if self.df is not None:
    #        self.df = None

    def _checkMap(self):
        if self.map is None:
            self._loadMap()

    def _loadMap(self):
        self.map = {}
        with open(self.filename) as file:
            for line in file:
                # Units are in m and fix type
                pLine = [float(x) for x in line.rstrip().split(' ')]

                if pLine[0] not in self.map:
                    self.map[pLine[0]] = {}

                self.map[pLine[0]][pLine[1]] = pLine[2]
                if self.addBackgroundFlux is not None:
                    self.map[pLine[0]][pLine[1]] += self.addBackgroundFlux

    def _freeMap(self):
        if self.map is not None:
            self.map = {}

    def getHisto(self, name, title):
        self._checkMap()

        from ROOT import TH2D  # type: ignore
        from ROOT import kFALSE  # type: ignore
        import ROOT

        binX = int((self.xMax - self.xMin)/self.xStep) + 1
        xMin = self.xMin - self.xStep/2
        xMax = self.xMax + self.xStep/2
        binY = int((self.yMax - self.yMin)/self.yStep) + 1
        yMin = self.yMin - self.yStep/2
        yMax = self.yMax + self.yStep/2
        hist = TH2D(name, title, binX, xMin*1000, xMax*1000, binY, yMin*1000, yMax*1000) # *1000 for units in mm
        hist.SetStats(kFALSE)
        hist.GetXaxis().SetTitle( "x [mm]" )
        hist.GetYaxis().SetTitle( "y [mm]" )
        hist.GetZaxis().SetTitle( "#Phi [p / (cm^{2} fb^{-1})]" )
        #hist.GetXaxis().SetTitleSize( 0.04 ) hist.GetYaxis().SetTitleSize( 0.04 ) hist.GetZaxis().SetTitleSize(
        #0.04 )
        hist.GetXaxis().SetTitleOffset(0.9)
        hist.GetYaxis().SetTitleOffset(1.7)
        hist.GetZaxis().SetTitleOffset(1.6)
        hist.GetYaxis().SetLabelOffset(0.01)
        #hist.GetXaxis().SetTitleFont(62) hist.GetYaxis().SetTitleFont(62) hist.GetZaxis().SetTitleFont(62)
        #hist.GetXaxis().SetLabelFont(62) hist.GetYaxis().SetLabelFont(62) hist.GetZaxis().SetLabelFont(62)

        for xIdx in range(int((self.xMax - self.xMin)/self.xStep)):
            xVal = round(self.xMin + xIdx*self.xStep, 6)
            for yIdx in range(int((self.yMax - self.yMin)/self.yStep)):
                yVal = round(self.yMin + yIdx*self.yStep, 6)
                hist.SetBinContent(hist.FindBin(xVal*1000, yVal*1000), self.map[xVal][yVal])

        return hist

    def peakUniformPadOccupancy(self, xLen, yLen):
        """xLen and yLen in m"""

        # Convert Phi 1fb-1 to Phi BX - multiply by 1.6 x 10^-12 Phi in units of particles/cm^2 Occupancy in units
        # of particles
        if self.maxFluence is not None:
            return self.maxFluence["fluence"] * 1.6E-12 * (xLen * yLen) * 1.0E4
        else:
            return None

    def integratePadOccupancy(self, xLen, yLen):
        """xLen and yLen in m"""
        self._checkMap()
        from math import ceil, floor

        # Convert Phi 1fb-1 to Phi BX - multiply by 1.6 x 10^-12 Phi in units of particles/cm^2 Occupancy in units
        # of particles

        xBins = ceil(xLen/self.xStep)
        yBins = ceil(yLen/self.yStep * 0.5 - 0.5) * 2 + 1
        minY = self.maxFluence["yIdx"] - floor(yBins/2)
        maxY = self.maxFluence["yIdx"] + floor(yBins/2)

        leftPad = self.maxFluence["x"] - self.xStep/2
        rightPad = self.maxFluence["x"] - self.xStep/2 + xLen
        bottomPad = self.maxFluence["y"] - yLen/2
        topPad = self.maxFluence["y"] + yLen/2

        fluence = 0
        for xIdx in range(self.maxFluence["xIdx"], self.maxFluence["xIdx"] + xBins):
            xVal = round(self.xMin + xIdx*self.xStep, 6)
            for yIdx in range(minY, maxY + 1):
                yVal = round(self.yMin + yIdx*self.yStep, 6)
                left = xVal - self.xStep/2
                right = xVal + self.xStep/2
                bottom = yVal - self.yStep/2
                top = yVal + self.yStep/2

                contributionX = 1
                if right > rightPad:
                    contributionX -= (right - rightPad)/self.xStep

                contributionY = 1
                if top > topPad:
                    contributionY -= (top - topPad)/self.yStep
                if bottom < bottomPad:
                    contributionY -= (bottomPad - bottom)/self.yStep
                fluence += self.map[xVal][yVal] * contributionX * contributionY

        occupancy = fluence * 1.6E-12 * (self.xStep * self.yStep) * 1.0E4
        return occupancy

    def plotShifts(self, integratedLuminosity=300, padLength = 1.3, numCols = 2, maxNumShifts=4, thresholdFlux = None, baseColor = None, colorOffset=3, drawOneSided=False):
        self._checkMap()
        self._checkValid()
        #print(self.maxFluence)
        #print(self.ridge)
        #print("Done!")

        firstIdx = None
        for idx in range(len(self.ridge)):
            if self.ridge[idx]["x"] >= self.detectorEdge:
                firstIdx = idx
                break
        if firstIdx is None:
            raise ValueError("There was a problem, unable to find the maximum of the map within the detector window")


        from ROOT import TCanvas  # type: ignore
        from ROOT import TH1D  # type: ignore
        from ROOT import TLine  # type: ignore
        from ROOT import TGraph  # type: ignore
        from ROOT import TLegend  # type: ignore
        from ROOT import kRed, kAzure  # type: ignore
        from array import array

        persistance = {}
        canv = TCanvas("sensor_shifts", "Sensor Shifts", numCols*600, 600)
        canv.Divide(numCols, 1)

        if thresholdFlux is not None:
            persistance["ThresholdLine"] = TLine(0, thresholdFlux, 10, thresholdFlux)
            persistance["ThresholdLine"].SetLineColor(kRed)
            persistance["ThresholdLine"].SetLineStyle(2)

        idx = 0
        for col in range(numCols):
            idx += 1
            pad = canv.cd(idx)
            pad.SetLogy()
            pad.SetTicks()

            hist = TH1D("shifts_col_{}".format(col), "Column {} Shifts at {} {}".format(col, integratedLuminosity, "fb^{-1}"), 2, 0, 10)

            hist.SetStats(False)
            hist.GetXaxis().SetTitle( "#Delta y [mm]" )
            hist.GetYaxis().SetTitle( "#Phi [p / cm^{2}]" )
            #hist.GetZaxis().SetTitleOffset(1.8)

            hist.Draw()

            persistance["hist_{}".format(col)] = hist

            if thresholdFlux is not None:
                persistance["ThresholdLine"].Draw("same")

            # Fetch ridge position indexes for current column
            xIdx = self.ridge[firstIdx+int(col*(padLength)/(self.xStep*1000))]['xIdx']
            yIdx = self.ridge[firstIdx+int(col*(padLength)/(self.xStep*1000))]['yIdx']

            persistance["col_{}_legend".format(col)] = TLegend(0.75,0.9,0.9,0.9 - 0.05*maxNumShifts)

            minFlux = None
            maxFlux = None
            if baseColor is None:
                baseColor = kAzure
            for nShift in range(1, maxNumShifts+1):
                lineColor = baseColor + colorOffset*(nShift-1)
                xArr, yArrMed, yArrUp, yArrDown = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )

                for shiftIdx in range(1,int(0.01/(nShift*self.yStep))):
                    shift = shiftIdx * self.yStep * nShift # Total shift
                    xArr.append(shift * 1000)

                    fluxMed = 0
                    for i in range(nShift + 1):
                        index = -int(nShift/2) + i
                        xVal = round(self.xMin + xIdx*self.xStep, 6)
                        yVal = round(self.yMin + (yIdx + index*shiftIdx)*self.yStep, 6)
                        fluxMed += self.map[xVal][yVal] * integratedLuminosity/(nShift+1)
                    yArrMed.append(fluxMed)

                    fluxPlus = 0
                    for i in range(nShift + 1):
                        xVal = round(self.xMin + xIdx*self.xStep, 6)
                        yVal = round(self.yMin + (yIdx + i*shiftIdx)*self.yStep, 6)
                        fluxPlus += self.map[xVal][yVal] * integratedLuminosity/(nShift+1)
                    yArrUp.append(fluxPlus)

                    fluxMinus = 0
                    for i in range(nShift + 1):
                        xVal = round(self.xMin + xIdx*self.xStep, 6)
                        yVal = round(self.yMin + (yIdx - i*shiftIdx)*self.yStep, 6)
                        print("xVal: {}; yVal: {}; nShift: {}".format(xVal,yVal,nShift))
                        print(self.map[xVal].keys())
                        fluxMinus += self.map[xVal][yVal] * integratedLuminosity/(nShift+1)
                    yArrDown.append(fluxMinus)

                    if minFlux is None:
                        minFlux = fluxPlus
                    if maxFlux is None:
                        maxFlux = fluxPlus

                    if fluxPlus > maxFlux:
                        maxFlux = fluxPlus
                    if fluxPlus < minFlux:
                        minFlux = fluxPlus

                    if fluxMinus > maxFlux:
                        maxFlux = fluxMinus
                    if fluxMinus < minFlux:
                        minFlux = fluxMinus

                    if fluxMed > maxFlux:
                        maxFlux = fluxMed
                    if fluxMed < minFlux:
                        minFlux = fluxMed

                graphMed  = TGraph(len(xArr), xArr, yArrMed)
                graphUp   = TGraph(len(xArr), xArr, yArrUp)
                graphDown = TGraph(len(xArr), xArr, yArrDown)
                graphMed.SetLineColor(lineColor)
                graphUp.SetLineColor(lineColor)
                graphDown.SetLineColor(lineColor)
                graphUp.SetLineStyle(3)
                graphDown.SetLineStyle(3)

                graphMed.Draw("l same")
                if drawOneSided:
                    graphUp.Draw("l same")
                    graphDown.Draw("l same")

                persistance["col_{}_graph_med_{}".format(col,nShift)]   = graphMed
                persistance["col_{}_graph_up_{}".format(col,nShift)]   = graphUp
                persistance["col_{}_graph_down_{}".format(col,nShift)] = graphDown

                persistance["col_{}_legend".format(col)].AddEntry(graphMed, "n = {}".format(nShift), "l")
            persistance["col_{}_legend".format(col)].Draw("same")

            if thresholdFlux is not None and thresholdFlux > maxFlux:
                maxFlux = thresholdFlux * 1.05
            else:
                if maxFlux is not None:
                    maxFlux *= 1.1
                else:
                    maxFlux = 1e15
            if thresholdFlux is not None and thresholdFlux < minFlux:
                minFlux = thresholdFlux * 0.95
            else:
                if minFlux is not None:
                    minFlux *= 0.9
                else:
                    minFlux = 1e10

            if maxFlux/minFlux < 10:
                minFlux = maxFlux/10

            hist.SetMinimum(minFlux)
            hist.SetMaximum(maxFlux)


        return canv, persistance

    def squarePadPeakUniformScan(self, bins, minPad, maxPad, doLog = False):
        if bins <= 1:
            return (None, None)
        if doLog and minPad == 0:
            return (None, None)

        from math import log
        padSize = []
        occupancy = []

        step = (maxPad - minPad)/(bins-1)
        if doLog:
            step = (log(maxPad,2) - log(minPad,2))/(bins-1)

        for ibin in range(bins):
            if doLog:
                padSize += [2**(ibin * step + log(minPad,2))]
            else:
                padSize += [ibin * step + minPad]
            occupancy += [self.peakUniformPadOccupancy(padSize[ibin], padSize[ibin])]

        return (padSize,occupancy)

    def squarePadIntegrateScan(self, bins, minPad, maxPad, doLog = False):
        if bins <= 1:
            return (None, None)
        if doLog and minPad == 0:
            return (None, None)

        from math import log
        padSize = []
        occupancy = []

        step = (maxPad - minPad)/(bins-1)
        if doLog:
            step = (log(maxPad,2) - log(minPad,2))/(bins-1)

        for ibin in range(bins):
            if doLog:
                padSize += [2**(ibin * step + log(minPad,2))]
            else:
                padSize += [ibin * step + minPad]
            occupancy += [self.integratePadOccupancy(padSize[ibin], padSize[ibin])]

        return (padSize,occupancy)

    def squarePadPeakUniformGraph(self, bins, minPad, maxPad, padScale = 1, doLog = False):
        from ROOT import TGraph  # type: ignore

        from array import array
        (padSize, occupancy) = self.squarePadPeakUniformScan(bins, minPad, maxPad, doLog = doLog)
        if padSize is None or occupancy is None:
            return None
        for ibin in range(len(padSize)):
            padSize[ibin] = padSize[ibin] * padScale

        x, y = array( 'd' ), array( 'd' )
        graph = None
        for ibin in range(len(padSize)):
            x.append(padSize[ibin])
            if occupancy[ibin] is not None:
                y.append(occupancy[ibin])
            else:
                y.append(0)
                print("There was a not defined occupancy, using the value 0 to avoid a crash")
            graph = TGraph(bins, x, y)

        return graph

    def squarePadIntegrateGraph(self, bins, minPad, maxPad, padScale = 1, doLog = False):
        from ROOT import TGraph  # type: ignore
        from array import array

        (padSize, occupancy) = self.squarePadIntegrateScan(bins, minPad, maxPad, doLog = doLog)
        if padSize is None or occupancy is None:
            return None
        padSize = [pad*padScale for pad in padSize]

        x, y = array( 'd' ), array( 'd' )
        graph = None
        for ibin in range(len(padSize)):
            x.append(padSize[ibin])
            if occupancy[ibin] is not None:
                y.append(occupancy[ibin])
            else:
                y.append(0)
                print("There was a not defined occupancy, using the value 0 to avoid a crash")
            graph = TGraph(bins, x, y)

        return graph
