import xml.etree.ElementTree as ET
import re
from xml.sax.saxutils import escape
import locale
snr=ET.Element("x:sr")

snr.attrib['xmlns:x']="http://www.eki.ee/dict/hem"
snr.attrib['xml:lang']="et"

f = open("08.xml.eelex.txt", "r", encoding="utf-8")
a=f.readlines()
b=[i.strip() for i in a]


#teeb algfaili listiks, kus iga rida on üks listi element
def listiks(alglist):
    c=[]
    #märksõnu eraldab ¤ märk
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
                    alglist[i+1]=re.sub('\<w:i\/\>\<w:sz w:val="20"\/\>', '<w:rStyle w:val="ms1it"/>', alglist[i+1])
                elif alglist[i+1].startswith('	'):
                    alglist[i+1]=re.sub('^	','',alglist[i+1])
                #ž oli alati muust tekstist eraldatud ja eraldi tekstimärgendite vahel, parandab selle ära
                if 'ž' in alglist[i+1]:
                    alglist[i+1]=re.sub('\<\/w:t\>\<w:t\>ž\<\/w:t\>\<w:t\>','ž',alglist[i+1])
            except IndexError:
                pass
        else:
            try:
                if 'ž' in alglist[i+1]:
                    alglist[i+1]=re.sub('\<\/w:t\>\<w:t\>ž\<\/w:t\>\<w:t\>','ž',alglist[i+1])
            except IndexError:
                pass

    #kustutab ära tühjad read kui tegemist on alltähendusega    
    for i,j in enumerate(alglist): #i on indeks, j on rida
        if j.startswith('<w:rStyle w:val="ms1"'):
            #jätab liitsõna märksõna esimese osa meelde
            msrida=j
        if not j:
            try:
                line2=re.search('[0-9]{1,2}\.', alglist[i+1])
                #lisab € märgi enne tähendusgruppide numbrite rida
                if not line2==None:
                    c.append('€')
                #lisab % enne Vrd kui sellele eelneb tühi rida, sest siis on tegemist terve artikli viitegrupiga ja mitte ainult tähendusviitega
                elif "Vrd" in alglist[i+1]:
                    c.append('%')
                else:
                    c.append("¤")
            except IndexError:
                pass
        else:
        #lisab ¤ märgi ja liitsõnade esimese osa enne liitsõnade teist osa    
            try:
                if "	<w:t>#NBH#</w:t>" in alglist[i+1] or ", </w:t><w:t>#NBH#</w:t>" in alglist[i+1] or "<w:t> </w:t><w:t>#NBH#</w:t>" in alglist[i+1]:
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
#d on lõpplist, millega edasi tegeleda

#for i in d:
#   print(i)

#kohalühendite list
kohalyh=['Amb', 'Ann', 'Ans', 'Aud', 'Emm', 'Hag', 'Han', 'Har', 'Hel', 'HJn', 'Hlj', 'HljK', 'Hls', 'HMd', 'Hää', 'Iis', 'IisK', 'IisR', 'Jaa', 'JJn', 'JMd', 'Juu', 'Jõe', 'JõeK', 'Jõh', 'Jäm', 'Jür', 'Kaa', 'Kad', 'Kam', 'Kan', 'Kei', 'Khk', 'Khn', 'Kir', 'KJn', 'Kod', 'KodT', 'Koe', 'Kos', 'Kra', 'Krj', 'Krk', 'Krl', 'Kse', 'Ksi', 'Kul', 'Kuu', 'KuuK', 'Kõp', 'Käi', 'Kär', 'Lai', 'Lei', 'Lih', 'LNg', 'Luk', 'Lut', 'Lüg', 'Mar', 'Mih', 'MMg', 'MMgT', 'Muh', 'Mus', 'Mär', 'Nai', 'Nis', 'Noa', 'Nõo', 'Ote', 'Pai', 'Pal', 'Pee', 'Pha', 'Phl', 'Pil', 'PJg', 'Plt', 'Plv', 'Pst', 'Puh', 'Pär', 'Pöi', 'Rak', 'RakR', 'Ran', 'Rap', 'Rei', 'Rid', 'Ris', 'Rõn', 'Rõu', 'Räp', 'Saa', 'San', 'Se', 'Sim', 'SJn', 'TMr', 'Tor', 'Trm', 'Trv', 'Tõs', 'Tür', 'Urv', 'Vai', 'Var', 'Vas', 'Vig', 'Vil', 'VJg', 'Vll', 'VMr', 'VNg', 'Vor', 'Võn', 'Vän', 'Äks']


