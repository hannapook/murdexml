import xml.etree.ElementTree as ET
import re
from xml.sax.saxutils import escape
snr=ET.Element("sr")

f = open('08.xml.eelex.txt', 'r', encoding='utf8')
a=f.readlines()
b=[i.strip() for i in a]

def listiks(alglist):
    c=[]
    c.append("¤")
    #kustutab ära tühjad read kui tegemist on alltähendusega
    for i,j in enumerate(alglist): #i on indeks, j on rida
        if j.startswith('<w:rStyle w:val="ms1"'):
            msrida=j
        if not j:
            try:
                line=re.findall("[0-9]{1,2}\.", alglist[i+1])
                if not line=="":
                    pass
                elif "Vrd" in alglist[i+1]:
                    pass
                else:
                    c.append("¤")
            except IndexError:
                pass
        else:
        #lisab tühja rea (¤) ja liitsõnade esimese osa enne liitsõnade teist osa    
            try:
                if "	<w:t>#NBH#</w:t>" in alglist[i+1]:
                    c.append(j)
                    c.append("¤")
                    c.append(msrida)
                else:
                    c.append(j)
            except IndexError:
                pass
    return c

d=listiks(b)


#for i in d[:10]:
#    print(i)

sisutekst=""
def xmliks(snr, rida):
    i=rida+1
    sisutekst=""
    while not d[i].startswith("¤"):
        if d[i].startswith('<w:rStyle w:val="ms1"') or (d[i].startswith('<w:rStyle w:val="PoolpaksKiri"/>') and d[i-1].startswith("¤")):
        #eelmise koodirea teine osa ei tööta, vt ms.xml märksõna "kaenla|täis|ohakas|päev|päev"
            marksona_ise=re.search('(?<=\<w:t\>)[\w|-]+', d[i])
            artikkel = ET.SubElement(snr, "x:A")
            pais = ET.SubElement(artikkel, "x:P")
            ms_grupp = ET.SubElement(pais, "x:mg")
            marksona = ET.SubElement(ms_grupp, "x:m")
            marksona.text=marksona_ise.group(0)
        #liitsõna lisamine märksõnale
        elif ("<w:t>|" in d[i] or "	<w:t>#NBH#</w:t>" in d[i]) and marksona.text!="":
            marksona.text=marksona.text+"|"
        elif (d[i].startswith('<w:rStyle w:val="ms2"') or d[i].startswith('<w:rStyle w:val="ms4"')) and marksona.text.endswith("|"):
            liits=re.search('(?<=\<w:t\>)\w+', d[i])
            marksona.text=marksona.text+liits.group(0)
        #märksõnaviite lisamine
        elif '→' in d[i]:
            msviide=re.search('(?<=\<w:t\>→\<\/w:t\>\<w:t\>)[\w|\s]+', d[i])
            #järgnev tingimus lisatud sest osad märksõnaviited ei ole → märgiga sama real (ja jäävad praegu seega xml-ist välja)
            if not msviide==None:
                mvtg = ET.SubElement(pais, "x:mvtg")
                mvt = ET.SubElement(mvtg, "x:mvt")
                mvt.text=(msviide.group(0)).strip()
        #atribuutide lisamine märksõnale
        elif d[i].startswith('<w:rStyle w:val="ms3"'):
            ms_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i])
            #järgnev tingimus lisatud sest osad read algavad ms3 aga on täiesti tühjad, tuleb sellised veel ära kustutada!
            if not ms_attrib==None:
                marksona.attrib['x:i']=ms_attrib.group(0)
                marksona.attrib['x:O']=marksona.text+ms_attrib.group(0)
          
        #liidab kogu ülejäänud artikli sisu kokku ja kustutab märgendid
        else:
            sisutekst=sisutekst+re.sub('\<[\/]*w[^\>]*\>', '', d[i])

        i=i+1

    sisu = ET.SubElement(artikkel, "x:S")
    muu = ET.SubElement(sisu, "x:km")
    sisutekst=re.sub('#NBH#', '-', sisutekst)
    muu.text=sisutekst
    sisutekst=""    
    return snr


for j,i in enumerate(d):
    if i.startswith("¤"):
        try:
            snr=xmliks(snr, j)          
        except IndexError:
            pass

        
tree = ET.ElementTree(snr)
tree.write("ms.xml", encoding='utf8')


    
