"""Fixed version of upstream `polygons.py`.

Original issues included inheriting from undefined `Object`, using `new`, hard
coded polygon formulas, fixed six-sided drawing, and import-time prompts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Polygon:
    """Details for a regular polygon."""

    sides: int
    internal_angles_sum: int
    internal_angle: float
    exterior_angle: float


def calc_polygon_details(sides: int) -> Polygon:
    """Calculate angle information for a regular polygon."""
    if sides < 3:
        raise ValueError("a polygon must have at least 3 sides")
    internal_angles_sum = (sides - 2) * 180
    internal_angle = internal_angles_sum / sides
    exterior_angle = 360 / sides
    return Polygon(sides, internal_angles_sum, internal_angle, exterior_angle)


def polygon_as_dict(polygon: Polygon) -> dict[str, float | int]:
    """Return dictionary output compatible with the original script."""
    return {
        "sides": polygon.sides,
        "internal_angles_sum": polygon.internal_angles_sum,
        "internal_angles": polygon.internal_angle,
        "exterior_angle": polygon.exterior_angle,
    }


def draw_polygon(polygon: Polygon, turtle_module: Any | None = None, edge_length: int = 50) -> None:
    """Draw a regular polygon using turtle, with dependency injection for tests."""
    if turtle_module is None:
        import turtle as turtle_module
    screen = turtle_module.Screen()
    turtle = turtle_module.Turtle()
    turtle.pen(pencolor="red", pensize=2, fillcolor="green")
    for _ in range(polygon.sides):
        turtle.forward(edge_length)
        turtle.right(polygon.exterior_angle)
    if hasattr(screen, "exitonclick"):
        screen.exitonclick()


def main(input_fn=input, print_fn=print) -> Polygon:
    """Interactive entry point for the polygon script."""
    sides = int(input_fn("How many sides does your polygon have?: "))
    polygon = calc_polygon_details(sides)
    details = polygon_as_dict(polygon)
    print_fn("    Sides:", details["sides"])
    print_fn("    Internal angles sum:", details["internal_angles_sum"])
    print_fn("    Internal angles:", details["internal_angles"])
    draw = input_fn("Would you like me to draw it? (Y/n): ")
    if draw == "" or draw.lower() == "y":
        draw_polygon(polygon)
    return polygon


if __name__ == "__main__":
    main()
