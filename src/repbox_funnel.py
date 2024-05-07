"""Module providing parts for a repbox filament funnel and external fitting."""
from math import sqrt
from configparser import ConfigParser
from bd_warehouse.thread import TrapezoidalThread
from build123d import (BuildPart, BuildSketch, Part, loft,
                       Circle, Plane, RegularPolygon, fillet,
                       vertices, extrude, chamfer, Text,
                       Mode, Location, Locations, revolve, CounterSinkHole,
                       Align, GeomType, SortBy, Axis, export_step, export_stl, add)
from ocp_vscode import show

REVISION_TEXT = "R1.0"

config=ConfigParser()
config.read('settings.ini')
connector_depth = config.getfloat('connector','depth',fallback=6.5)
connector_diameter = config.getfloat('connector', 'diameter', fallback=10.1)
connector_pitch = config.getfloat('connector', 'pitch', fallback=0.874)

shaft_length = config.getfloat('shaft', 'length', fallback=20)
shaft_diameter = config.getfloat('shaft', 'diameter', fallback=11.5)

bend_angle = config.getfloat('bend', 'angle', fallback=10)

fitting_diameter = config.getfloat('fitting', 'diameter', fallback=17.5)
fitting_depth = config.getfloat('fitting', 'depth', fallback=4.5)
fitting_pitch = config.getfloat('fitting', 'pitch', fallback=1.25 )
fitting_tolerance = config.getfloat('fitting', 'tolerance', fallback=0.5)

hex_diameter = config.getfloat('fitting', 'hex_diameter', fallback=21)
hex_depth = config.getfloat('fitting', 'hex_depth', fallback=5)

funnel_length = config.getfloat('funnel', 'length', fallback=40)
funnel_top_scale = config.getfloat('funnel', 'top_scale', fallback=1.5)

tube_outer_diameter = config.getfloat('tube', 'outer_diameter', fallback=6.5)
tube_inner_diameter = config.getfloat('tube', 'inner_diameter', fallback=3.5)

font_path = config.get('general', 'font-path', fallback='C:\\Windows\\Fonts\\arial.ttf')

def cone_funnel(lower_radius=10, upper_radius=20, inner_radius=5, height=30, minimum_wall=0):
    """Function generating a round funnel."""
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
    return funnel

def hex_funnel(lower_radius=10, upper_radius=20, inner_radius=5, height=30, minimum_wall=0):
    """Function generating a hexagonal funnel."""
    with BuildPart() as outer_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))):
            RegularPolygon(radius=lower_radius, side_count=6)
            fillet(vertices(), radius=lower_radius/4)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1))):
            RegularPolygon(radius=upper_radius, side_count=6)
            fillet(vertices(), radius=upper_radius/4)
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
    return funnel

def socket_base(chamfer_thread=True):
    """Function generating the socket base -- a hexagonal nut with a revision label."""
    with BuildPart() as base_part:
        with BuildSketch():
            RegularPolygon(radius=hex_diameter/2, side_count=6)
            Circle((shaft_diameter+fitting_tolerance)/2, mode=Mode.SUBTRACT)
        extrude(amount=shaft_length)
        if chamfer_thread:
            chamfer(
                base_part.edges()
                .filter_by(GeomType.CIRCLE)
                .sort_by(SortBy.RADIUS)
                .sort_by(Axis.Z)[0],
                length=fitting_pitch/2,
                )
        fillet(base_part.edges().filter_by(Axis.Z), radius=hex_diameter/7)
        with BuildSketch(base_part.faces().sort_by(Axis.Y)[0]):
            Text(
                REVISION_TEXT,
                font_path=font_path,
                font_size=3,
                align=(Align.CENTER, Align.CENTER)
                )
        extrude(amount=-.4, mode=Mode.SUBTRACT)
    return base_part.part

def bend():
    """Function generating the transitional bend with a path to bend the PTFE tube."""
    with BuildPart() as bend_part:
        with BuildSketch():
            with Locations((0, connector_diameter*2)):
                RegularPolygon(radius=hex_diameter/2, side_count=6)
                fillet(vertices(), radius=hex_diameter/8)
                Circle(tube_outer_diameter/2, mode=Mode.SUBTRACT)
        revolve(axis=Axis.X, revolution_arc=bend_angle)
    return bend_part.part.moved(Location((0,connector_diameter*-2,0)))

