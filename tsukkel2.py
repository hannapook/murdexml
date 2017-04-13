import xml.etree.ElementTree as ET
snr=ET.Element("sr")


f = open('08.xml.eelex.txt', 'r', encoding='utf8')
a=f.readlines()
b=[i.strip() for i in a]

def xmliks(snr, rida):
    ms_rida=b[rida+1]
    if ms_rida.startswith('<w:rStyle w:val="ms1"'):
        i1=ms_rida.find('<w:t>')
        i2=ms_rida.find('</w:t>')
        marksona_ise=ms_rida[i1+5:i2]
        if not marksona_ise[0].isdigit():
            artikkel = ET.SubElement(snr, "x:A")
            pais = ET.SubElement(artikkel, "x:P")
            ms_grupp = ET.SubElement(pais, "x:mg")
            marksona = ET.SubElement(ms_grupp, "x:m")
            marksona.text=marksona_ise
    #if 'Vrd' in ms_rida:
      #kustuta sellele eelnev tühi rida ära

#tahaks siin teha tsükli, et ei peaks iga kord uut rida uuesti defineerima

#liitsõna-märksõnade lisamine (kui ühes artiklis on mitu liitsõna, siis hetkel lisab ainult esimese)
        rida2=b[rida+2]
        i1=rida2.find('<w:t>')
        i2=rida2.find('</w:t>')
        teine_rida=rida2[i1+5:i2]
        if teine_rida.startswith('|'):
            marksona.text=marksona_ise+teine_rida

#märksõnaviite xmli paigutamine
#töötab hetkel ainult siis, kui märksõna pole liitsõna
        if '→' in rida2: 
            i1=rida2.find('→</w:t><w:t>')
            msv=rida2[i1+12:]
            i2=msv.find('</w:t>')
            ms_viide=msv[:i2]
            mvtg = ET.SubElement(pais, "x:mvtg")
            mvt = ET.SubElement(mvtg, "x:mvt")
            mvt.text=ms_viide

#atribuutide lisamine märksõna elemendile
        if rida2.startswith('<w:rStyle w:val="ms3"'):
            i1=rida2.find('<w:t>')
            i2=rida2.find('</w:t>')
            marksona.attrib['x:i']=rida2[i1+5:i2]
            marksona.attrib['x:O']=marksona.text+rida2[i1+5:i2]
            
        rida3=b[rida+3]
        i1=rida3.find('<w:t>')
        i2=rida3.find('</w:t>')
        kolmas_rida=rida3[i1+5:i2]
        if rida3.startswith('<w:rStyle w:val="ms'):
            marksona.text=marksona.text+kolmas_rida
    return snr

##for j,i in enumerate(b):
##    if not i:
##        try:
##            snr=xmliks(snr, j)
##        except IndexError:
##            pass

while b:
    a=b.pop(0)
    if "<w:t>#NBH#</w:t>" in a:
        eelmine = True
    if a.startswith('<w:rStyle w:val="ms'):
        if eelmine:
            ms=ms+a
        ms = a
        print(a)
        
#tree = ET.ElementTree(snr)
#tree.write("ms.xml", encoding='utf8')


    