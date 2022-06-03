import random
import csv

def create_dna(lenght):

    """Burada kullanıcının girdigi uzunlukta dna oluşturup bir string dizisine atıyorum."""

    nuc = ["A", "C", "G", "T"]
    dna = ""
    for i in range(lenght):
        dna = dna + nuc[random.randint(0, 3)]
    return dna

def contol_dna(dna):

    """Kullanıcının girdigi dna'da yanlış bir durum var mı onu kontrol ediyorum."""

    hata = 0
    hata_indisleri = ["Hatalı İndisler : "]
    for i in dna:
        if i == 'A' or i == 'C' or i == 'G' or i == 'T':
            hata = hata + 0
        else:
            hata_indisleri.append(i)
            hata = hata + 1
    if hata == 0:
        print("DNA dizilimi hatasızdır.")
        return 0
    else:
        print("DNA dizilimi HATALIDIR !")
        print(hata_indisleri)
        return 404

def create_csv(isim, arr):
    """Burada dosya ismine gore olusturdugum dna dizilerini dosyalama yaptigim yer dosyalama icin csv kutuphanesini kullandim."""
    dosya_adi = str(isim + ".csv")
    csv_dosya = open(dosya_adi, "w", newline='')  # Yazma odaklı csv dosyası olusturuyoruz.
    yazici = csv.writer(csv_dosya,
                        delimiter=',')  # Yazıcı olusturuyoruz virguller ile ayırıp satır satır assagıya inecek
    yazici.writerow(arr)  # yaz emri veriyoruz
    csv_dosya.close()  # dosyayı kapatıyoruz.
    print("DNA kaydedildi")
    return dosya_adi

def atama_dna(lenght):
    """Kullanıcı icin DNA giris arayuzu olusturdum."""
    sec = input("DNA Random Oluşturulsun mu ?    (Y/N)  : ")
    if str(sec) == "Y" or str(sec) == "y":
        try:
            dna_1 = create_dna(lenght)
            create_csv("dna_1", dna_1)  # Olusturdugum dna yı dosyalama fonksiyonuna gonderiyorum.
            print("DNA başarı ile oluşturulup kaydedilmiştir.")
            return dna_1
        except:
            print("DNA oluşturulamadı veya kaydedilemedi tekrar deneyiniz.")
            return atama_dna(lenght)
    elif str(sec) == "N" or str(sec) == "n":
        try:
            dna2_temp = ""
            dna_2 = input("DNA dizilimini giriniz : ")
            dna2_temp = dna2_temp + dna_2
            if contol_dna(dna2_temp) == 0:
                create_csv("dna_2", dna2_temp)  # Kullanicinin girdigi dna yi dosyalama fonksiyonuna gonderiyorum.
                print("DNA başarı ile kaydedilmiştir.")
                return dna2_temp
            else:
                print("Hatalı DNA dizilimi girdiniz lütfen dizilimi kontrol ediniz.")
                return atama_dna(lenght)
        except:
            print("DNA oluşturulamadı veya kaydedilemedi tekrar deneyiniz.")
            return atama_dna(lenght)
    else:
        print("Yanlış giriş yaptınız lütfen tekrar deneyiniz .")
        return atama_dna(lenght)


def dna_sekansla(dna1, lenght, piece):
    """Dna'yı alıp kullanıcının girdigi uzunluk ve sayıda rastgele yerlerden parcalar alıyorum ve sekanslar
    isimli matrise tum sekansları ardarda yerlestiriyorum."""
    dna = ""
    dna = dna + dna1
    sinir = int(len(dna)) - lenght
    temp_sekans = ""
    for i in range(piece + 1):
        selector = random.randint(0, sinir)
        for k in range(selector, selector + lenght):
            temp_sekans = temp_sekans + str(dna[k])
    return temp_sekans

def reverse_complements(sekanslar, sekans_lenght):
    """Sekanslardan sekans boyu kadar parçalar alıp bunları tumleyenini alıp ters cevirip tum reverse complementlerin
     tutuldugu string dizisine ard arda yerleştiriyorum."""
    complements = ""
    for i in range(0, len(sekanslar), sekans_lenght):
        temp = ""
        for k in range(i, i + sekans_lenght):
            if sekanslar[k] == 'A':
                temp = temp + 'T'
            elif sekanslar[k] == 'C':
                temp = temp + 'G'
            elif sekanslar[k] == 'G':
                temp = temp + 'C'
            elif sekanslar[k] == 'T':
                temp = temp + 'A'
        complements = complements + temp[::-1]
    return complements

