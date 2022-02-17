#!/Users/griffin/Dropbox/_Courses/4553-Spatial-DS/Lectures/07_Folium/venv/bin/python3.9

import sys
# import osgeo.utils.gdal_auth as a convenience to use as a script
from osgeo.utils.gdal_auth import *  # noqa
from osgeo.utils.gdal_auth import main
from osgeo.gdal import deprecation_warn


deprecation_warn('gdal_auth', 'utils')
sys.exit(main(sys.argv))
