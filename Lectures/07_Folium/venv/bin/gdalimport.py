#!/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Lectures/07_Folium/venv/bin/python3.9

import sys
# import osgeo.utils.gdalimport as a convenience to use as a script
from osgeo.utils.gdalimport import *  # noqa
from osgeo.utils.gdalimport import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdalimport', 'utils')
sys.exit(main(sys.argv))
