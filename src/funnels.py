"""Module providing parts for a cone funnel."""

from math import sqrt
from build123d import (BuildPart,BuildSketch,Plane,Circle,
    loft,Part,Compound, RegularPolygon, fillet,
    Axis)

def cone_funnel(lower_radius=10, upper_radius=20, inner_radius=5, height=30, minimum_wall=0):
    """
    Function generating a round funnel.
    
        Parameters:
            lower_radius (int): The radius for the base of the funnel
            upper_radius (int): The radius at the top of the funnel
            inner_radius (int): The radius for the inside hole of the funnel
            height (int): The length of the radius
            minimum_wall(int): The thickness of the wall at the top between the outer and inner edge of the funnel

        Returns:
            funnel (Compound): A cone shaped funnel 
    """
    with BuildPart() as outer_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))):
            Circle(lower_radius)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1))):
            Circle(upper_radius)
        loft()
    with BuildPart() as inner_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))):
            Circle(inner_radius)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1))):
            Circle(upper_radius-minimum_wall)
        loft()
    funnel = Part(outer_funnel.part - inner_funnel.part)
    if minimum_wall > 0:
        funnel = funnel.fillet(radius=minimum_wall/4, edge_list=funnel.edges().sort_by(Axis.Z)[-2:])
    return Compound(label="funnel", children=funnel)

def hex_funnel(lower_radius=10, upper_radius=20, inner_radius=5, height=30, minimum_wall=0):
    """
    Function generating a funnel with a hexagonal exterior and round interior.
    
        Parameters:
            lower_radius (int): The radius for the base of the funnel
            upper_radius (int): The radius at the top of the funnel
            inner_radius (int): The radius for the inside hole of the funnel
            height (int): The length of the radius
            minimum_wall(int): The thickness of the wall at the top between the outer and inner edge of the funnel

        Returns:
            funnel (Compound): A hexagon shaped funnel 
    """
    with BuildPart() as outer_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))) as lower_sketch:
            RegularPolygon(radius=lower_radius, side_count=6)
            fillet(lower_sketch.vertices(), radius=lower_radius/4)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1)))as upper_sketch:
            RegularPolygon(radius=upper_radius, side_count=6)
            fillet(upper_sketch.vertices(), radius=upper_radius/4)
        loft()

    with BuildPart() as inner_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))):
            Circle(inner_radius)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1))):
            Circle((upper_radius/2*sqrt(3))-minimum_wall)
        loft()
    funnel = Part(outer_funnel.part - inner_funnel.part)
    if minimum_wall > 0:
        wall_edges = funnel.edges().sort_by(Axis.Z)[-2:]
        max_fillet_radius = funnel.max_fillet(wall_edges,max_iterations=100)
        funnel = funnel.fillet(radius=max_fillet_radius, edge_list=wall_edges)
    return Compound(label="funnel", children=funnel)
