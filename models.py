"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from typing import Optional, Dict, Union

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, pha: bool, pdes: str = '', name: Optional[str] = None, diameter: float = float('nan')):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self.designation = pdes
        self.name = name
        self.diameter = float(diameter)
        self.hazardous = pha
        self.approaches = []

    @property
    def fullname(self) -> str:
        """Return a representation of the full name of this NEO."""
        if self.name:
            return f"{self.designation} {self.name}"
        else:
            return self.designation

    def __str__(self) -> str:
        """Return `str(self)`."""
        hazardous_str = 'is' if self.hazardous else 'is not'
        return f"NEO {self.fullname} has a diameter of {self.diameter:.3f} km and {hazardous_str} potentially hazardous."

    def __repr__(self) -> str:
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(hazardous={self.hazardous!r}, pdes={self.designation!r}, name={self.name!r}, diameter={self.diameter:.3f})"

    def serialize(self) -> Dict[str, Union[str, float, bool]]:
        """Return serialize NEO's object."""
        return {
            "designation": self.designation,
            "name": self.name,
            "diameter_km": self.diameter,
            "potentially_hazardous": self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, des='', cd=None, dist=0.0, v_rel=0.0) -> None:
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = des
        self.time = cd_to_datetime(cd) if bool(cd) else None
        self.distance = float(dist)
        self.velocity = float(v_rel)
        self.neo = None

    @property
    def time_str(self) -> str:
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time) if bool(self.time) else ""

    def __str__(self) -> str:
        """
        Return a string representation of the CloseApproach.

        Returns:
            str: A string representation of the CloseApproach.
        """
        return f"At {self.time_str}, '{self.neo.fullname!r}' approaches Earth at a distance of {self.distance:.2f} au and a velocity of {self.velocity:.2f} km/s"

    def __repr__(self) -> str:
        """
        Return a string representation of the CloseApproach.

        Returns:
            str: A string representation of the CloseApproach.
        """
        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def serialize(self, isCsv=False) -> Dict[str, Union[str, float, bool]]:
        """
        Return a dictionary representation of the CloseApproach.

        Args:
            isCsv (bool): Whether or not to include NEO data in the output.

        Returns:
            dict: A dictionary representation of the CloseApproach.
        """
        serialized_result = {
            "datetime_utc": self.time_str,
            "distance_au": self.distance,
            "velocity_km_s": self.velocity,
        }
        serialized_neo = self.neo.serialize()
        if isCsv:
            serialized_result = {**serialized_result, **serialized_neo}
        else:
            serialized_result["neo"] = serialized_neo
        return serialized_result