def xmliks(snr, rida):
    i=rida+1
    kommentaar=""
    
    while not d[i].startswith("¤"):

        #märksõna lisamine artiklisse
        if d[i].startswith('<w:rStyle w:val="ms1') or (d[i].startswith('<w:rStyle w:val="PoolpaksKiri"/>') and d[i-1].startswith("¤")):
            marksona_ise=re.search('(?<=\<w:t\>)\*{,1}[\w|\-|\(|\)]+', d[i])
            artikkel = ET.SubElement(snr, "x:A")
            pais = ET.SubElement(artikkel, "x:P")
            ms_grupp = ET.SubElement(pais, "x:mg")
            marksona = ET.SubElement(ms_grupp, "x:m")
            marksona.text=marksona_ise.group(0)
            if d[i].startswith('<w:rStyle w:val="ms1it"'):
                marksona.attrib['x:liik']="h"
                
            
        #liitsõna teiste osade lisamine märksõnale
        elif ("<w:t>|</w:t>" in d[i] or "	<w:t>#NBH#</w:t>" in d[i] or ", </w:t><w:t>#NBH#</w:t>" in d[i] or "<w:t> </w:t><w:t>#NBH#</w:t>" in d[i]) and marksona.text!="":
            marksona.text=marksona.text+"|"
            
        elif (d[i].startswith('<w:rStyle w:val="ms2"') or d[i].startswith('<w:rStyle w:val="ms4"')) and marksona.text.endswith("|"):
            liits=re.search('(?<=\<w:t\>)[\w|\||\(|\)]+', d[i])
            marksona.text=marksona.text+liits.group(0)

        #atribuutide lisamine märksõnale
        elif d[i].startswith('<w:rStyle w:val="ms3"'):
            ms_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i])
            if not ms_attrib==None:
                marksona.attrib['x:i']=ms_attrib.group(0)
                marksona.attrib['x:O']=marksona.text+ms_attrib.group(0)

        #märksõnaviite lisamine
        elif '→' in d[i]:
            msviide=re.search('(?<=\<w:t\>→\<\/w:t\>\<w:t\>)[\w|\s|\-]+-{0,1}', d[i])
            #osad märksõnaviited ei ole → märgiga sama real, seega õigesse kohta ei paigutu
            if not msviide==None:
                mvtg = ET.SubElement(pais, "x:mvtg")
                mvt = ET.SubElement(mvtg, "x:mvt")
                mvt.text=(msviide.group(0)).strip()
                mvt.attrib['x:mvtl']="var"

        #atribuutide lisamine märksõnaviitele
        elif 'superscript' in d[i] and '→' in d[i-1]:
            mvt_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i])
            mvt.attrib['x:i']=mvt_attrib.group(0)


        #tähendusviite lisamine
        elif 'Vrd' in d[i] and not '%' in d[i-1]:
            #töötab korrektselt kui on ainult üks tähendusviide, rohkemate viidete puhul paigutab õigesse kohta ainult esimese
            #probleem selles, et mitme viite vahel on vahel komad, vahel tekstimärgendid, vahel on need eri ridadel
            th_viide=re.search('(?<=\<w:t\>)[\w|\s|\-]+', d[i+1])
            if not th_viide==None:
                th_viide=(th_viide.group(0)).strip()
                if not 'sisu' in locals():
                    sisu = ET.SubElement(artikkel, "x:S")
                    rnrp = ET.SubElement(sisu, "x:rp")
                    thnrp = ET.SubElement(rnrp, "x:tp")
                    thnrp.attrib['x:tnr']='1'
                    thgr = ET.SubElement(thnrp, "x:tg")
                    thnr_vg=ET.SubElement(thgr, "x:tvtg")
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=th_viide
                    thv.attrib['x:tvtl']="syn"
                elif not 'thnrp' in locals():
                    thnrp = ET.SubElement(rnrp, "x:tp")
                    thnrp.attrib['x:tnr']='1'
                    thgr = ET.SubElement(thnrp, "x:tg")
                    thnr_vg=ET.SubElement(thgr, "x:tvtg")
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=th_viide
                    thv.attrib['x:tvtl']="syn"
                elif not 'thgr' in locals():
                    thgr = ET.SubElement(thnrp, "x:tg")
                    thnr_vg=ET.SubElement(thgr, "x:tvtg")
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=th_viide
                    thv.attrib['x:tvtl']="syn"  
                else:
                    thnr_vg=ET.SubElement(thgr, "x:tvtg")
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=th_viide
                    thv.attrib['x:tvtl']="syn"                    
            if 'superscript' in d[i+2]:
                thv_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i+2])
                thv.attrib['x:i']=thv_attrib.group(0)


        #artikliviidete lisamine
        #töötab samuti korrektselt ainult ühe artikliviite puhul, rohkemate artikliviidete puhul lisab ainult esimese
        elif 'Vrd' in d[i] and '%' in d[i-1]:
            art_viide=re.search('(?<=\<w:t\>)[\w|\s|\-]+', d[i+1])
            if not art_viide==None:
                art_viide=(art_viide.group(0)).strip()
                if not 'sisu' in locals():
                    sisu = ET.SubElement(artikkel, "x:S")
                    rnrp = ET.SubElement(sisu, "x:rp")
                    avg = ET.SubElement(rnrp, "x:atvtg")
                    artviide=ET.SubElement(avg, "x:tvt")
                    artviide.text=art_viide
                    artviide.attrib['x:tvtl']="syn"
                else:
                    avg = ET.SubElement(rnrp, "x:atvtg")
                    artviide=ET.SubElement(avg, "x:tvt")
                    artviide.text=art_viide
                    artviide.attrib['x:tvtl']="syn"
            if 'superscript' in d[i+2]:
                art_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i+2])
                artviide.attrib['x:i']=art_attrib.group(0)
                

        #üld-tähendusviidete lisamine
        elif 'Vt' in d[i]:
            yld_viide=re.search('(?<=\<w:t\>)[\w|\s|\-]+', d[i+1])
            if not yld_viide==None:
                yld_viide=(yld_viide.group(0)).strip()
                if not 'sisu' in locals():
                    sisu = ET.SubElement(artikkel, "x:S")
                    rnrp = ET.SubElement(sisu, "x:rp")
                    thnrp = ET.SubElement(rnrp, "x:tp")
                    thnrp.attrib['x:tnr']='1'
                    thgr = ET.SubElement(thnrp, "x:tg")
                    thnr_vg=ET.SubElement(thgr, "x:tvtg")
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=yld_viide
                    thv.attrib['x:tvtl']="yld"
                elif not 'thnr_vg' in locals():
                    thnr_vg=ET.SubElement(thgr, "x:tvtg")
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=yld_viide
                    thv.attrib['x:tvtl']="yld"
                else:
                    thv=ET.SubElement(thnr_vg, "x:tvt")
                    thv.text=th_viide
                    thv.attrib['x:tvtl']="yld"
            if 'superscript' in d[i+2]:
                thv_attrib=re.search('(?<=\<w:t\>)[0-9]{1,2}', d[i+2])
                thv.attrib['x:i']=thv_attrib.group(0)

        #tähendusgrupid
        #teeb praegu väga ebaintelligentselt 7 tähendusgruppi, ilmselt saaks siin kasutada while tsüklit
        #kood töötabki ainult max 7 tähendusgrupi korral, rohkemate tähendusgruppide puhul lisab ülejäänud sisu viimase tähendusgrupi alla
        elif d[i].startswith('€'):
            if not 'thnrp' in locals():
                sisu = ET.SubElement(artikkel, "x:S")
                rnrp = ET.SubElement(sisu, "x:rp")
                thnrp = ET.SubElement(rnrp, "x:tp")
                thnrp.attrib['x:tnr']='1'
            elif not 'thnrp2' in locals():
                thnrp2 = ET.SubElement(rnrp, "x:tp")
                number=(re.search('[0-9]{1,2}\.', d[i+1])).group(0)
                number2=re.search('([^.]*)', number).group(0)
                thnrp2.attrib['x:tnr']=number2
            elif not 'thnrp3' in locals():
                thnrp3 = ET.SubElement(rnrp, "x:tp")
                number=(re.search('[0-9]{1,2}\.', d[i+1])).group(0)
                number2=re.search('([^.]*)', number).group(0)
                thnrp3.attrib['x:tnr']=number2
            elif not 'thnrp4' in locals():
                thnrp4 = ET.SubElement(rnrp, "x:tp")
                number=(re.search('[0-9]{1,2}\.', d[i+1])).group(0)
                number2=re.search('([^.]*)', number).group(0)
                thnrp4.attrib['x:tnr']=number2
            elif not 'thnrp5' in locals():
                thnrp5 = ET.SubElement(rnrp, "x:tp")
                number=(re.search('[0-9]{1,2}\.', d[i+1])).group(0)
                number2=re.search('([^.]*)', number).group(0)
                thnrp5.attrib['x:tnr']=number2
            elif not 'thnrp6' in locals():
                thnrp6 = ET.SubElement(rnrp, "x:tp")
                number=(re.search('[0-9]{1,2}\.', d[i+1])).group(0)
                number2=re.search('([^.]*)', number).group(0)
                thnrp6.attrib['x:tnr']=number2
            elif not 'thnrp7' in locals():
                thnrp7 = ET.SubElement(rnrp, "x:tp")
                number=(re.search('[0-9]{1,2}\.', d[i+1])).group(0)
                number2=re.search('([^.]*)', number).group(0)
                thnrp7.attrib['x:tnr']=number2


        #näidete lisamine
        #töötab samuti hetkel max 7 tähendusgrupiga, sest ei osanud intelligentsemat lahendust välja mõelda
        #ilmselt saaks selle osa ühendada eelmisega while-tsüklis, aga ei osanud

        #eristab näiteid grammatikast selle järgi, et näidete puhul on tekstimärgendite vahel tühikud
        #mõned grammatikaelementide tekstimärgendid sisaldavad ka tühikuid, need on siis ka näidete märgendi saanud
        #sellisel juhul tekib kaks nr1 tähendusgruppi

        #kui näite sees on (kant)sulgudes kommentaar või täiendus, siis algfailis oli see eraldi real (kuna teistsuguse vormistusega) ja seega selle koha peal läheb näide pooleks

        #kui algfailis näitele kihelkonda ei järgnenud (st mitu näidet oli samast kohast), siis kõige viimane neist saab kihelkonnamärgendi ja ülejäänud jäävad ilma
        #sealjuures jäävad need näited kõik eri näitegruppidesse, kuigi sama kihelkonna puhul võiks nad olla samas näitegrupis
        elif (d[i].startswith('<w:i/><w:sz w:val="20"') or d[i].startswith('<w:i/>	')) and not ' </w:t><w:t>#NBH#' in d[i] and ' ' in (re.sub('\<[\/]*w[^\>]*\>', '', d[i])).strip():
            naide=(re.sub('\<[\/]*w[^\>]*\>', '', d[i])).strip()
            naide=re.sub('#NBH#', '-', naide)
            if not 'sisu' in locals():
                sisu = ET.SubElement(artikkel, "x:S")
                rnrp = ET.SubElement(sisu, "x:rp")
                thnrp = ET.SubElement(rnrp, "x:tp")
                thnrp.attrib['x:tnr']='1'
                thgr = ET.SubElement(thnrp, "x:tg")
                nplokk = ET.SubElement(thgr, "x:np")
                ngrupp = ET.SubElement(nplokk, "x:ng")
                naide_ise= ET.SubElement(ngrupp, "x:n")
                naide_ise.text=naide
                khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                kihelkonnatekst=re.search('([\w]*)', khlk)
                if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                   if not kihelkonnatekst==None:
                        kihelkonnatekst=kihelkonnatekst.group(0)
                        kihelkond= ET.SubElement(ngrupp, "x:khk")
                        kihelkond.text=kihelkonnatekst
            elif not 'thnrp2' in locals():
                if not 'nplokk' in locals():
                    thgr = ET.SubElement(thnrp, "x:tg")
                    nplokk = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                       if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                       if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
            elif not 'thnrp3' in locals():
                if not 'nplokk2' in locals():
                    thgr = ET.SubElement(thnrp2, "x:tg")
                    nplokk2 = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk2, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                       if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk2, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
            elif not 'thnrp4' in locals():
                if not 'nplokk3' in locals():
                    thgr = ET.SubElement(thnrp3, "x:tg")
                    nplokk3 = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk3, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk3, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
            elif not 'thnrp5' in locals():
                if not 'nplokk4' in locals():
                    thgr = ET.SubElement(thnrp4, "x:tg")
                    nplokk4 = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk4, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk4, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
            elif not 'thnrp6' in locals():
                if not 'nplokk5' in locals():
                    thgr = ET.SubElement(thnrp5, "x:tg")
                    nplokk5 = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk5, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk5, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
            elif not 'thnrp7' in locals():
                if not 'nplokk6' in locals():
                    thgr = ET.SubElement(thnrp6, "x:tg")
                    nplokk6 = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk6, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk6, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
            else:
                if not 'nplokk7' in locals():
                    thgr = ET.SubElement(thnrp7, "x:tg")
                    nplokk7 = ET.SubElement(thgr, "x:np")
                    ngrupp = ET.SubElement(nplokk7, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst
                else:
                    ngrupp = ET.SubElement(nplokk7, "x:ng")
                    naide_ise= ET.SubElement(ngrupp, "x:n")
                    naide_ise.text=naide
                    khlk=(re.sub('\<[\/]*w[^\>]*\>', '', d[i+1])).strip()
                    kihelkonnatekst=re.search('([\w]*)', khlk)
                    if any(kihelkond in kihelkonnatekst.group(0) for kihelkond in kohalyh):
                        if not kihelkonnatekst==None:
                            kihelkonnatekst=kihelkonnatekst.group(0)
                            kihelkond= ET.SubElement(ngrupp, "x:khk")
                            kihelkond.text=kihelkonnatekst

        #koondab kogu artikli teksti kommentaari nime alla
        kommentaar=kommentaar+re.sub('\<[\/]*w[^\>]*\>', '', d[i])
        i=i+1

    #lisab kogu artikli sisu lõppfaili data elementi
    if not 'kommentaar'=="":
        data=ET.SubElement(artikkel, "x:data")
        kommentaar=re.sub('#NBH#', '-', kommentaar)
        kommentaar=re.sub('€', '', kommentaar)
        kommentaar=re.sub('%', '', kommentaar)
        data.text=kommentaar.strip()

    return snr

#käib terve algfailist saadud listi läbi
for j,i in enumerate(d): #j on indeks, i on rida
    if i.startswith("¤"):
        try:
            snr=xmliks(snr, j)          
        except IndexError:
            pass

#tekitab xml-faili       
tree = ET.ElementTree(snr)
tree.write("ms.xml", encoding="utf8")

#hiljem kustutasin tühjad märgendid käsureal, sest ei saanud ET.remove() funktsiooni kasutamisest täpselt aru


#käsitsi algfailis tehtud parandused:

##püstkriipsud märksõnade järelt kustutatud - üldiselt olid liitsõna püstkriipsud eraldi real, mõnel juhul aga liitsõna esimese osa järel, mis tekitas märksõnadesse topelt-püstkriipse või jättis mõned liitsõnad vahele (nt kadakapuu, kadakmari)
##ülesleitud juhtudel on grammatika tekstimärgenditest kustutatud tühik, et neid ei loetaks näidete hulka (nt kaksama, kahar, kajama)
##mõnikord oli grammatikas leiduv sidekriips ja käände/pöördelõpp eraldi ridadel ja sellega luges kood neid ridu kui liitsõna teist osa ja võis tekitada topelt-artikleid, nende puhul on algfailis #NBH# ja sellele järgnev käände/pöördelõpp ühele reale tõstetud (nt kalingur, kahar)
##liitsõnade puhul on - asendatud #NBH#-ga, sest ainult üksikutel juhtudel oli liitsõna teise osa ees sidekriips (nt kahekeelne, kahekerru)