import re
import os.path
from os import path
import glob

ROOT_DIRECTORY = '/Users/garethhouk/Documents/play/Al-Anon Map Project/'

FILE_KML_HEADER = '''<?xml version="1.0" encoding="utf-8" ?>
<kml xmlns="http://www.opengis.net/kml/2.2">
<Document><Folder><name>Al Anon Area 59 (WA) Districts</name>
<Schema name="gz_2010_us_050_00_5m" id="gz_2010_us_050_00_5m">
	<SimpleField name="Name" type="string"></SimpleField>
	<SimpleField name="Boundaries" type="string"></SimpleField>
	<SimpleField name="AREA" type="string"></SimpleField>
	<SimpleField name="DISTRICT" type="integer"></SimpleField>
	<SimpleField name="Color" type="integer"></SimpleField>
</Schema>\n'''

FILE_KML_TAIL = '''</Folder></Document></kml>\n'''

DISTRICT_KML_HEADER = '''<Placemark>
	<name>District {}</name>
  <Style><LineStyle><color>ff0000ff</color></LineStyle>  <PolyStyle><fill>0</fill></PolyStyle></Style>
	<ExtendedData><SchemaData schemaUrl="#gz_2010_us_050_00_5m">
		<SimpleData name="Name">District {}</SimpleData>
		<SimpleData name="AREA">59</SimpleData>
		<SimpleData name="DISTRICT">{}</SimpleData>
		<SimpleData name="Boundaries">{}</SimpleData>
		<SimpleData name="Color">{}</SimpleData>
	</SchemaData></ExtendedData>\n'''

DISTRICT_KML_TAIL = '''</Placemark>\n'''

def get_district_string(s):
    regex_district = '/d(\d*)\.coordinates'
    a = re.search(regex_district,s)
    try:
        return(a.group(1))
    except:
        return('')

def get_all_coordinates_files() -> list:
    all_district_coordinates = glob.glob(ROOT_DIRECTORY+'district_coordinates/*.coordinates')
    dist_numbers = [int(get_district_string(item)) for item in all_district_coordinates]
    # sort into numerical order for ingestion in loops
    sorted_files = [x for y, x in sorted(zip(dist_numbers,all_district_coordinates))]
    return(sorted_files)

def get_district_boundaries(district: str) -> str:
    try:
        with open(ROOT_DIRECTORY+'district_boundaries/d'+str_dist+'.txt', 'r', encoding='ascii') as f:
            boundaries = f.read()
            return(boundaries)
    except:
        return('')

def get_district_color(district: str) -> int:
    try:
        c = int(district) % 20 + 1
    except:
        c = 0
    return(c)

all_district_coordinates = get_all_coordinates_files()

output_file = ROOT_DIRECTORY+'all_districts.kml'
print(f"Writing file {output_file}")
with open(output_file,'w+') as f:
    f.write(FILE_KML_HEADER)
    for district_coordinate_file in all_district_coordinates:
        str_dist = get_district_string(district_coordinate_file)
        boundaries = get_district_boundaries(str_dist)
        district_color = get_district_color(str_dist)
        f.write(DISTRICT_KML_HEADER.format(str_dist,str_dist,int(str_dist),boundaries,district_color))
        with open(district_coordinate_file, 'r', encoding='ascii') as dist_coord_file:
            coordinate_kml = dist_coord_file.read()
        f.write(coordinate_kml)
        f.write(DISTRICT_KML_TAIL)
    f.write(FILE_KML_TAIL)
f.close

def replace_altitude_with_zeros():
    return(0)


