import xml.etree.ElementTree as ET
snr=ET.Element("sr")

f = open('08.xml.eelex.txt', 'r', encoding='utf8')
a=f.readlines()
b=[i.strip() for i in a]

def listiks(alglist):
    c=[]
    for i,j in enumerate(alglist):
        if not j:
            try:
                if "<w:t>2.</w:t>" in alglist[i+1]: #regulaaravaldised, find
                    pass
                else:
                    c.append("¤")
            except IndexError:
                pass        
        else:
            c.append(j)
    return c

d=listiks(b)


def xmliks(snr, rida):
    sisutekst=""
    ms_rida=d[rida+1]
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

#tahaks siin teha tsükli, et ei peaks iga kord uut rida uuesti defineerima
#liitsõna-märksõnade lisamine (kui ühes artiklis on mitu liitsõna, siis hetkel lisab ainult esimese)
        rida2=d[rida+2]
        i1=rida2.find('<w:t>')
        i2=rida2.find('</w:t>')
        teine_rida=rida2[i1+5:i2]
        if teine_rida.startswith('|'):
            marksona.text=marksona_ise+teine_rida

        rida3=d[rida+3]
        i1=rida3.find('<w:t>')
        i2=rida3.find('</w:t>')
        kolmas_rida=rida3[i1+5:i2]
        if rida3.startswith('<w:rStyle w:val="ms'):
            marksona.text=marksona.text+kolmas_rida

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
        elif rida2.startswith('<w:rStyle w:val="ms3"'):
            i1=rida2.find('<w:t>')
            i2=rida2.find('</w:t>')
            marksona.attrib['x:i']=rida2[i1+5:i2].strip()
            marksona.attrib['x:O']=marksona.text+rida2[i1+5:i2].strip()

        else:
            
            i=rida+2
            while d: 
               sisutekst=sisutekst+b[i]
               #print(sisutekst)
               i=i+1

            #sisu = ET.SubElement(artikkel, "x:S")
            #sisu.text=sisutekst
            #sisutekst=""   

    return snr


for j,i in enumerate(d):
    if i.startswith("¤"):       
        try:
            snr=xmliks(snr, j)          
        except IndexError:
            pass

##eelmine=False
##ms=""
##
##c=b[:100]
##while c:
##    a=c.pop(0)
##    if 'w:val="ms1"' in a:
##        eelmine = True
##        ms1=a
##        if a.startswith('<w:rStyle w:val="ms2') and eelmine==True:
##            ms=ms1+a
##        else:
##            ms=ms1
##        eelmine=False
##        print(ms)
        
tree = ET.ElementTree(snr)
tree.write("ms.xml", encoding='utf8')


    