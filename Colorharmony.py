import itertools
import numpy as np
import math




class ColorHarmony:
    #########################################################################################
    ### karena rgbtolab tidak berfungsi menggunakan fungsi manual                         ###
    ### https://stackoverflow.com/questions/13405956/convert-an-image-rgb-lab-with-python ###
    #########################################################################################
    def rgb2lab(inputcolor):
        num = 0
        RGB = [0, 0, 0]

        for value in inputcolor:
            value = float(value) / 255

            if value > 0.04045:
                value = ((value + 0.055) / 1.055) ** 2.4
            else:
                value = value / 12.92

            RGB[num] = value * 100
            num = num + 1

        XYZ = [0, 0, 0, ]

        X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
        Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
        Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
        XYZ[0] = round(X, 4)
        XYZ[1] = round(Y, 4)
        XYZ[2] = round(Z, 4)

        XYZ[0] = float(XYZ[0]) / 95.047  # ref_X =  95.047   Observer= 2°, Illuminant= D65
        XYZ[1] = float(XYZ[1]) / 100.0  # ref_Y = 100.000
        XYZ[2] = float(XYZ[2]) / 108.883  # ref_Z = 108.883

        num = 0
        for value in XYZ:

            if value > 0.008856:
                value = value ** (0.3333333333333333)
            else:
                value = (7.787 * value) + (16 / 116)

            XYZ[num] = value
            num = num + 1

        Lab = [0, 0, 0]

        L = (116 * XYZ[1]) - 16
        a = 500 * (XYZ[0] - XYZ[1])
        b = 200 * (XYZ[1] - XYZ[2])

        Lab[0] = round(L, 4)
        Lab[1] = round(a, 4)
        Lab[2] = round(b, 4)

        return Lab

    ######################################################
    ### Divide into 2 Region according to pixel count  ###
    ######################################################
    def rgb2hex(r, g, b):
        return "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

    def region(color_count,jumlahpixel):
        isismall = []
        isibig = []
        ct2 = 0
        ct=0
        dominantcolor = ""
        dominantcolorsmall=""

        for color, count in color_count.items():
            if (count > 0.025 * jumlahpixel):
                if (ct2 < count):
                    ct2 = count
                    dominantcolor = color

                isibig.append(ColorHarmony.rgb2lab(color))

            if (count > 0.0025 * jumlahpixel and count < 0.025 * jumlahpixel):
                if (ct < count):
                    ct = count
                    dominantcolorsmall = color
                if color not in isismall:
                 isismall.append(ColorHarmony.rgb2lab(color))


        return isismall, isibig, dominantcolor,dominantcolorsmall

    #################################################################################
    ### merubah LAB menjadi LCH                                                   ###
    ### Already change according to the problem                                   ###
    ### https://www.konicaminolta.com/instruments/knowledge/color/part4/05.html   ###
    #################################################################################

    def HC(inputColor1, inputColor2):
        if (inputColor1[2] == 0 and inputColor1[1] == 0 or inputColor2[2] == 0 and inputColor2[1] == 0):
            CB1 = 0
            CB2 = 0
        else:
            CB1 = math.sqrt((inputColor1[1]) ** 2 + (inputColor1[2] ** 2))
            CB2 = math.sqrt((inputColor2[1]) ** 2 + (inputColor2[2] ** 2))
        DeltaH = math.sqrt(
            (inputColor1[1] - inputColor2[1]) ** 2 + (inputColor1[2] - inputColor2[2]) ** 2 - (CB2 - CB1) ** 2)

        DeltaCAB = CB2 - CB1

        DeltaC = ((DeltaH ** 2) + (DeltaCAB / 1.46) ** 2) ** 0.5

        Hc = 0.04 + 0.53 * math.tanh(0.8 - 0.045 * DeltaC)
        return Hc

    def Hl(inputColor1, inputColor2):
        Lsum = inputColor2[0] + inputColor1[0]
        Hlsum = 0.28 + 0.54 * math.tanh(-3.88 + 0.029 * Lsum)
        DeltaL = abs(inputColor1[0] - inputColor2[0])
        HDeltaL = 0.14 + 0.15 * math.tanh(-2 + 0.2 * DeltaL)
        Hl = Hlsum + HDeltaL
        return Hl

    def Hh(inputColor1, inputColor2):
        if (inputColor1[2] == 0 and inputColor1[1] == 0 or inputColor2[2] == 0 and inputColor2[1] == 0 or inputColor1[1] or inputColor2[1]):
            h1 = 0
            h2 = 0
        else:
            h1 = math.degrees(math.atan(inputColor1[2] / inputColor1[1]))
            h2 = math.degrees(math.atan(inputColor2[2] / inputColor2[1]))
        Hs1 = -0.08 - 0.14 * math.sin(math.degrees(h1 + math.degrees(0.87267))) - 0.07 * math.sin(
            math.degrees(2 * h1 + math.degrees(math.pi / 2)))
        Hs2 = -0.08 - 0.14 * math.sin(math.degrees(h2 + math.degrees(0.87267))) - 0.07 * math.sin(
            math.degrees(2 * h2 + math.degrees(math.pi / 2)))
        Ey1 = ((0.22 * inputColor1[0] - 12.8) / 10) * math.exp(
            (math.degrees((math.pi / 2) - h1)) / 10 - math.exp((math.degrees((math.pi / 2) - h1)) / 10))
        Ey2 = ((0.22 * inputColor2[0] - 12.8) / 10) * math.exp(
            (math.degrees((math.pi / 2) - h2)) / 10 - math.exp((math.degrees((math.pi / 2) - h2)) / 10))
        CB1 = math.sqrt((inputColor1[1]) ** 2 + (inputColor1[2] ** 2))
        CB2 = math.sqrt((inputColor2[1]) ** 2 + (inputColor2[2] ** 2))
        Ec1 = 0.5 + 0.5 * math.tanh(-2 + 0.5 * CB1)
        Ec2 = 0.5 + 0.5 * math.tanh(-2 + 0.5 * CB2)
        HSY1 = Ec1 * (Hs1 + Ey1)
        HSY2 = Ec2 * (Hs2 + Ey2)
        HH = HSY2 + HSY1
        return HH

    def L(besar):
        sorted(besar)
        hasil =0
        if(len(besar)<=0):
            hasil = 0
        else:
          hasil =besar[0]
        return hasil





    def S(kecil):
        sorted(kecil)
        return kecil[0]


    def var(kecil):
        np.var(kecil)
        return np.var(kecil)


    def SH(L, S, var):
        sh = 1.6857 + 0.1822 * L + 1.1403 * S - 3.1432 * var
        return sh



    ##########################################
    ### Calculate Global Harmony Scoree    ###
    ##########################################
    def calculate_fitness(populationbig, populationsmall):
        colorharmonismall = []
        colorharmonibig = []


        for a, b in itertools.combinations(populationsmall, 2):
            hc = ColorHarmony.HC(a, b)
            hl = ColorHarmony.Hl(a, b)
            hh = ColorHarmony.Hh(a, b)
            total = hc + hl + hh
            colorharmonismall.append(total)


        for x, y in itertools.combinations(populationbig, 2):
            hc = ColorHarmony.HC(x, y)
            hl = ColorHarmony.Hl(x, y)
            hh = ColorHarmony.Hh(x, y)
            total = hc + hl + hh
            colorharmonibig.append(total)



        score = ColorHarmony.SH(ColorHarmony.L(colorharmonibig), ColorHarmony.S(colorharmonismall), ColorHarmony.var(colorharmonismall))
        return score


    def color_harmony_2_colors_cromosom(cromosomawal,iterasi):
        hasil = []
        all = []
        x = 0
        y= iterasi
        while x < iterasi:
          while y < 5:
            hc = ColorHarmony.HC(cromosomawal[x], cromosomawal[y])
            hl = ColorHarmony.Hl(cromosomawal[x], cromosomawal[y])
            hh = ColorHarmony.Hh(cromosomawal[x], cromosomawal[y])
            total = hc + hl + hh
            hasil.append(total)
            y += 1
          all.append(hasil)
          x+=1
          y = iterasi
          hasil=[]
        temp=[0,0,0,0]

        o=0
        p=0
        while o < iterasi:
           while p < 5 - iterasi:
               temp[p] += all[o][p]
               p+= 1
           p=0
           o+=1

        return temp

    def color_harmony_2_color(cromosomawal):
        hasil =[]
        i=1
        while i < len(cromosomawal):
            hc = ColorHarmony.HC(cromosomawal[0], cromosomawal[i])
            hl = ColorHarmony.Hl(cromosomawal[0], cromosomawal[i])
            hh = ColorHarmony.Hh(cromosomawal[0], cromosomawal[i])
            total = hc + hl + hh
            hasil.append(total)
            i+=1

        return hasil

    def scoretotal(population):
        totals =[]
        for a, b in itertools.combinations(population, 2):
            hc = ColorHarmony.HC(a, b)
            hl = ColorHarmony.Hl(a, b)
            hh = ColorHarmony.Hh(a, b)
            total = hc + hl + hh
            totals.append(total)
        return sum(totals)/5








