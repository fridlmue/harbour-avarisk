"""
    Copyright (C) 2021 Friedrich Mütschele and other contributors
    This file is part of pyAvaCore.
    pyAvaCore is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    pyAvaCore is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with pyAvaCore. If not, see <http://www.gnu.org/licenses/>.
"""

from datetime import date, datetime, timedelta
import typing
from .avabulletin import AvaBulletin, DangerRatingType
from .geojson import Feature, FeatureCollection


class Bulletins:
    """
    Class for the AvaBulletin collection
    Follows partly CAAMLv6 caaml:Bulletins
    """

    bulletins: typing.List[AvaBulletin]

    def main_date(self) -> date:
        validityDate: datetime = self.bulletins[0].validTime.startTime
        if validityDate.hour > 15:
            validityDate = validityDate + timedelta(days=1)
        return validityDate.date()


    def max_danger_ratings(self):
        ratings = dict()
        for bulletin in self.bulletins:
            for region in bulletin.regions:
                regionID = region.regionID
                for danger in bulletin.dangerRatings:
                    if (
                        Bulletins.region_without_elevation(regionID)
                        or not danger.elevation
                        or danger.elevation.toString() == ""
                        or danger.elevation.toString().startswith("<")
                    ):
                        pm = ''
                        if hasattr(bulletin, 'predecessor_id'):
                            pm = ':pm'
                            key = f"{regionID}:low"
                            ratings[f"{key}:am"] = ratings.pop(key)
                        key = f"{regionID}:low{pm}"
                        ratings[key] = max(
                            danger.get_mainValue_int(), ratings.get(key, 0)
                        )
                    if (
                        Bulletins.region_without_elevation(regionID)
                        or not danger.elevation
                        or danger.elevation.toString() == ""
                        or danger.elevation.toString().startswith(">")
                    ):
                        pm = ''
                        if hasattr(bulletin, 'predecessor_id'):
                            pm = ':pm'
                            key = f"{regionID}:high"
                            ratings[f"{key}:am"] = ratings.pop(key)
                        key = f"{regionID}:high{pm}"
                        ratings[key] = max(
                            danger.get_mainValue_int(), ratings.get(key, 0)
                        )

            for region in bulletin.regions:
                regionID = region.regionID
                sel_ratings = [value for key,value in ratings.items() if regionID in key]
                sel_keys = [key for key,value in ratings.items() if regionID in key]

                if not ('am' in sel_keys[0]) and not ('pm' in sel_keys[0]):
                    key = f"{regionID}:high"
                    ratings[f"{key}:am"] = ratings[key]
                    ratings[f"{key}:pm"] = ratings[key]
                    key = f"{regionID}:low"
                    ratings[f"{key}:am"] = ratings[key]
                    ratings[f"{key}:pm"] = ratings[key]
                
                key = f"{regionID}:high"
                if not key in sel_keys:
                    ratings[key] = max(ratings[f"{key}:am"], ratings[f"{key}:pm"])
                
                key = f"{regionID}:low"    
                if not key in sel_keys:
                    ratings[key] = max(ratings[f"{key}:am"], ratings[f"{key}:pm"])
                    
                key = regionID
                if not f"{key}:am" in sel_keys:
                    ratings[f"{key}:am"] = max(ratings[f"{key}:high:am"], ratings[f"{key}:low:am"])
                    
                if not f"{key}:pm" in sel_keys:
                    ratings[f"{key}:pm"] = max(ratings[f"{key}:high:pm"], ratings[f"{key}:low:pm"])
                    
                if not key in sel_keys:
                    ratings[key] = max(sel_ratings)

        # return 0 independent of "no_snow" or "no_rating"
        for key, value in ratings.items():
            if value == -1:
                ratings[key] = 0

        return ratings

    def augment_geojson(self, geojson: FeatureCollection):
        for feature in geojson.features:
            self.augment_feature(feature)

    def augment_feature(self, feature: Feature):
        id = feature.properties.id
        elevation = feature.properties.elevation

        def affects_region(b: AvaBulletin):
            return id in [r.regionID for r in b.regions]

        def affects_danger(d: DangerRatingType):
            if Bulletins.region_without_elevation(id):
                return True
            elif not d.elevation:
                return True
            elif not (
                hasattr(d.elevation, "lowerBound") or hasattr(d.elevation, "upperBound")
            ):
                return True
            elif hasattr(d.elevation, "upperBound") and elevation == "low":
                return True
            elif hasattr(d.elevation, "lowerBound") and elevation == "high":
                return True
            else:
                return False

        bulletins = [b for b in self.bulletins if affects_region(b)]
        dangers = [
            d.get_mainValue_int()
            for b in bulletins
            for d in b.dangerRatings
            if affects_danger(d)
        ]
        if not dangers:
            return
        feature.properties.max_danger_rating = max(dangers)

    @staticmethod
    def region_without_elevation(id: str):
        return (
            id.startswith("CH-")
            or id.startswith("IT-21-")
            or id.startswith("IT-23-")
            or id.startswith("IT-25-")
            or id.startswith("IT-34-")
            or id.startswith("IT-36-")
            or id.startswith("IT-57-")
            or id.startswith("FR-")
        )
