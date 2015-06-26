# Copyright 2015 Florian Tautz
# see LICENSE in the project root for licensing information

from math import radians, acos, sin, cos


class GeoLocation(object):
    def __init__(self, lat, lon, data=None):
        self.lat = lat
        self.lon = lon
        self.data = data

    def distance_to(self, other):
        if other is None:
            return float('inf')
        if abs(self.lat - other.lat) < 1e-9 and abs(self.lon - other.lon) < 1e-9:
            return 0.0
        rlat1 = radians(self.lat)
        rlat2 = radians(other.lat)
        rtheta = radians(self.lon - other.lon)
        try:
            phi = acos(sin(rlat1) * sin(rlat2) +
                       cos(rlat1) * cos(rlat2) * cos(rtheta))
        except ValueError:
            return 0.0
        return phi * 6371009  # earth radius

    @staticmethod
    def mean(locations):
        lat, lon = 0.0, 0.0
        for loc in locations:
            lat += loc.lat
            lon += loc.lon
        lat /= len(locations)
        lon /= len(locations)
        return GeoLocation(lat, lon)


def simplify_track(positions):
    locations = [GeoLocation(tp.latitude, tp.longitude, tp) for tp in positions]
    removed = []
    for epsilon in [3.0, 5.0, 5.0]:
        locations, _removed = _simplify(locations, epsilon)
        removed += _removed
    return [[loc.data for loc in locs] for locs in [locations, removed]]


def _simplify(locations, epsilon):
    keep, remove = [], []

    group = [locations[0]]
    for loc in locations[1:]:
        group_mean = GeoLocation.mean(group)
        if group_mean.distance_to(loc) >= epsilon:
            tp_keep = group[0].data
            tp_keep.latitude = group_mean.lat
            tp_keep.longitude = group_mean.lon
            keep.append(group[0])
            remove += group[1:]
            group = []
        group.append(loc)

    # merge last group into last point
    group_mean = GeoLocation.mean(group)
    tp_keep = group[-1].data
    tp_keep.latitude = group_mean.lat
    tp_keep.longitude = group_mean.lon
    keep.append(group[-1])
    remove += group[:-1]

    return keep, remove
