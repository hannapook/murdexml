import xml.etree.ElementTree as ET

#hetkel defineeritud juhuslikud atribuudid-elemendid
marksona_ise="maja"
sorteerimisvaartus="maja"
msviite_liik="var"
tahendusnr="1"
alamstahendusnr="1"
thviite_liik="syn"
art_thviite_liik="yld"

artikkel = ET.Element("x:A")
pais = ET.SubElement(artikkel, "x:P")

mg = ET.SubElement(pais, "x:mg")

marksona = ET.SubElement(mg, "x:m", O=sorteerimisvaartus)
marksona.text=marksona_ise

vormikood = ET.SubElement(mg, "x:vk")
varp = ET.SubElement(mg, "x:varp")

varg = ET.SubElement(varp, "x:varg")
variant = ET.SubElement(varg, "x:var")
levg = ET.SubElement(varg, "x:levg")

kohalyh = ET.SubElement(levg, "x:kly")
paralg = ET.SubElement(levg, "x:parg")

vormikood_par = ET.SubElement(paralg, "x:vk")
variant_par = ET.SubElement(paralg, "x:var")

msviideg = ET.SubElement(pais, "x:mvtg")
msviide = ET.SubElement(msviideg, "x:mvt", mvtl=msviite_liik)

sisu = ET.SubElement(artikkel, "x:S")

rnrp = ET.SubElement(sisu, "x:rp")
thnrp = ET.SubElement(rnrp, "x:tp")
thgrupp = ET.SubElement(thnrp, "x:tg", tnr=tahendusnr)
defgrupp = ET.SubElement(thgrupp, "x:dg")

stiil = ET.SubElement(defgrupp, "x:s")
seletus = ET.SubElement(defgrupp, "x:d")

ntpuuduvad = ET.SubElement(thgrupp, "x:np0")
kohalyh_np0 = ET.SubElement(ntpuuduvad, "x:kly")

naitep = ET.SubElement(thgrupp, "x:np")
naiteg = ET.SubElement(naitep, "x:ng")
naide = ET.SubElement(naiteg, "x:n")
stiil_naide = ET.SubElement(naide, "x:s")
kihelk = ET.SubElement(naide, "x:khk")

alamsp = ET.SubElement(thgrupp, "x:amp")
alamsg = ET.SubElement(alamsp, "x:amg")
alams = ET.SubElement(alamsg, "x:am")

alamsthnrp = ET.SubElement(alamsp, "x:atp", anr=alamstahendusnr)
alamsthg = ET.SubElement(alamsthnrp, "x:atg")
alamsdefg = ET.SubElement(alamsthg, "x:adg")

stiil = ET.SubElement(alamsdefg, "x:s")
seletus = ET.SubElement(alamsdefg, "x:d")

ntpuuduvad_alams = ET.SubElement(alamsthg, "x:np0")
kohalyh_np0_alams = ET.SubElement(ntpuuduvad_alams, "x:kly")

naitep_alams = ET.SubElement(alamsthg, "x:np")
naiteg_alams = ET.SubElement(naitep_alams, "x:ng")
naide_alams = ET.SubElement(naiteg_alams, "x:n")
stiil_naide_alams = ET.SubElement(naide_alams, "x:s")
kihelk_alams = ET.SubElement(naide_alams, "x:khk")

thnr_viiteg = ET.SubElement(thnrp, "x:ptvtg")
thnr_viide = ET.SubElement(thnr_viiteg, "x:tvt", tvtl=thviite_liik)

artikli_viiteg = ET.SubElement(rnrp, "x:atvtg")
artikli_viide = ET.SubElement(artikli_viiteg, "x:tvt", tvtl=art_thviite_liik)

tree = ET.ElementTree(artikkel)
tree.write("valmis_xml.xml")