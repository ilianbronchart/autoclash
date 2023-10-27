from typing import Any
from pydantic import BaseModel


class Rect(BaseModel):
    x: int
    y: int
    w: int
    h: int


    def __iter__(self):
        yield self.x
        yield self.y
        yield self.w
        yield self.h


    def __repr__(self):
        return f"Rect(x={self.x}, y={self.y}, w={self.w}, h={self.h})"
    

    def close_to(self, other: 'Rect', threshold_x, y_overlap_ratio: float = 0.8) -> bool:
        x_close = (self.x - threshold_x <= other.x + other.w <= self.x + self.w + threshold_x) or \
                (other.x - threshold_x <= self.x + self.w <= other.x + other.w + threshold_x)

        y_overlap = (max(self.y, other.y) <= min(self.y + self.h, other.y + other.h))
        y_overlap_length = min(self.y + self.h, other.y + other.h) - max(self.y, other.y)
        
        self_height = self.h
        other_height = other.h
        
        y_overlap_ratio_actual = y_overlap_length / min(self_height, other_height)

        return x_close and y_overlap and y_overlap_ratio_actual >= y_overlap_ratio


    def merge(self, other: 'Rect') -> 'Rect':
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        w = max(self.x + self.w, other.x + other.w) - x
        h = max(self.y + self.h, other.y + other.h) - y

        return Rect(x=x, y=y, w=w, h=h)


class TextRect(BaseModel):
    text: str
    rect: Rect
    img: Any