def print_sek_and_comp(sekans, complement, lenght):
    """Sekansları ve reverse complementleri ekrana yazdırıyorum"""
    print("***SEKANSLAR***--------***REV.COMP.***")
    print("")
    for i in range(0, len(sekans), lenght):
        temp1 = " "
        temp2 = " "
        for k in range(i, i + lenght):
            temp1 = temp1 + sekans[k]
            temp2 = temp2 + complement[k]
        temp1 = temp1 + " "
        temp2 = temp2 + " "
        print("  "+temp1+"           "+temp2)
    print("")
    print("--------------------------------------------")

def sek_and_revcomp_local_alignment(sekans, complements, sek_lenght, sek_piece, indell_point, match_point, missmatch_point):
    w, h = sek_piece, sek_piece
    score = [[0 for x in range(w)] for y in range(h)] #Buyuk skor matrisini daha sonra kullanmak uzere olusturup icini 0'larla dolduruyorum

    for i in range(0, (sek_piece * sek_lenght) - sek_lenght, sek_lenght):
        sek_part = sekans[i:i + sek_lenght] #Tum sekansların bulundugu string dizisinden sırayla bir parca sekans cekiyorum.
        for k in range(0, (sek_piece * sek_lenght) - sek_lenght, sek_lenght):
            complements_part = complements[k:k + sek_lenght] #Tum rev.complementlerin bulundugu string dizisinden sırayla bir parca rev.complement cekiyorum.
            w, h = sek_lenght+1, sek_lenght+1
            compare = [[0 for x in range(w)] for y in range(h)] #Burada local alignment yapılacak sekans ve complementin karsilastiralacagi arrayi daha sonra kullanmak uzere dolduruyorum.
            bigger = 0  # Alignment sırasında elde edilen en buyuk skoru tuttugum daha buyuk bir skor gelirse degisen birdegisken tanımladım.
            for p in range(1, sek_lenght + 1):
                for j in range(1, sek_lenght + 1):
                    left_to_right = compare[p][j - 1] + indell_point    # Burada Alignment yaparken soldan saga ilerledigimizde elde edicegimiz puanı bir degiskene atıyorum
                    up_to_down = compare[p - 1][j - 1] + indell_point   # Burada Alignment yaparken yukarıdan assagiya ilerledigimizde elde edicegimiz puanı bir degiskene atıyorum
                    if sek_part[j - 1] == complements_part[p - 1]:
                        cross = compare[p - 1][j - 1] + match_point     # Burada Alignment yaparken capraz ilerledigimizde ve eslesme durumunda elde edicegimiz puanı bir degiskene atıyorum
                    else:
                        cross = compare[p - 1][j - 1] + missmatch_point # Burada Alignment yaparken capraz ilerledigimizde ve eslesmeme durumunda elde edicegimiz puanı bir degiskene atıyorum
                    compare[p][j] = max(left_to_right, up_to_down, cross, 0)    # Her yonden geldigimizde elde ettigimiz puanların en yuksek degerini alıp o indise yerlestiriyorum ve negatife dusmemesi icin minimum degeri 0a esitliyorum.

                    if compare[p][j] >= bigger:
                        bigger = compare[p][j]  # Elde ettigimiz deger daha onceki degerlerden buyukse en buyuk puanı biggera atıyorum.
                """for l in range(0, sek_lenght+1):
                    print(compare[l])
                print('/n')"""

            y_stepper = int(i / sek_lenght)     # Buyuk skor matrisinin indislerini ayarlıyorum.
            x_stepper = int(k / sek_lenght)     # Buyuk skor matrisinin indislerini ayarlıyorum.
            score[y_stepper][x_stepper] = bigger    #Buyuk skor matrisinde bu alignmentde elde ettigimiz en buyuk degeri aktarıyorum.
    print("----- SEKANSLAR VE REV.COMPLAMENTLERİN KARŞILAŞTIRILMASI TAMAMLANDI -----")

    return score

