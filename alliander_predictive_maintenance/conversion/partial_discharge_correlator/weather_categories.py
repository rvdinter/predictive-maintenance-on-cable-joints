from enum import Enum


class WeatherCategories(Enum):
    """ Categories of Weather data from KNMI Daggegevens and CDS Era5sl"""

    WIND = ['wind_direction', 'FHVEC', 'wind_speed', 'wind_speed_max', 'wind_speed_max_hour', 'wind_speed_min',
            'wind_speed_min_hour', 'wind_gust_max', 'wind_gust_max_hour', '100m_u_component_of_wind',
            '100m_v_component_of_wind', '10m_u_component_of_wind', '10m_v_component_of_wind']
    TEMPERATURE = ['temperature', 'temperature_min', 'temperature_min_hour', 'temperature_max', 'temperature_max_hour',
                   'T10N', 'T10NH', '2m_temperature']
    SOIL_TEMPERATURE = ['soil_temperature_level_1', 'soil_temperature_level_2', 'soil_temperature_level_3',
                        'soil_temperature_level_4']
    PRECIPITATION = ['precipitation_duration', 'precipitation', 'precipitation_max', 'precipitation_max_hour',
                     'total_precipitation']
    HUMIDITY = ['humidity', 'humidity_max', 'humidity_max_hour', 'humidity_min', 'humidity_min_hour']
    SOLAR = ['sunlight_duration', 'percentage_of_max_possible_sunlight_duration', 'surface_solar_radiation_downwards',
             'surface_solar_radiation_downward_clear_sky', 'global_radiation']
    AIR_PRESSURE = ['air_pressure', 'air_pressure_max', 'air_pressure_max_hour', 'air_pressure_min',
                    'air_pressure_min_hour']
    VISION = ['VVN', 'VVNH', 'VVX', 'VVXH']
    WATER_IN_SOIL = ['volumetric_soil_water_layer_1', 'volumetric_soil_water_layer_2', 'volumetric_soil_water_layer_3',
                     'volumetric_soil_water_layer_4']
    OTHER = ['EV24', 'cloud_cover', '2m_dewpoint_temperature', 'mean_sea_level_pressure', 'mean_wave_period',
             'surface_pressure', 'sea_surface_temperature', 'significant_height_of_combined_wind_waves_and_swell']
