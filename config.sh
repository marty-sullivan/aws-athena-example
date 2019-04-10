
#
# Name of the CloudFormation Stack to create
# IMPORTANT: Use lower case letters only!
#

STACK_NAME="mainetemperatureforecast"

#
# Indicates whether to auto-run the state machine at half-past each hour
#

AUTORUN="true"

#
# NDFD weather element to forecast
#

NDFD_ELEMENT="temp"

#
# Square KM for the forecast map
# Note: Larger area is fine, just understand: Lambda will run longer and output data will be larger!
#

SQUARE_KM="150"

#
# Coordinates for the center point of the forecast in CONUS
#
# Contiguous US (CONUS) boundaries for NDFD:
#
# Latitude:  20.1920 - 52.8077
# Longitude: -130.1034 - -60.8856
#

CENTER_LATITUDE="43.6591"
CENTER_LONGITUDE="-70.2568"

#
# Timezone for timestamps in the forecast (must be valid TZ database name)
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#

TIMEZONE='America/New_York'
