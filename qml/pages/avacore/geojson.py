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

# Generated using https://app.quicktype.io/
from typing import Optional, List, Any, TypeVar, Callable, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    assert isinstance(x, float)
    return x


def to_float_coordinate(x: Any) -> float:
    assert isinstance(x, float)
    return round(x, 4)


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Geometry:
    type: Optional[str]
    coordinates: Optional[List[List[List[List[float]]]]]

    def __init__(self, type: Optional[str], coordinates: Optional[List[List[List[List[float]]]]]) -> None:
        self.type = type
        self.coordinates = coordinates

    @staticmethod
    def from_dict(obj: Any) -> 'Geometry':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        coordinates = from_union([lambda x: from_list(lambda x: from_list(lambda x: from_list(lambda x: from_list(from_float, x), x), x), x), from_none], obj.get("coordinates"))
        return Geometry(type, coordinates)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["coordinates"] = from_union([lambda x: from_list(lambda x: from_list(lambda x: from_list(lambda x: from_list(to_float_coordinate, x), x), x), x), from_none], self.coordinates)
        return result


class Properties:
    threshold: None
    id: Optional[str]
    elevation: Optional[str]
    max_danger_rating: Optional[int]

    def __init__(self, threshold: None, id: Optional[str], elevation: Optional[str], max_danger_rating: Optional[int]) -> None:
        self.threshold = threshold
        self.id = id
        self.elevation = elevation
        self.max_danger_rating = max_danger_rating

    @staticmethod
    def from_dict(obj: Any) -> 'Properties':
        assert isinstance(obj, dict)
        threshold = from_none(obj.get("threshold"))
        id = from_union([from_str, from_none], obj.get("id"))
        elevation = from_union([from_str, from_none], obj.get("elevation"))
        max_danger_rating = from_union([from_int, from_none], obj.get("maxDangerRating"))
        return Properties(threshold, id, elevation, max_danger_rating)

    def to_dict(self) -> dict:
        result: dict = {}
        result["threshold"] = from_none(self.threshold)
        result["id"] = from_union([from_str, from_none], self.id)
        result["elevation"] = from_union([from_str, from_none], self.elevation)
        result["maxDangerRating"] = from_union([from_int, from_none], self.max_danger_rating)
        return result


class Feature:
    type: Optional[str]
    properties: Optional[Properties]
    geometry: Optional[Geometry]

    def __init__(self, type: Optional[str], properties: Optional[Properties], geometry: Optional[Geometry]) -> None:
        self.type = type
        self.properties = properties
        self.geometry = geometry

    @staticmethod
    def from_dict(obj: Any) -> 'Feature':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        properties = from_union([Properties.from_dict, from_none], obj.get("properties"))
        geometry = from_union([Geometry.from_dict, from_none], obj.get("geometry"))
        return Feature(type, properties, geometry)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["properties"] = from_union([lambda x: to_class(Properties, x), from_none], self.properties)
        result["geometry"] = from_union([lambda x: to_class(Geometry, x), from_none], self.geometry)
        return result


class FeatureCollection:
    type: Optional[str]
    features: Optional[List[Feature]]

    def __init__(self, type: Optional[str], features: Optional[List[Feature]]) -> None:
        self.type = type
        self.features = features

    @staticmethod
    def from_dict(obj: Any) -> 'FeatureCollection':
        assert isinstance(obj, dict)
        type = from_union([from_str, from_none], obj.get("type"))
        features = from_union([lambda x: from_list(Feature.from_dict, x), from_none], obj.get("features"))
        return FeatureCollection(type, features)

    def to_dict(self) -> dict:
        result: dict = {}
        result["type"] = from_union([from_str, from_none], self.type)
        result["features"] = from_union([lambda x: from_list(lambda x: to_class(Feature, x), x), from_none], self.features)
        return result
