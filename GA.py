import math
import random
from Colorharmony import ColorHarmony


class GA():


    def select_initial_population(child):
        child = ColorHarmony.rgb2lab(child)
        ##hue value for children
        HueValue = math.sqrt((child[1]) ** 2 + (child[2] ** 2))
        tempL = random.uniform(0, 100)
        selisih = abs(child[0] - tempL)
        while (selisih < 50):
                tempL = random.uniform(0, 100)
                selisih =abs(child[0] - tempL)
        L = tempL
        ##for A
        tempA = random.uniform(-127, 128)
        ##for B
        tempB = random.uniform(-128, 127)

        HueTemp = math.sqrt((tempA) ** 2 + (tempB ** 2))

        while (abs(HueValue - HueTemp)> 10):
            a = child[1] - 20
            if (a < -127):
                a = -127
            b = child[1] + 20
            if (b > 128):
                b = 128
            c = child[2] - 20
            if (a < -128):
                a = -128
            d = child[2] + 20
            if (b > 127):
                b = 127
            tempA = random.uniform(a, b)
            ##for B
            tempB = random.uniform(c, d)
            HueTemp = math.sqrt((tempA) ** 2 + (tempB ** 2))
        A = tempA
        B = tempB
        x=[]
        x.append(L)
        x.append(A)
        x.append(B)
        return x


    def select_individual_by_tournament(array_of_score,population,iterasi):
        temp = float('-inf')
        i=0
        parent=[]
        while i < len(array_of_score):
            if (iterasi == 4):
                temp = array_of_score[i]
                parent = population[4]
                break
            if(temp<=array_of_score[i]) and array_of_score != 0:
                temp = array_of_score[i]
                if(i+iterasi>4):
                 parent = population[4]
                else:
                 parent = population[i+iterasi]
            i+=1

        return parent

    def breed_by_crossover(parent_1, parent_2):
        # Get length of chromosome
        chromosome_length = len(parent_1)

        # Pick crossover point, avoding ends of chromsome
        crossover_point = random.randint(1, chromosome_length - 1)

        # Create children. np.hstack joins two arrays
        child_1 = list(parent_1[0:crossover_point])+list(parent_2[crossover_point:chromosome_length])

        child_2 = list(parent_2[0:crossover_point])+list(parent_1[crossover_point:chromosome_length])

        # Return children
        return child_1, child_2
    ##GANTI NAMA REGION_1_GENETIK_PROSES
    def bigGA(initialpopulation,mutation_rate,dom):
        GenerasiiTigaR1 = []
        GenerasiEmpatR1 = []
        GenerasiLimaR1 = []
        scoreKeseluruhan = []
        temps=[]
        print("GEN SATU Populasi R1")
        print(initialpopulation)
        print("SCORE 1")
        print(ColorHarmony.scoretotal(initialpopulation))
        scoreKeseluruhan.append(ColorHarmony.scoretotal(initialpopulation))
        ##scre dari populasi awal
        p = ColorHarmony.color_harmony_2_color(initialpopulation)
        # pilih parent untuk score terbaik
        x = GA.select_individual_by_tournament(p, initialpopulation, 1)
        # masukin warna dominan kedalam populasi ( selalu dikunci)
        temps.append(ColorHarmony.rgb2lab(dom))
        # masukin warna terbaik diantara populasi initial
        temps.append(x)
        # buat 2 anak dari 2 parent
        index = random.randint(0, 4)
        child1, child2 = GA.breed_by_crossover(initialpopulation[index], x)
        # Mutate salah satu anak supaya ga terlalu mirip sama parent ( butuh variansi )
        cc = GA.randomly_mutate_population(child1,mutation_rate)
        # masukin child 1 yg udh di mutate
        temps.append(cc)
        # masukin child 2
        temps.append(child2)
        # buat 1 warna random karena tadi cmn 4 ( 2 parent 2 anak )
        y = GA.randomly_mutate_population(child2,mutation_rate)
        temps.append(y)
        # populasi generasi ke 2
        print("GEN DUA Populasi R1")
        print(temps)
        print("SCORE 2")
        print(ColorHarmony.scoretotal(temps))
        scoreKeseluruhan.append(ColorHarmony.scoretotal(temps))
        # warna dominan dan warna kedua di lock
        # cari warna ketiga dengan bandingin score warna 1 dan dua ke masing masing solusi (3 warna lainnya)
        Iterasi3 = ColorHarmony.color_harmony_2_colors_cromosom(temps, 2)
        # pilih warna ketiga yg paling baik
        rr = GA.select_individual_by_tournament(Iterasi3, temps, 2)
        # masukin warna pertama kedua ketiga
        GenerasiiTigaR1.append(ColorHarmony.rgb2lab(dom))
        GenerasiiTigaR1.append(temps[1])
        GenerasiiTigaR1.append(rr)
        index1 = random.randint(0, 4)
        child3, child4 = GA.breed_by_crossover(temps[index1], rr)

        cx = GA.randomly_mutate_population(child3,mutation_rate)
        child4 = GA.randomly_mutate_population(child4, mutation_rate)
        GenerasiiTigaR1.append(cx)
        GenerasiiTigaR1.append(child4)
        print("GEN TIGA Populasi R1")
        print(GenerasiiTigaR1)
        print("SCORE 3")
        print(ColorHarmony.scoretotal(GenerasiiTigaR1))
        scoreKeseluruhan.append(ColorHarmony.scoretotal(GenerasiiTigaR1))

        Iterasi4 = ColorHarmony.color_harmony_2_colors_cromosom(GenerasiiTigaR1, 3)
        rx = GA.select_individual_by_tournament(Iterasi4, GenerasiiTigaR1, 3)
        GenerasiEmpatR1.append(ColorHarmony.rgb2lab(dom))
        GenerasiEmpatR1.append(GenerasiiTigaR1[1])
        GenerasiEmpatR1.append(GenerasiiTigaR1[2])
        GenerasiEmpatR1.append(rx)
        index2 = random.randint(0, 4)
        child5, child6 = GA.breed_by_crossover(GenerasiiTigaR1[index2], rx)

        xx = GA.randomly_mutate_population(child5,mutation_rate)

        GenerasiEmpatR1.append(xx)
        print("GEN EMPAT Populasi R1")
        print(GenerasiEmpatR1)
        print("SCORE 4")
        print(ColorHarmony.scoretotal(GenerasiEmpatR1))
        scoreKeseluruhan.append(ColorHarmony.scoretotal(GenerasiEmpatR1))

        Iterasi4a = ColorHarmony.color_harmony_2_colors_cromosom(GenerasiEmpatR1, 4)
        rxx = GA.select_individual_by_tournament(Iterasi4a, GenerasiEmpatR1, 4)
        rxx = GA.randomly_mutate_population(rxx, mutation_rate)

        GenerasiLimaR1.append(ColorHarmony.rgb2lab(dom))
        GenerasiLimaR1.append(GenerasiEmpatR1[1])
        GenerasiLimaR1.append(GenerasiEmpatR1[2])
        GenerasiLimaR1.append(GenerasiEmpatR1[3])
        GenerasiLimaR1.append(rxx)
        print("GEN LIMA Populasi R1")
        print(GenerasiLimaR1)
        print(ColorHarmony.scoretotal(GenerasiLimaR1))
        scoreKeseluruhan.append(ColorHarmony.scoretotal(GenerasiLimaR1))
        sementara= scoreKeseluruhan.index(max(scoreKeseluruhan))

        if(sementara==0):
            return initialpopulation
        elif(sementara==1):
            return temps
        elif (sementara==2):
            return GenerasiiTigaR1
        elif (sementara==3):
            return GenerasiEmpatR1
        elif (sementara==4):
            return GenerasiLimaR1


    def smallGA(initialpopulation,mutation_rate,domsmall):
        GenerasiiTigaR2 = []
        GenerasiEmpatR2 = []
        GenerasiLimaR2 = []
        TempSmallColor=[]
        ScoreKeseluruhanR2=[]
        print("GEN SATU Populasi R2")
        print(initialpopulation)
        print("SCORE 1")
        print(ColorHarmony.scoretotal(initialpopulation))
        ScoreKeseluruhanR2.append(ColorHarmony.scoretotal(initialpopulation))
        ##scre dari populasi awal
        psmall = ColorHarmony.color_harmony_2_color(initialpopulation)
        # pilih parent untuk score terbaik
        xsmall = GA.select_individual_by_tournament(psmall, initialpopulation, 1)
        # masukin warna dominan kedalam populasi ( selalu dikunci)
        TempSmallColor.append(ColorHarmony.rgb2lab(domsmall))
        # masukin warna terbaik diantara populasi initial
        TempSmallColor.append(xsmall)
        # buat 2 anak dari 2 parent
        index = random.randint(0, 4)
        child1small, child2small = GA.breed_by_crossover(initialpopulation[index], xsmall)
        # Mutate salah satu anak supaya ga terlalu mirip sama parent ( butuh variansi )
        ccsmall = GA.randomly_mutate_population(child1small,mutation_rate)
        child2small = GA.randomly_mutate_population(child2small,mutation_rate)
        # masukin child 1 yg udh di mutate
        TempSmallColor.append(ccsmall)
        # masukin child 2
        TempSmallColor.append(child2small)
        # buat 1 warna random karena tadi cmn 4 ( 2 parent 2 anak )
        ysmall = GA.select_initial_population(domsmall)
        TempSmallColor.append(ysmall)
        # populasi generasi ke 2
        print("GEN DUA Populasi R2")
        print(TempSmallColor)
        print("SCORE 2")
        print(ColorHarmony.scoretotal(TempSmallColor))
        ScoreKeseluruhanR2.append(ColorHarmony.scoretotal(TempSmallColor))
        # warna dominan dan warna kedua di lock
        # cari warna ketiga dengan bandingin score warna 1 dan dua ke masing masing solusi (3 warna lainnya)
        Iterasi3small = ColorHarmony.color_harmony_2_colors_cromosom(TempSmallColor, 2)
        # pilih warna ketiga yg paling baik
        rrsmall = GA.select_individual_by_tournament(Iterasi3small, TempSmallColor, 2)
        # masukin warna pertama kedua ketiga
        GenerasiiTigaR2.append(ColorHarmony.rgb2lab(domsmall))
        GenerasiiTigaR2.append(TempSmallColor[1])
        GenerasiiTigaR2.append(rrsmall)
        index1 = random.randint(0, 4)
        child3small, child4small = GA.breed_by_crossover(TempSmallColor[index1], rrsmall)
        cxsmall = GA.randomly_mutate_population(child3small,mutation_rate)
        child4small = GA.randomly_mutate_population(child4small,mutation_rate)
        GenerasiiTigaR2.append(cxsmall)
        GenerasiiTigaR2.append(child4small)
        print("GEN TIGA Populasi R2")
        print(GenerasiiTigaR2)
        print("SCORE 3")
        print(ColorHarmony.scoretotal(GenerasiiTigaR2))
        ScoreKeseluruhanR2.append(ColorHarmony.scoretotal(GenerasiiTigaR2))

        Iterasi4small = ColorHarmony.color_harmony_2_colors_cromosom(GenerasiiTigaR2, 3)
        rxsmall = GA.select_individual_by_tournament(Iterasi4small, GenerasiiTigaR2, 3)
        GenerasiEmpatR2.append(ColorHarmony.rgb2lab(domsmall))
        GenerasiEmpatR2.append(GenerasiiTigaR2[1])
        GenerasiEmpatR2.append(GenerasiiTigaR2[2])
        GenerasiEmpatR2.append(rxsmall)
        index2 = random.randint(0, 4)
        child5small, child6small = GA.breed_by_crossover(GenerasiiTigaR2[index2], rxsmall)
        xxsmall = GA.randomly_mutate_population(child5small,mutation_rate)
        GenerasiEmpatR2.append(xxsmall)
        print("GEN EMPAT Populasi R2")
        print(GenerasiEmpatR2)
        print("SCORE 4")
        print(ColorHarmony.scoretotal(GenerasiEmpatR2))
        ScoreKeseluruhanR2.append(ColorHarmony.scoretotal(GenerasiEmpatR2))

        Iterasi4asmall = ColorHarmony.color_harmony_2_colors_cromosom(GenerasiEmpatR2, 4)
        rxxsmall = GA.select_individual_by_tournament(Iterasi4asmall, GenerasiEmpatR2, 4)
        GenerasiLimaR2.append(ColorHarmony.rgb2lab(domsmall))
        GenerasiLimaR2.append(GenerasiEmpatR2[1])
        GenerasiLimaR2.append(GenerasiEmpatR2[2])
        GenerasiLimaR2.append(GenerasiEmpatR2[3])
        GenerasiLimaR2.append(rxxsmall)
        print("GEN LIMA Populasi R2")
        print(GenerasiLimaR2)
        print(ColorHarmony.scoretotal(GenerasiLimaR2))
        ScoreKeseluruhanR2.append(ColorHarmony.scoretotal(GenerasiLimaR2))
        sementaraR2 = ScoreKeseluruhanR2.index(max(ScoreKeseluruhanR2))
        if (sementaraR2 == 0):
            return initialpopulation
        elif (sementaraR2 == 1):
            return TempSmallColor
        elif (sementaraR2 == 2):
            return GenerasiiTigaR2
        elif (sementaraR2 == 3):
            return GenerasiEmpatR2
        elif (sementaraR2 == 4):
            return GenerasiLimaR2

    def randomly_mutate_population(child,mutation_rate):
        banyak_gen = int(len(child) * mutation_rate)
        i=0
        while i < banyak_gen:
            ##hue value for children
            HueValue = math.sqrt((child[1]) ** 2 + (child[2] ** 2))
            tempL = random.uniform(0, 100)
            selisih = abs(child[0] - tempL)
            while (selisih < 50):
                tempL = random.uniform(0, 100)
                selisih = abs(child[0] - tempL)

            L = tempL
            ##for A
            tempA = random.uniform(-127, 128)
            ##for B
            tempB = random.uniform(-128, 127)

            HueTemp = math.sqrt((tempA) ** 2 + (tempB ** 2))

            while (abs(HueValue - HueTemp) > 6):

                a = child[1] - 20
                if (a < -127):
                    a = -127
                b = child[1] + 20
                if (b > 128):
                    b = 128
                c = child[2] - 20
                if (a < -128):
                    a = -128
                d = child[2] + 20
                if (b > 127):
                    b = 127
                tempA = random.uniform(a, b)
                ##for B
                tempB = random.uniform(c, d)
                HueTemp = math.sqrt((tempA) ** 2 + (tempB ** 2))
                i+=1

            A = tempA
            B = tempB
            x = []
            x.append(L)
            x.append(A)
            x.append(B)
        return x





