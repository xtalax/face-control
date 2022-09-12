from facedetector import Face
import pyautogui as pag
from utils import *
from ControlSettings import *
import gestures
import time

def control(detector, b):

    while 1: #loop until face detected
        points, frame = detector.detect_faces()
        if points is not None:
            break
            
    face = Face(points, frame)
    settings = ControlSettings(detector, face, b)

    #Wait until eye threshold is calibrated and history filled
    while not face.gazecalibrated:
        points, frame = detector.detect_faces()
        if points is None:
            continue
        face.update(points, frame)
    elapsed = 0.1
    while 1:
        start = time.time()
        points, frame = detector.detect_faces()
        if points is None:
            continue
        face.update(points, frame)
        settings.update(face, b, elapsed)
        
        #Reset scrolling state if timer has elapsed, plus an average tick
        if time.time() > settings.scrolltime + settings.scrolldelay + settings.steptime: 
            settings.isscrolling = False
            settings.scrollstarted = False

# --------------------------------
# # Gesture detection logic
# --------------------------------

        if face.diffar > b.wink:
            if face.leftar < face.rightar:
                if face.leftar < b.squint:
                    gestures.leftwink(face, b, settings)

            elif face.leftar > face.rightar:
                if face.rightar < b.squint:
                    gestures.rightwink(face, b, settings)
        if (face.moutharea > b.omouth) and (face.mar < b.pog):
            gestures.mouthopen(face, b, settings)
            if face.moutharea > b.mouthopen: # if mouth open
                gestures.widemouth(face, b, settings)

            elif (face.smilefactor > b.smile) and (face.moutharea > b.smilearea): # if smile
                gestures.smile(face, b, settings)
            else:
                gestures.omouth(face, b, settings)
        
        # elif face.frownfactor > b.frown: # if frown
        #     gestures.frown(face, b, settings)
                
        else:    
            gestures.restingmouth(face, b, settings)
                       
        if face.eyear < b.squint:
            gestures.squint(face, b, settings)
        elif face.eyear > b.wide:
            gestures.wideeyes(face, b, settings)
        else:
            gestures.restingeyes(face, b, settings)


        if face.mar > b.pog: #if pog, calibrate
            gestures.pog(face, b, settings)

        if face.browdist > b.browraised: # if brows raised
            gestures.raisedbrows(face, b, settings)
        else:
            gestures.restingbrows(face, b, settings)
        if settings.isscrolling:
            gestures.isscrolling(face, b, settings) # commands to run every time
        else:
            gestures.mousemode(face, b, settings)

        if abs(settings.eyex) > 5:
            settings.screen.root.xfixes_hide_cursor()
            settings.display.sync()
        else:
            settings.screen.root.xfixes_show_cursor()#
            settings.display.sync()

        if settings.calibrate:
            break

            
        end = time.time()
        elapsed = start - end

        
