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

#ühtlustab märgendeid (kõik märksõnad ei ole märgendiga ms1 ja osadel on tärnid eelneval real)
    for i,j in enumerate(alglist):
        if not j:
            try:
                line=re.search('[0-9]{1,2}\.', alglist[i+1])
                if alglist[i+1].startswith('<w:b/><w:sz w:val="20"/>') and '<w:t>*</w:t>' in alglist[i+1]:
                    alglist[i+1]=re.sub('^.*$', ' ', alglist[i+1])
                    alglist[i+2]=re.sub('\<w:t\>', '<w:t>*', alglist[i+2])
                elif alglist[i+1].startswith('<w:b/><w:sz w:val="20"/>') and not 'Vrd' in alglist[i+1] and line==None:
                    alglist[i+1]=re.sub('\<w:b\/\>\<w:sz w:val="20"\/\>', '<w:rStyle w:val="ms1"', alglist[i+1])
                elif alglist[i+1].startswith('<w:i/><w:sz w:val="20"/>') and not 'Vrd' in alglist[i+1] and line==None:
                    alglist[i+1]=re.sub('\<w:i\/\>\<w:sz w:val="20"\/\>', '<w:rStyle w:val="ms1"/>', alglist[i+1])
            except IndexError:
                pass

    #kustutab ära tühjad read kui tegemist on alltähendusega    
    for i,j in enumerate(alglist): #i on indeks, j on rida
        if j.startswith('<w:rStyle w:val="ms1"'):
            msrida=j
        if not j:
            try:
                line2=re.search('[0-9]{1,2}\.', alglist[i+1])
                if not line2==None:
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

    c.append('¤')
    return c

d=listiks(b)


#for i in d[10000:]:
#   print(i)

#kustutab ära tühjad märgendid
#for i in d:
#    uus=re.sub('\<w:t\>[ ]*\<\/w:t\>','',i)

sisutekst=""
def xmliks(snr, rida):
    i=rida+1
    sisutekst=""
    art_viide=""
    while not d[i].startswith("¤"):
        if d[i].startswith('<w:rStyle w:val="ms1"') or (d[i].startswith('<w:rStyle w:val="PoolpaksKiri"/>') and d[i-1].startswith("¤")):
            marksona_ise=re.search('(?<=\<w:t\>)\*{,1}[\w|-]+', d[i])
            #\w hulgas ei ole š, z ja ž tähti
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
            msviide=re.search('(?<=\<w:t\>→\<\/w:t\>\<w:t\>)[\w|\s|]+-{0,1}', d[i])
            #järgnev tingimus lisatud sest osad märksõnaviited ei ole → märgiga sama real
            #(ja jäävad praegu seega xml-ist välja, kuidas seda lahendada?)
            if not msviide==None:
                mvtg = ET.SubElement(pais, "x:mvtg")
                mvt = ET.SubElement(mvtg, "x:mvt")
                mvt.text=(msviide.group(0)).strip()
        #atribuutide lisamine märksõnale
        elif d[i].startswith('<w:rStyle w:val="ms3"'):
            ms_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i])
            if not ms_attrib==None:
                marksona.attrib['x:i']=ms_attrib.group(0)
                marksona.attrib['x:O']=marksona.text+ms_attrib.group(0)
        elif 'Vrd' in d[i]:
            #töötab hetkel kui on ainult üks tähendusviide
            #mitme viite vahel on komad või märgendid, aga kuidas neid ka ikka arvestada saaks?
            art_viide=re.search('(?<=\<w:t\>)[\w|\s]+', d[i+1])
            if not art_viide==None:
                art_viide=art_viide.group(0)
                               
          
        #liidab kogu ülejäänud artikli sisu kokku ja kustutab märgendid
        else:
            sisutekst=sisutekst+re.sub('\<[\/]*w[^\>]*\>', '', d[i])
#            print(sisutekst)

        i=i+1

    sisu = ET.SubElement(artikkel, "x:S")
    rnrp = ET.SubElement(sisu, "x:rp")
    muu = ET.SubElement(rnrp, "x:km")
    sisutekst=re.sub('#NBH#', '-', sisutekst)
    muu.text=sisutekst
    sisutekst=""
    avg = ET.SubElement(rnrp, "x:atvtg")
    aviide = ET.SubElement(avg, "x:tvt")
    aviide.text=art_viide

    return snr


for j,i in enumerate(d):
    if i.startswith("¤"):
        try:
            snr=xmliks(snr, j)          
        except IndexError:
            pass

        
tree = ET.ElementTree(snr)
tree.write("ms.xml", encoding='utf8')


    