def sek_local_alignment(sekans, sek_lenght, sek_piece, indell_point, match_point, missmatch_point):

    """Ustteki fonksiyonlar tek farkı burada buyuk skor matrisinin altını doldurucagımız sekanslar ve reverse complamentlerin skorlarını alıyorum."""

    w, h = sek_piece, sek_piece
    score = [[0 for x in range(w)] for y in range(h)]

    for i in range(0, (sek_piece * sek_lenght) - sek_lenght, sek_lenght):
        sek_part1 = sekans[i:i + sek_lenght]
        for k in range(0, (sek_piece * sek_lenght) - sek_lenght, sek_lenght):
            sek_part2 = sekans[k:k + sek_lenght]
            w, h = sek_lenght+1, sek_lenght+1
            compare = [[0 for x in range(w)] for y in range(h)]
            bigger= 0

            for p in range(1, sek_lenght+1):
                for j in range(1, sek_lenght+1):
                    left_to_right = compare[p][j - 1] + indell_point
                    up_to_down = compare[p-1][j - 1] + indell_point
                    if sek_part1[j - 1] == sek_part2[p - 1] :
                        cross = compare[p - 1][j - 1] + match_point
                    else :
                        cross = compare[p - 1][j - 1] + missmatch_point
                    compare[p][j] = max(left_to_right, up_to_down, cross, 0)

                    if compare[p][j] >= bigger:
                        bigger = compare[p][j]
                """for l in range(0, sek_lenght+1):
                    print(compare[l])
                print('/n')"""

            y_stepper = int(i / sek_lenght)
            x_stepper = int(k / sek_lenght)
            score[y_stepper][x_stepper] = bigger

    print("----- SEKANS VE SEKANS KARŞILAŞTIRILMASI TAMAMLANDI -----")

    return score

def score_printer(score, lenght, min_s):

    """Elde ettigimiz skor matrislerini ekrana yazdirdigimiz fonksiyon."""

    temp_score = [[], []]
    temp_score = score
    for i in range(0, lenght-1):
        for k in range(0, lenght-1):
            if i==k:
                print("*", end=" ")
            else:
                if temp_score[i][k] >= min_s:
                    print(str(temp_score[i][k]), end=" ")
                else :
                    print("  ", end=" ")
        print("")

def overlap_matrix_for_sequence_assembly(sas_score, sarc_score, lenght, min_s):

    """Bu fonksiyonda sekanslar ve sekansların skorlarını alıp Buyuk Skor Matrisindeki Ust ucgene yerlesrip
    alt ucgenede sekanslar ve reverse complementlerin skorlarını yerlestiriyorum."""

    w, h = lenght, lenght
    overlap_matrix = [[0 for x in range(w)] for y in range(h)]

    for i in range(0, lenght):
        for k in range(1+i, lenght):
            overlap_matrix[i][k] = sas_score[i][k]

    print("----------------- SAS SCORE MATRIX --------------------")
    score_printer(sas_score, lenght, 0)

    print("----------------- SARC SCORE MATRIX -------------------")
    score_printer(sarc_score, lenght, 0)

    for i in range(0, lenght):
        for k in range(0, i):
            overlap_matrix[i][k] = sarc_score[i][k]
    print("--------------- OVERLAP SCORE MATRIX ------------------")
    score_printer(overlap_matrix, lenght, min_s)

    return overlap_matrix

def create_score_csv(score_matrix,name):
    """Burada dosya ismine gore olusturdugum skor matrislerini dosyalama yaptigim yer dosyalama icin csv kutuphanesini kullandim."""
    dosya_adi = str(name + ".csv")
    csv_dosya = open(dosya_adi, "w", newline='')
    yazici = csv.writer(csv_dosya, delimiter=',')
    for score_data in score_matrix:
        yazici.writerow(score_data)
    csv_dosya.close()
    return dosya_adi

def mainfonc():

    """Artik olusturdugum tum fonksiyonlari kullanıp olayi bitiriyorum."""

    lenght = int(input("DNA'nın Uzunluğunu Giriniz : "))
    a_dna = atama_dna(lenght)
    sek_lenght = int(input("Sekans Uzunluğunu Giriniz (L): "))
    sek_piece = int(input("Kaç adet sekans istiyorsunuz (N): "))
    sek_dna = dna_sekansla(a_dna, sek_lenght, sek_piece)
    rev_comp = reverse_complements(sek_dna, sek_lenght)
    print_sek_and_comp(sek_dna, rev_comp, sek_lenght)
    match_point = int(input("Match puanını giriniz : "))
    missmatch_point = int(input("Miss match puanını giriniz : "))
    indell_point = int(input("Indell puanını giriniz : "))
    min_score = int(input("Tablo da gösterilecek en küçük skor (T) : "))

    sas_score = sek_local_alignment(sek_dna, sek_lenght, sek_piece, indell_point, match_point, missmatch_point)
    create_score_csv(sas_score, "sas_score")
    sarc_score = sek_and_revcomp_local_alignment(sek_dna, rev_comp, sek_lenght, sek_piece, indell_point, match_point, missmatch_point)
    create_score_csv(sarc_score, "sarc_score")
    sonuc_matrix = overlap_matrix_for_sequence_assembly(sas_score, sarc_score, sek_piece, min_score)
    create_score_csv(sonuc_matrix, "sonuc_matrix")

mainfonc()  # VE ARTIK MUTLU SON OLUSTURDUGUM TUM METODLARI CALISTIRIP SONUCLARI GORUYORUZ.
