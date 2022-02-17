#!/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Lectures/07_Folium/venv/bin/python3.9

import sys
# import osgeo.utils.gdal_proximity as a convenience to use as a script
from osgeo.utils.gdal_proximity import *  # noqa
from osgeo.utils.gdal_proximity import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdal_proximity', 'utils')
sys.exit(main(sys.argv))
