from PIL import Image, ImageDraw
import time, random, math

def calculateAreas_mm():
    ''' Calculate the areas each wedge will occupy - precursor to image. ''' 
    innerBulls = pow((12.7/2.0), 2)*math.pi
    outerBulls = pow((31.8/2.0), 2)*math.pi
    totalBulls = innerBulls+outerBulls

    trebleCircle = pow(113.75, 2)*math.pi - pow(105.75, 2)*math.pi
    doubleCircle = pow(176.75, 2)*math.pi - pow(168.75, 2)*math.pi

    trebleWedge = trebleCircle/20.0
    doubleWedge = doubleCircle/20.0

    # We calculate from centerpoint to inner edge of double circle
    singleCircle = pow(168.75, 2)*math.pi - (totalBulls + trebleCircle)
    singleWedge = singleCircle/20.0

    print innerBulls, outerBulls, trebleWedge, doubleWedge, singleWedge

class dartBoard:

    def __init__(self, mult):
        self.xmax = 340
        self.ymax = 340
        self.mult = 1
        self.trueX = self.xmax*self.mult
        self.trueY = self.xmax*self.mult
        self.size = (self.trueX, self.trueY)
        self.board = Image.new("RGB", self.size, "black")
        self.draw = ImageDraw.Draw(self.board) 
        self.arcLabels = [6, 10, 15, 2, 17, 3, 19, 7, 16, \
                          8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13]
        random.seed(time.time())

    def drawRad(self, rad, multiplier):
        wedgeArc = (int(self.trueX/2-(rad*self.mult)), 
                    int(self.trueY/2-(rad*self.mult)), 
                    int(self.trueX/2+(rad*self.mult)), 
                    int(self.trueY/2+(rad*self.mult)))
        for i in range(0, len(self.arcLabels)):
            colStr = "rgb("+str(12*self.arcLabels[i])+", "+multiplier+",0)"
            #colStr = ','.join([str(i*18)]*3)
            #print 18*i, self.arcLabels[i]
            self.draw.pieslice(wedgeArc, (351+(18*i))%360,
                               (351+(18*(i+1)))%360, 
                               fill=colStr) 

    def genDartBoard(self):
        ''' Draws a board with RGB = {value, multiplier, extra} '''
        inBullRad = 12.7 ## inner bullseye
        inBullBBox = (int(self.trueX/2-(inBullRad*self.mult)/2), 
                      int(self.trueY/2-(inBullRad*self.mult)/2), 
                      int(self.trueX/2+(inBullRad*self.mult)/2), 
                      int(self.trueY/2+(inBullRad*self.mult)/2))
        outBullRad = 31.8 ## outer bullseye
        outBullBBox = (int(self.trueX/2-(outBullRad*self.mult)/2), 
                       int(self.trueY/2-(outBullRad*self.mult)/2), 
                       int(self.trueX/2+(outBullRad*self.mult)/2), 
                       int(self.trueY/2+(outBullRad*self.mult)/2))
        dblRad = 170
        self.drawRad(dblRad, "2")
        ssRad = 162
        self.drawRad(ssRad, "1")
        tripRad = 107.4
        self.drawRad(tripRad, "3")
        fsRad = 99.4
        self.drawRad(fsRad, "1")
        self.draw.ellipse(outBullBBox, fill="rgb(0, 1, 0)")
        self.draw.ellipse(inBullBBox, fill="rgb(0, 2, 0)")
        

    def throwDart(self, tgt, pSkill):
        ''' this simulates a throw of the dart at a tgt (x,y) with skill pSkill
            pSkill will be utilized with the random.gauss function to identify
            how often the player hits the target they are aiming for 
            Arguments are an x,y target and a tuple (a,g) of average distance 
            away and total allowable distance from target.
        '''
        hitX = int(tgt[0]+random.gauss(pSkill[0], pSkill[1]))
        hitY = int(tgt[1]+random.gauss(pSkill[0], pSkill[1]))
        if(hitX<self.trueX) and (hitX>0) and (hitY<self.trueY) and (hitY>0):
            hit = (hitX, hitY)
            r,g,b = self.board.getpixel(hit)
            if(b<247):
                self.board.putpixel(hit, (r, g, b+30))
            #print hitX,hitY 
            return(r/12, g)
        
    def saveBoard(self):
        self.board.save("./output/"+str(time.time()).split(".")[0]+".BMP", "BMP")

    def retAimPoint(self, aimVal):
        if(aimVal!=0) and ((aimVal<15) and (aimVal>20)):
            raise ValueError(str(aimVal)+" is not a valid target.")
        if(aimVal==0):
            return(self.trueX/2, self.trueY/2)
        valueAngles = [[15,2], [17,4], [19,6], [16,8], [20,15],[18,17]]
        angleDict = dict()
        for k in valueAngles:
            angleDict[k[0]] = (18*k[1])
        #print angleDict
        return(int(math.cos(math.radians(angleDict[aimVal]))*103.4*self.mult)+self.trueX/2, 
               int(math.sin(math.radians(angleDict[aimVal]))*103.4*self.mult)+self.trueY/2)


def evalScore(scoreD):
    ''' returns sum of a dict; should be 21 for a win. '''
    tSum = 0
    for i in scoreD:
        if(scoreD[i]>3):
            tSum+=3
        else:
            tSum+=scoreD[i]
    return(tSum)

def initScoreDict(): 
    scoreDict = dict()
    for i in range(15,21):
        scoreDict[i] = 0
    scoreDict[0] = 0
    return(scoreDict)

def playBullseyeGame():
    pass
 
if(__name__=="__main__"):
    db = dartBoard(2)
    db.genDartBoard()
    skill = (20, 100)
    #skill = (0,0)
    ## Generic Strategy:
    ##  Throw the darts at the bullseye, anything that you hit, you take.
    scoreDict = initScoreDict()
    print "Generic Strategy: Bullseye Targeting"
    print scoreDict

    shotCount = 0
    while(scoreDict[0]<3):
        t = db.throwDart(db.retAimPoint(0), skill)
        if(t!=None) and (t[0] in scoreDict):
            scoreDict[t[0]] += t[1]
            #print evalScore(scoreDict),
            #print t#, scoreDict
        shotCount+=1
    if(evalScore(scoreDict)<21):
        print "Evasive action!"
    print shotCount, scoreDict

    print "Gentlemen's Strategy: 20-15, then Bulls"
    gentStrat = initScoreDict()
    print gentStrat
    shotCount = 0
    for i in [20,19,18,17,16,15,0]:
        while(gentStrat[i]<3):
            t = db.throwDart(db.retAimPoint(i), skill)
            #print i, db.retAimPoint(i), t
            if(t!=None) and (t[0]==i):
                gentStrat[t[0]] += t[1]
            shotCount+=1
    print shotCount, gentStrat
    #db.saveBoard()
