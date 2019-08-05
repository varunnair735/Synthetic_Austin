'''
Created on 09.03.2010

@author: andi

* reads current position, rotation from fbx file
* sets CE camera to the parsed values
Note: camera needs to be exported as single object.
anim curves are not read, only camera transformation of current frame
fbx file needs to be ascii, version <= 2010, y-Up

'''
from scripting import *
import time
# get a CityEngine instance
ce = CE()



'''
parse lines and look for id
prepare cam data in array
non-generic, works for specific fbx part only
'''

def drange(x, y, jump):
      while x < y:
        yield x
        x += jump

def parseLine(lines, id):
    data = False
    for line in lines:
        if line.find(id) >=0 :
            data = line.partition(id)[2]
            break
    if data:
        data = data[:len(data)-1] # strip \n
        data = data.split(",")
    return data

'''
parse lines from fbx file that store cam data
'''
def parseFbxCam(filename):
    f=open(filename)
    lines = f.readlines()
    cnt = 0
    loc =  parseLine(lines, 'Property: "Lcl Translation", "Lcl Translation", "A+",')
    rot =  parseLine(lines, 'Property: "Lcl Rotation", "Lcl Rotation", "A+",')
    return [loc,rot]



'''
helper functions
'''
def setCamPosV(v, vec):
    v.setCameraPosition(vec[0], vec[1], vec[2])

def setCamRotV(v, vec):
    v.setCameraRotation(vec[0], vec[1], vec[2])


'''
sets camera on first CE viewport
'''
def setCamData(data):
    v = ce.getObjectsFrom(ce.get3DViews(), ce.isViewport)[0]
    setCamPosV(v, data[0])
    setCamRotV(v, data[1])
    return v


'''
master function
'''
def importFbxCamera(fbxfile, axis):

    data = parseFbxCam(fbxfile)
    if(data[0] and data[1]) :
        data[0][0]=str(axis[0])
        data[0][1] = '175'
        data[0][2]= str(axis[1])
        data[1][0] = data[1][1]='-90.00'
        v = setCamData(data)
        #print "Camera set to "+str(data)
        return v
    else:
        print "No camera data found in file "+file

def exportImages(directory, v, Tag=""):
   path = directory + "/_" + Tag + "_RGB.jpg"
   v.snapshot(path)

def exportGroundtruths(directory, v, Tag=""):
   path = directory + "/_" + Tag + "_GT.jpg"
   v.snapshot(path)

def loop_capturer(start_axis, step, end_axis, tag, mode='RGB'):
    counter = 0
    print('Start Shooting!')
    print(start_axis[0], end_axis[0], step)
    for i in drange(start_axis[0], end_axis[0], step):
        for j in drange(start_axis[1], end_axis[1], step):
            camfile = ce.toFSPath("data/camera.fbx")
            view = importFbxCamera(camfile, (i, j))
            counter += 1
            print(counter)
            time.sleep(0.02)
            if mode == 'RGB':
                exportImages(ce.toFSPath('images/austin4/raw'), view, Tag=tag+'_'+str(counter))
            else:
                exportGroundtruths(ce.toFSPath('images/austin4/raw'), view, Tag=tag+'_'+str(counter))
            #break

if __name__ == '__main__':
    loop_capturer((-1600, -2400), 182, (1400, 1000), 'austin4', mode='RGB')