def build_external_fitting():
    """Function generating the complete external fitting."""
    chamfer_radius = (shaft_diameter-tube_outer_diameter)/8
    fitting_nut_thread =  TrapezoidalThread(
        diameter=connector_diameter,
        pitch=connector_pitch,
        length=connector_depth-connector_pitch/2,
        thread_angle = 30.0,
        external=False,
        hand="right",
        align=Align.CENTER,
        ).moved(Location((0,0,connector_pitch/2)))

    shaft_thread =  TrapezoidalThread(
        diameter=shaft_diameter,
        pitch=fitting_pitch,
        length=shaft_length-fitting_depth-chamfer_radius,
        thread_angle = 30.0,
        external=True,
        interference=fitting_tolerance,
        end_finishes=("square","chamfer"),
        hand="right",
        align=Align.CENTER,
        ).moved(Location((0,0,connector_depth+fitting_depth)))

    with BuildPart() as outer_fitting:
        with BuildSketch():
            RegularPolygon(radius=fitting_diameter/2, side_count=6)
        extrude(amount=connector_depth)
        with BuildSketch(outer_fitting.faces().sort_by(Axis.Y)[0]):
            Text(
                REVISION_TEXT,
                font_path=font_path,
                font_size=3,
                align=(Align.CENTER, Align.CENTER)
                )
        extrude(amount=-.4, mode=Mode.SUBTRACT)
        with Locations(outer_fitting.faces().sort_by(Axis.Z)[0]):
            CounterSinkHole(
                radius=connector_diameter/2,
                counter_sink_radius=connector_diameter/2+connector_pitch/2
                )
        with BuildSketch(outer_fitting.faces().sort_by(Axis.Z)[-1]):
            Circle(shaft_diameter/2)
            Circle(tube_outer_diameter/2, mode=Mode.SUBTRACT)
        extrude(amount=fitting_depth)
        with BuildSketch(outer_fitting.faces().sort_by(Axis.Z)[-1]):
            Circle(shaft_diameter/2-1)
            Circle(tube_outer_diameter/2, mode=Mode.SUBTRACT)
        extrude(amount=shaft_length-fitting_depth)
        chamfer(
            outer_fitting.edges()
            .filter_by(GeomType.CIRCLE)
            .sort_by(SortBy.RADIUS)
            .sort_by(Axis.Z)[-1],
            length=chamfer_radius,
        )
    return Part(children=[outer_fitting.part, fitting_nut_thread, shaft_thread])

def build_internal_fitting():
    """Function generating the assembled internal filament funnel."""
    fitting_nut_thread =  TrapezoidalThread(
        diameter=shaft_diameter+fitting_tolerance,
        pitch=fitting_pitch,
        length=shaft_length,
        thread_angle = 30.0,
        external=False,
        end_finishes=("square","square"),
        hand="right",
        align=Align.CENTER,
        )

    with BuildPart() as inner_fitting:
        with BuildPart() as socket_base_part:
            add(socket_base(chamfer_thread=False))
        with BuildPart(socket_base_part.faces().sort_by(Axis.Z)[-1]) as bend_part:
            add(bend())
        with BuildPart(bend_part.faces().sort_by(Axis.Z)[-1]):
            add(hex_funnel(
                lower_radius=shaft_diameter/2 + fitting_depth,
                upper_radius=(shaft_diameter/2 + fitting_depth) * funnel_top_scale,
                inner_radius=tube_inner_diameter/2,
                height=funnel_length,
                minimum_wall = 1.5,
                )
            )
    return Part(children=[inner_fitting.part, fitting_nut_thread])

external_fitting = build_external_fitting()
internal_fitting = build_internal_fitting()

show(internal_fitting)
#show(external_fitting)

#need to make sure the directories are there
export_stl(external_fitting, "../stl/outer-fitting.stl",tolerance=.0001)
export_stl(internal_fitting, "../stl/inner-funnel.stl",tolerance=.0001)

# export failing, restore when https://github.com/gumyr/build123d/issues/618 is resolved
# export_step(external_fitting, "../step/outer-fitting.step")
export_step(internal_fitting, "../step/inner-funnel.step")
