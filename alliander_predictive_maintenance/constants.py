from typing import Tuple

# For parsing the FailedJoints data file
FAILED_JOINTS_PRIORITY: int = 10
FAILED_JOINTS_LOCATION_FRACTIONAL_TIME: Tuple[int, int] = (1, 1000)

TEST_CIRCUIT_IDS = [1, 2, 3, 4, 5]

# Error messages
COLUMNS_DO_NOT_MATCH_MANDATORY = "Columns in the data set do not match the mandatory columns."
IEXCEL_READER_LOAD_NOT_CALLED = "The data set file has not been loaded yet. The load() method must be called first."
CIRCUIT_ID_NOT_IN_DATAFRAME = "Circuit ID {circuit_id} is not in the DataFrame."
DATADUMP_NOT_LOADED = "The data dump has not been loaded yet. The load_data_dump() method must be called first."
PARTIAL_DISCHARGE_DATA_FILE_NOT_FOUND = "Partial discharge data file cannot be found at path: {path}"
INVALID_PATH = "The given path is invalid: {path}"
CIRCUIT_CONFIG_FILE_NOT_FOUND = "Circuit Config file cannot be found at path: {path}"
INVALID_ENUM_INPUT = "Invalid enum input"
HTTP_ERROR_COULD_NOT_GET_DATA = "Could not get data from the API"
INVALID_JOINT_LOCATION = "Joint location {location} is invalid with circuit length {circuit_length}"
INVALID_TIME_WINDOW = "TimeWindow {time_window} is out of range for {min}, {max}"
NOTIMPLEMENTEDERROR_AWS = "Alliander S3 environment should load {data} data here"