"""
USAGE:
python3 ilusta.py ms.xml

"""
import sys

from lxml import etree
# print("running with lxml.etree")


with open(sys.argv[1],'r') as f:
    snr = etree.parse(f)

# print(snr)
print(str(etree.tostring(snr,
                         encoding='utf8',
                         pretty_print=True).decode('utf8')
)
)
