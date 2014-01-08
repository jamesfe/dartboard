from PIL import Image, ImageDraw
import time
import math

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
        self.mult = 2
        self.trueX = self.xmax*self.mult
        self.trueY = self.xmax*self.mult
        self.size = (self.trueX, self.trueY)
        self.board = Image.new("RGB", self.size, "black")
        self.draw = ImageDraw.Draw(self.board) 
        self.arcLabels = [6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5, 20, 1, 18, 4, 13]

    def drawRad(self, rad):
        wedgeArc = (int(self.trueX/2-(rad*self.mult)), 
                    int(self.trueY/2-(rad*self.mult)), 
                    int(self.trueX/2+(rad*self.mult)), 
                    int(self.trueY/2+(rad*self.mult)))
        for i in range(0, len(self.arcLabels)):
            colStr = ','.join([str(i*18)]*3)
            self.draw.pieslice(wedgeArc, (354+(18*i))%360, (354+(18*(i+1)))%360, fill="rgb("+colStr+")") 
     

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
        fsRad = 99.4+(12.7/2)
        self.drawRad(fsRad)

        self.draw.ellipse(outBullBBox, fill="#00dd00")
        self.draw.ellipse(inBullBBox, fill="#ff0000")
        
        self.board.save("./output/"+str(time.time()).split(".")[0]+".BMP", "BMP")


if(__name__=="__main__"):
    db = dartBoard(2)
    db.genDartBoard() 
