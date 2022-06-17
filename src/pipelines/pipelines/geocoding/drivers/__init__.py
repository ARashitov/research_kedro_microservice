from .geodata_gov_hk import GeodataGovHK
from .google_map import GoogleMap


registry = {
    "google_map": GoogleMap,
    "geodata_gov_hk": GeodataGovHK,
}
