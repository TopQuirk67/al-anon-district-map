import re
import os.path
from os import path

KML_FILE = '/Users/gary/play/Al-Anon Map Project/gz_2010_us_050_00_5m_WA_counties.kml'

KML_HEADER = '''<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document><Folder><name>gz_2010_us_050_00_5m</name>
<Schema name="gz_2010_us_050_00_5m" id="gz_2010_us_050_00_5m">
	<SimpleField name="Name" type="string"></SimpleField>
	<SimpleField name="Description" type="string"></SimpleField>
	<SimpleField name="GEO_ID" type="string"></SimpleField>
	<SimpleField name="STATE" type="string"></SimpleField>
	<SimpleField name="COUNTY" type="string"></SimpleField>
	<SimpleField name="NAME" type="string"></SimpleField>
	<SimpleField name="LSAD" type="string"></SimpleField>
	<SimpleField name="CENSUSAREA" type="float"></SimpleField>
</Schema>'''

KML_TAIL = '''</Folder></Document></kml>'''

# def get_file_header(content):
#     regex_header = '(<\?xml version="1.0" encoding="utf-8" \?>)((?s:.)*?)(<\/Schema>)'
#     a = re.search(regex_header,content)
#     return(a.group(1),a.group(2),a.group(3))

def extract_county_name(s) -> str:
    regex_name = '<name>(.*?)<\/name>'
    a = re.search(regex_name,s)
    return(a.group(1))

def extract_coordinates(s) -> list:
    a = regex_coordinates = '<coordinates>(.*?)<\/coordinates>'
    a = re.search(regex_coordinates,s)
    s_coordinates = a.group(1)
    return([tuple(item.split(',')) for item in s_coordinates.split(' ')])
#    return([(-121.,43.,891.),(-122.,43.5,891.), ])

def make_list_of_WA_counties(content) -> list:
    county_regex = '(<Placemark>)(?s:.)*?(<\/Placemark>)'
    x = re.finditer(county_regex,content)
    counties = []
    for match in x:
        s = match.start()
        e = match.end()
        county_kml = (content[s:e])
        county_name = extract_county_name(county_kml)
        coordinates = extract_coordinates(county_kml)
        county_dict = {'name':county_name,'coordinates':coordinates,'kml':county_kml}
        counties.append(county_dict)
        #print( 'String match "%s" at %d:%d' % (content[s:e], s, e))
    # print(type(x))
    return(counties)
    #return({})

def replace_altitude_with_zeros():
    return(0)

with open(KML_FILE, "r", encoding="ascii") as content_file:
    content = content_file.read()

counties = make_list_of_WA_counties(content)
for item in counties:
    with open('/Users/ghouk/play/Al-Anon Map Project/counties_kml/'+item['name']+'.kml','w+') as f:
        f.write(KML_HEADER)
        f.write(item['kml'])
        f.write(KML_TAIL)
    f.close
