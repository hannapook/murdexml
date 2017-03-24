import xml.etree.ElementTree as ET
snr=ET.Element("sr")


f = open('08.xml.eelex.txt', 'r', encoding='utf8')
a=f.readlines()
b=[i.strip() for i in a][:999]

for j,i in enumerate(b):
    if not i:
        artikkel = ET.SubElement(snr, "x:A")
        marksona = ET.SubElement(artikkel, "x:m")
        ms_rida=b[j+1]
        i1=ms_rida.find('<w:t>')
        i2=ms_rida.find('</w:t>')
        marksona_ise=ms_rida[i1+5:i2]
        #if not marksona_ise[0].isdigit: - see millegipärast ei tööta
        if marksona_ise.startswith('k'):
            marksona.text=marksona_ise
            #tree = ET.tostring(artikkel)
            #print(tree)

tree = ET.ElementTree(snr)
tree.write("ms.xml")


    