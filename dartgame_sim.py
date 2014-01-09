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
        self.draw.ellipse(outBullBBox, fill="rgb(0, 2, 0)")
        self.draw.ellipse(inBullBBox, fill="rgb(0, 1, 0)")
        

    def throwDart(self, tgt, pSkill):
        ''' this simulates a throw of the dart at a tgt (x,y) with skill pSkill
            pSkill will be utilized with the random.gauss function to identify
            how often the player hits the target they are aiming for '''
        hitX = int(tgt[0]+random.gauss(pSkill[0], pSkill[1]))
        hitY = int(tgt[1]+random.gauss(pSkill[0], pSkill[1]))
        if(hitX<self.trueX) and (hitX>0) and (hitY<self.trueY) and (hitY>0):
            hit = (hitX, hitY)
            r,g,b = self.board.getpixel(hit)
            if(b<247):
                self.board.putpixel(hit, (r, g, b+30))
            return(r/12, g)
        
    def saveBoard(self):
        self.board.save("./output/"+str(time.time()).split(".")[0]+".BMP", "BMP")

if(__name__=="__main__"):
    db = dartBoard(2)
    db.genDartBoard()
    for i in range(1000):
        db.throwDart((170, 170), (20, 169))
    db.saveBoard()
