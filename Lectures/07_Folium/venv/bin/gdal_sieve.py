#!/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Lectures/07_Folium/venv/bin/python3.9

import sys
# import osgeo.utils.gdal_sieve as a convenience to use as a script
from osgeo.utils.gdal_sieve import *  # noqa
from osgeo.utils.gdal_sieve import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdal_sieve', 'utils')
sys.exit(main(sys.argv))
