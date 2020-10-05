from datetime import datetime
from GA import GA
from Colorharmony import ColorHarmony
import cv2
import numpy
import PIL as PIL
from PIL import ImageDraw,Image
from skimage.color import lab2rgb
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk
import time




class Solver:
    ##ganti nama jadi solver
    def get_num_pixels(filepath):
        width, height = PIL.Image.open(filepath).size
        return width * height

    def Skripsi (PosterInput,ScoreSebelum):
        t0 = time.time()

        #######################################################################################################
        ### Meanshif the image using OpenCV to reduce colors                                                ###
        #######################################################################################################

        # PosterInput = cv2.imread(Poster)

        Shape = PosterInput.shape

        flatImg=np.reshape(PosterInput, [-1, 3])

        bandwidth = estimate_bandwidth(flatImg, quantile=0.2, n_samples=100)
        ms = MeanShift(bandwidth = bandwidth, bin_seeding=True)

        ms.fit(flatImg)

        labels=ms.labels_

        cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(labels)
        n_clusters_ = len(labels_unique)

        segmentedImg = cluster_centers[np.reshape(labels, Shape[:2])]

        cv2.imwrite("hasilmean.jpg", segmentedImg.astype(np.uint8))

        image = PIL.Image.open("hasilmean.jpg")
        color_count = {}
        width, height = image.size
        rgb_image = image.convert('RGB')

        imgtemp = cv2.imread("hasilmean.jpg")

        rows, cols, depth = imgtemp.shape

        # buat R,G,B sama posisi X dan Y
        temps = np.zeros((rows * cols, 5))

        k = 0
        # masukin warna prtama R kedua G ketiga B keempat posisi X kelima posisi Y
        for p in range(0, rows):
            for f in range(0, cols):
                temps[k][0] = imgtemp[p][f][0]
                temps[k][1] = imgtemp[p][f][1]
                temps[k][2] = imgtemp[p][f][2]
                temps[k][3] = p
                temps[k][4] = f

                k = k + 1

        for x in range(width):
            for y in range(height):
                rgb = rgb_image.getpixel((x, y))

                if rgb in color_count:
                    color_count[rgb] += 1
                else:
                    color_count[rgb] = 1





        jumlahpixel = Solver.get_num_pixels("hasilmean.jpg")



        # *************************************
        # ******** MAIN ALGORITHM CODE ********
        # *************************************


        maximum_generation = 1
        s,b,dom,domsmall = ColorHarmony.region(color_count,jumlahpixel)


        scoreawal = ColorHarmony.calculate_fitness(b, s)/2

        #GENERATE BIG COLOR
        for generation in range(maximum_generation):
            new_population = []
            new_populationsmall=[]
            # new_populationsmall.append(rgb2lab(domsmall))
            new_population.append(ColorHarmony.rgb2lab(dom))
            i=0
            x=0
            temp = False
            while i < 4:
               color = GA.select_initial_population(dom)
               new_population.append(color)
               i+=1

            pop=GA.bigGA(new_population,0.5,dom)
            while x<5:
                color = GA.select_initial_population(domsmall)
                new_populationsmall.append(color)
                x += 1

            poop=GA.smallGA(new_populationsmall,1,domsmall)
            FitnessScore= ColorHarmony.calculate_fitness(pop,poop)
            ct = 0
            while FitnessScore <1.5 and FitnessScore > ScoreSebelum or ct>10:
                poop = GA.smallGA(new_populationsmall,0.5,domsmall)
                FitnessScore=ColorHarmony.calculate_fitness(pop,poop)
                ct+=1
        w=0
        rgb=[]
        rgbBig=[]
        v=0
        while w < 5:
            color = (lab2rgb(poop[w],illuminant='D65', observer='2')* 254).astype(numpy.uint8)
            rgb.append(color)
            w+=1

        while v < 5:
            colorbig = (lab2rgb(pop[v],illuminant='D65', observer='2')* 254).astype(numpy.uint8)
            rgbBig.append(colorbig)
            v+=1


        im = PIL.Image.new('RGB', (300, 450), (255, 255, 255))
        draw = ImageDraw.Draw(im)
        s = 0

        while s < 5:
         draw.text((100, 10), "Your Primary Color", fill=(0, 0, 0))
         if (len(pop) > 0):
            draw.rectangle((120, 50, 180, 120), fill=(tuple(dom)))
         else:
            draw.rectangle((120, 50, 180, 120), fill=(tuple(domsmall)))
         draw.text((100, 130), "Primary Selection", fill=(0, 0, 0))
         draw.rectangle((s * 60, 150, 60 + (s * 60), 280), fill=(tuple(rgbBig[s])))
         temp = ColorHarmony.rgb2hex(rgbBig[s][0],rgbBig[s][1],rgbBig[s][2])
         draw.text((s*60+10, 260), temp, fill=(0, 0, 0))
         draw.text((100, 300), "Secondary Selection", fill=(0, 0, 0))
         draw.rectangle((s * 60, 320, 60 + (s * 60), 450), fill=(tuple(rgb[s])))
         temps = ColorHarmony.rgb2hex(rgb[s][0], rgb[s][1], rgb[s][2])
         draw.text((s * 60+10, 430), temps, fill=(0, 0, 0))
         s+=1
        timestamp = datetime.timestamp(datetime.now())
        filename = 'web'+str(timestamp)+'.png'
        im.save('static/web'+str(timestamp)+'.png')
        print('Selesai')
        t1 = time.time()

        total = t1 - t0
        return filename,FitnessScore,total,scoreawal



