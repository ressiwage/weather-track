from typing import Any
from dataclasses import dataclass
import requests, json



@dataclass
class Condition:
    text: str
    icon: str
    code: int

    @staticmethod
    def from_dict(obj: Any) -> 'Condition':
        _text = str(obj.get("text"))
        _icon = str(obj.get("icon"))
        _code = int(obj.get("code"))
        return Condition(_text, _icon, _code)

@dataclass
class Current:
    last_updated_epoch: int
    last_updated: str
    temp_c: float
    temp_f: float
    is_day: int
    condition: Condition
    wind_mph: float
    wind_kph: float
    wind_degree: int
    wind_dir: str
    pressure_mb: float
    pressure_in: float
    precip_mm: float
    precip_in: float
    humidity: int
    cloud: int
    feelslike_c: float
    feelslike_f: float
    vis_km: float
    vis_miles: float
    uv: float
    gust_mph: float
    gust_kph: float

    @staticmethod
    def from_dict(obj: Any) -> 'Current':
        _last_updated_epoch = int(obj.get("last_updated_epoch"))
        _last_updated = str(obj.get("last_updated"))
        _temp_c = float(obj.get("temp_c"))
        _temp_f = float(obj.get("temp_f"))
        _is_day = int(obj.get("is_day"))
        _condition = Condition.from_dict(obj.get("condition"))
        _wind_mph = float(obj.get("wind_mph"))
        _wind_kph = float(obj.get("wind_kph"))
        _wind_degree = int(obj.get("wind_degree"))
        _wind_dir = str(obj.get("wind_dir"))
        _pressure_mb = float(obj.get("pressure_mb"))
        _pressure_in = float(obj.get("pressure_in"))
        _precip_mm = float(obj.get("precip_mm"))
        _precip_in = float(obj.get("precip_in"))
        _humidity = int(obj.get("humidity"))
        _cloud = int(obj.get("cloud"))
        _feelslike_c = float(obj.get("feelslike_c"))
        _feelslike_f = float(obj.get("feelslike_f"))
        _vis_km = float(obj.get("vis_km"))
        _vis_miles = float(obj.get("vis_miles"))
        _uv = float(obj.get("uv"))
        _gust_mph = float(obj.get("gust_mph"))
        _gust_kph = float(obj.get("gust_kph"))
        return Current(_last_updated_epoch, _last_updated, _temp_c, _temp_f, _is_day, _condition, _wind_mph, _wind_kph, _wind_degree, _wind_dir, _pressure_mb, _pressure_in, _precip_mm, _precip_in, _humidity, _cloud, _feelslike_c, _feelslike_f, _vis_km, _vis_miles, _uv, _gust_mph, _gust_kph)

@dataclass
class Location:
    name: str
    region: str
    country: str
    lat: float
    lon: float
    tz_id: str
    localtime_epoch: int
    localtime: str

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        _name = str(obj.get("name"))
        _region = str(obj.get("region"))
        _country = str(obj.get("country"))
        _lat = float(obj.get("lat"))
        _lon = float(obj.get("lon"))
        _tz_id = str(obj.get("tz_id"))
        _localtime_epoch = int(obj.get("localtime_epoch"))
        _localtime = str(obj.get("localtime"))
        return Location(_name, _region, _country, _lat, _lon, _tz_id, _localtime_epoch, _localtime)

@dataclass
class Root:
    location: Location
    current: Current

    @staticmethod
    def from_dict(obj: Any) -> 'Root':
        _location = Location.from_dict(obj.get("location"))
        _current = Current.from_dict(obj.get("current"))
        return Root(_location, _current)

# Example Usage
# jsonstring = json.loads(myjsonstring)
# root = Root.from_dict(jsonstring)

def get_current():
    r = requests.get(r"http://api.weatherapi.com/v1/current.json?key=738a432fd9cc4ca29e9103506220408&q=Perm").content
    jsonstring = json.loads(r)
    root = Root.from_dict(jsonstring)
    
    print("\n\n\n", root)
    return {
        "weather":root.current.condition.icon,
        "temperature":root.current.temp_c,
        "humidity":root.current.humidity,
        "weather_text":root.current.condition.text
    }