from dice_img_lib import const as cst
from dice_img_lib import camera
import numpy as np

def szkolenie():
    best = [0,0,0]
    licznik=0

    for i in np.arange(cst.rescaleH_per_min[1], cst.rescaleH_per_min[2], step=cst.rescaleH_per_min[3]):
        for k in np.arange(cst.rescaleH_per_max[1], cst.rescaleH_per_max[2], step=cst.rescaleH_per_max[3]):
            cst.rescaleH_per_min[0]=i
            cst.rescaleH_per_max[0]=k
            res = camera.checkImages()
            licznik+=1
            print("L:"+str(licznik))
            if(res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("H: "+ str(i)+"    "+str(k)+"    "+str(res))
    cst.rescaleH_per_min[0] = best[1]
    cst.rescaleH_per_max[0] = best[2]
    best = [0,0,0]
    licznik=0

    for i in np.arange(cst.rescaleS_per_min[1], cst.rescaleS_per_min[2], step=cst.rescaleS_per_min[3]):
        for k in np.arange(cst.rescaleS_per_max[1], cst.rescaleS_per_max[2], step=cst.rescaleS_per_max[3]):
            cst.rescaleS_per_min[0]=i
            cst.rescaleS_per_max[0]=k
            res = camera.checkImages()
            licznik+=1
            print("L:"+str(licznik)+"    "+str(res))
            if(res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("S: "+str(i)+"    "+str(k)+"    "+str(res))
    cst.rescaleS_per_min[0] = best[1]
    cst.rescaleS_per_max[0] = best[2]
    best = [0,0,0]
    licznik=0

    for i in np.arange(cst.rescaleV_per_min[1], cst.rescaleV_per_min[2], step=cst.rescaleV_per_min[3]):
        for k in np.arange(cst.rescaleV_per_max[1], cst.rescaleV_per_max[2], step=cst.rescaleV_per_max[3]):
            cst.rescaleV_per_min[0]=i
            cst.rescaleV_per_max[0]=k
            res = camera.checkImages()
            licznik+=1
            print("L:"+str(licznik)+"    "+str(res))
            if(res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("V: "+str(i)+"    "+str(k)+"    "+str(res))
    cst.rescaleV_per_min[0] = best[1]
    cst.rescaleV_per_max[0] = best[2]

    best = [0, 0, 0]
    licznik = 0

    for i in np.arange(cst.progH_min[1], cst.progH_min[2], step=cst.progH_min[3]):
        for k in np.arange(cst.progH_max[1], cst.progH_max[2], step=cst.progH_max[3]):
            cst.progH_min[0] = i
            cst.progH_max[0] = k
            res = camera.checkImages()
            licznik += 1
            print("L:" + str(licznik) + "    " + str(res))
            if (res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("PROGH: " + str(i) + "    " + str(k) + "    " + str(res))
    cst.progH_min[0] = best[1]
    cst.progH_max[0] = best[2]

    best = [0, 0, 0]
    licznik = 0

    for i in np.arange(cst.progS_min[1], cst.progS_min[2], step=cst.progS_min[3]):
        for k in np.arange(cst.progS_max[1], cst.progS_max[2], step=cst.progS_max[3]):
            cst.progS_min[0] = int(i)
            cst.progS_max[0] = int(k)
            res = camera.checkImages()
            licznik += 1
            print("L:" + str(licznik) + "    " + str(res))
            if (res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("PROGS: " + str(i) + "    " + str(k) + "    " + str(res))
    cst.progS_min[0] = best[1]
    cst.progS_max[0] = best[2]

    best = [0, 0, 0]
    licznik = 0

    for i in np.arange(cst.progV_min[1], cst.progV_min[2], step=cst.progV_min[3]):
        for k in np.arange(cst.progV_max[1], cst.progV_max[2], step=cst.progV_max[3]):
            cst.progV_min[0] = i
            cst.progV_max[0] = k
            res = camera.checkImages()
            licznik += 1
            print("L:" + str(licznik) + "    " + str(res))
            if (res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("PROGV: " + str(i) + "    " + str(k) + "    " + str(res))
    cst.progV_min[0] = best[1]
    cst.progV_max[0] = best[2]





    best = [0, 0, 0]
    licznik = 0

    for i in np.arange(cst.progS_min[1], cst.progS_min[2], step=cst.progS_min[3]):
        for k in np.arange(cst.progV_min[1], cst.progV_min[2], step=cst.progV_min[3]):
            cst.progS_min[0] = i
            cst.progV_min[0] = k
            res = camera.checkImages()
            licznik += 1
            print("L:" + str(licznik) + "    " + str(res))
            if (res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("PROGV: " + str(i) + "    " + str(k) + "    " + str(res))
    cst.progS_min[0] = best[1]
    cst.progV_min[0] = best[2]






    best = [0, 0, 0]
    licznik = 0

    for i in np.arange(cst.progMorSize[1], cst.progMorSize[2], step=cst.progMorSize[3]):
        for k in np.arange(cst.progMorRepe[1], cst.progMorRepe[2], step=cst.progMorRepe[3]):
            cst.progMorSize[0] = i
            cst.progMorRepe[0] = k
            res = camera.checkImages()
            licznik += 1
            print("L:" + str(licznik) + "    " + str(res))
            if (res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("MOR: " + str(i) + "    " + str(k) + "    " + str(res))
    cst.progMorSize[0] = best[1]
    cst.progMorRepe[0] = best[2]

    best = [0, 0, 0]
    licznik = 0
    for k in np.arange(cst.bilaX[1], cst.bilaX[2], step=cst.bilaX[3]):
        cst.bilaX[0] = k
        res = camera.checkImages()
        licznik += 1
        print("L:" + str(licznik) + "    " + str(res))
        if (res - best[0] > 0.00001):
            best[0] = res
            best[2] = k
            print("BIL: " + str(k) + "    " + str(res))

    best = [0, 0, 0]
    licznik = 0

    for i in np.arange(cst.bilaY[1], cst.bilaY[2], step=cst.bilaY[3]):
        for k in np.arange(cst.bilaZ[1], cst.bilaZ[2], step=cst.bilaZ[3]):
            cst.bilaY[0] = i
            cst.bilaZ[0] = k
            res = camera.checkImages()
            licznik += 1
            print("L:" + str(licznik) + "    " + str(res))
            if (res - best[0] > 0.00001):
                best[0] = res
                best[1] = i
                best[2] = k
                print("BILA Y Z: " + str(i) + "    " + str(k) + "    " + str(res))
