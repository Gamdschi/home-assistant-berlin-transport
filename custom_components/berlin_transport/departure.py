from dataclasses import dataclass
from datetime import datetime

from .const import TRANSPORT_TYPE_VISUALS, DEFAULT_ICON


@dataclass
class Departure:
    """Departure dataclass to store data from API:
    https://v6.vbb.transport.rest/api.html#get-stopsiddepartures"""

    trip_id: str
    line_name: str
    line_type: str
    timestamp: datetime
    time: datetime
    direction: str | None = None
    icon: str | None = None
    bg_color: str | None = None
    fallback_color: str | None = None
    location: tuple[float, float] | None = None
    cancelled: bool = False

    @classmethod
    def from_dict(cls, source):
        line_type = source.get("line", {}).get("product")
        line_visuals = TRANSPORT_TYPE_VISUALS.get(line_type) or {}
        timestamp=datetime.fromisoformat(source.get("when") or source.get("plannedWhen"))
        return cls(
            trip_id=source["tripId"],
            line_name=source.get("line", {}).get("name"),
            line_type=line_type,
            timestamp=timestamp,
            time=timestamp.strftime("%H:%M"),
            direction=source.get("direction"),
            icon=line_visuals.get("icon") or DEFAULT_ICON,
            bg_color=source.get("line", {}).get("color", {}).get("bg"),
            fallback_color=line_visuals.get("color"),
            location=[
                source.get("currentTripPosition", {}).get("latitude") or 0.0,
                source.get("currentTripPosition", {}).get("longitude") or 0.0,
            ],
            cancelled=source.get("cancelled", False),
        )

    def to_dict(self):
        return {
            "line_name": self.line_name,
            "line_type": self.line_type,
            "time": self.time,
            "direction": self.direction,
            "color": self.fallback_color or self.bg_color,
            "cancelled": self.cancelled,
        }
