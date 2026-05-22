from __future__ import annotations

from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

SurfaceType = Literal[
    "homepage", "pricing", "product", "positioning", "blog", "changelog"
]
ChangeKind = Literal["added", "removed", "modified"]
ChangeType = Literal[
    "feature_ship",
    "pricing_move",
    "positioning_shift",
    "content_angle",
    "design_only",
    "noise",
]


class Surface(BaseModel):
    url: str
    type: SurfaceType
    competitor: str


class FetchResult(BaseModel):
    surface: Surface
    content_md: Optional[str] = None
    fetched_at: datetime
    status: Literal["ok", "fetch_failed"] = "ok"
    error: Optional[str] = None


class DiffChunk(BaseModel):
    id: str
    competitor: str
    url: str
    surface_type: SurfaceType
    kind: ChangeKind
    text: str


class Classification(BaseModel):
    id: str
    change_type: ChangeType
    significance: int = Field(ge=1, le=5)
    reason: str


class SignificantChange(BaseModel):
    """A diff chunk that passed the classification filter."""

    competitor: str
    url: str
    surface_type: SurfaceType
    change_type: ChangeType
    significance: int
    reason: str
    text: str
