import ray

##eye = (0.0, 0.0, -10.0)
##screenZ = -7.0

##eye = (0.0, 0.0, -1.4)
##screenZ = eye[2]+0.25

eye = (0.0, 0.0, -1.4)
screenZ = eye[2]+0.35

screenWidth, screenHeight = 0.4, 0.25

def getRay(screenX, screenY, resX, resY):
    screenX -= (resX-1.0)/2
    screenY -= (resY-1.0)/2
    spX = screenX * screenWidth/resX
    spY = (screenHeight-screenY) * screenHeight/resY
    spZ = screenZ
    dir = spX-eye[0], spY-eye[1], spZ-eye[2]
    dir = ray.normalise(*dir)
#    print screenX, screenY
#    print eye, dir
    return ray.Ray(eye, dir)
