from odoo import fields, models, api
import meteomatics.api as meteomatics_api
import datetime as dt
import logging

_logger = logging.getLogger(__name__)

class WeatherData(models.Model):
    _name = 'weather.data'
    _description = 'Weather Data'

    location = fields.Char(string='Location')
    temperature = fields.Float(string='Temperature')
    condition = fields.Char(string='Condition',default='Clear')

    def fetch_and_store_weather_data(self):
        # fetch weather data from meteomatics api
        weather_data = self._fetch_weather_data()
        if weather_data:
            print(f"creating record with data:{weather_data}")
            self.create({
                'location':weather_data['location'],
                'temperature':weather_data['temperature'],
                'condition':weather_data['condition']
            })

    def _fetch_weather_data(self):
        username = 'test_sreejith_deepa'
        password = '9xhVPmV4R0'

        coordinates = [(25.2048,-55.2708)]  #dubai coordinates
        parameters = ['t_2m:C'] # temperature at 2meters
        model = 'mix'

        startdate = dt.datetime.utcnow().replace(minute=0,second=0,microsecond=0)
        enddate = startdate + dt.timedelta(hours=1) # forcast for the next hour
        interval = dt.timedelta(hours=1)

        try:
            # query the time series from meteomatics
            df = meteomatics_api.query_time_series(coordinates,startdate,enddate,interval,parameters,username,password,model=model)

            print(f"api response:{df}")

            temperature = df['t_2m:C'].iloc[0]

            print(f"extracted temperature:{temperature}")

            return {
                'temperature':temperature,
                'location':'Dubai',
                'condition':'Clear'
            }
        except Exception as e:
            _logger.error(f"error fetching weather data {str(e)}")
            return None