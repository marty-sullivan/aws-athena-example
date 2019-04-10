
#
# Name of the CloudFormation Stack to create
#

STACK_NAME="AthenaLambdaExample"

#
# NDFD weather element to forecast
#

NDFD_ELEMENT="temp"

#
# Coordinates for the center point of the forecast
#
# Contiguous US boundaries for NDFD:
#
# Latitude:  20.1920 - 52.8077
# Longitude: -130.1034 - -60.8856
#

CENTER_LATITUDE="42.6777"
CENTER_LONGITUDE="-76.6990"

#
# Timezone for timestamps in the forecast (must be valid TZ database name)
# https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#

TIMEZONE='America/New_York'
