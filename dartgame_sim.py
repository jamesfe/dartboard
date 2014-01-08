import Image, ImageDraw
import time
import math

def calculateAreas_mm():
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


