#!/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Lectures/07_Folium/venv/bin/python3.9

import sys
# import osgeo.utils.gdalchksum as a convenience to use as a script
from osgeo.utils.gdalchksum import *  # noqa
from osgeo.utils.gdalchksum import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdalchksum', 'utils')
sys.exit(main(sys.argv))
