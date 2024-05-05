from build123d import *
from ocp_vscode import *
from bd_warehouse.thread import  TrapezoidalThread
from math import sqrt
import json
from configparser import ConfigParser

config=ConfigParser()
config.read('settings.ini')
connector_depth = config.getfloat('connector','depth',fallback=6.5)
connector_diameter = config.getfloat('connector', 'diameter', fallback=10.1)
connector_pitch = config.getfloat('connector', 'pitch', fallback=0.874)

shaft_length = config.getfloat('shaft', 'length', fallback=20)
shaft_diameter = config.getfloat('shaft', 'diameter', fallback=12.5)

bend_angle = config.getfloat('bend', 'angle', fallback=10)

fitting_diameter = config.getfloat('fitting', 'diameter', fallback=17.5)
fitting_depth = config.getfloat('fitting', 'depth', fallback=4.5)
fitting_pitch = config.getfloat('fitting', 'pitch', fallback=2)

funnel_length = config.getfloat('funnel', 'length', fallback=40)
funnel_top_scale = config.getfloat('funnel', 'top_scale', fallback=1.5)

tube_outer_diameter = config.getfloat('tube', 'outer_diameter', fallback=6.5)
tube_inner_diameter = config.getfloat('tube', 'inner_diameter', fallback=3.5)

def ConeFunnel(lower_radius=10, upper_radius=20, inner_radius=5, height=30, minimum_wall=0):
    with BuildPart() as outer_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))) as cone_base:
            Circle(lower_radius)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1))) as cone_top:
            Circle(upper_radius)
        loft()
    with BuildPart() as inner_funnel:
        with BuildSketch(Plane(origin=(0, 0,0), z_dir=(0, 0, 1))) as funnel_base:
            Circle(inner_radius)
        with BuildSketch(Plane(origin=(0, 0,height), z_dir=(0, 0, 1))) as funnel_top:
            Circle(upper_radius-minimum_wall)
        loft()
    
    funnel = Part(outer_funnel.part - inner_funnel.part)
    
    if minimum_wall > 0:
        funnel = funnel.fillet(radius=minimum_wall/3, edge_list=funnel.edges().sort_by(Axis.Z)[-2:])
    return funnel

def SocketBase():
    with BuildPart() as socket_base:
        with BuildSketch():
            Circle(shaft_diameter/2 + fitting_depth)
            Circle((shaft_diameter+fitting_pitch)/2, mode=Mode.SUBTRACT)
        extrude(amount=shaft_length)
        chamfer(
            socket_base.edges()
            .filter_by(GeomType.CIRCLE)
            .sort_by(SortBy.RADIUS)
            .sort_by(Axis.Z)[0],
            length=fitting_pitch/2,
            )
    return(socket_base.part)

def Bend():
    with BuildPart() as bend:
        with BuildSketch() as x2:
            with Locations((0, connector_diameter*2)):
                Circle(shaft_diameter/2 + fitting_depth)
                Circle(tube_outer_diameter/2, mode=Mode.SUBTRACT)
        revolve(axis=Axis.X, revolution_arc=bend_angle)    
    return bend.part.moved(Location((0,-connector_diameter*2,0)))

def BuildExternalFitting():
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
        length=shaft_length-fitting_depth-(shaft_diameter-tube_outer_diameter)/8,
        thread_angle = 30.0,
        external=True,
        end_finishes=("square","chamfer"),
        hand="right",
        align=Align.CENTER,
        ).moved(Location((0,0,connector_depth+fitting_depth)))

    with BuildPart() as outer_fitting:
        with BuildSketch():
            RegularPolygon(radius=fitting_diameter/2, side_count=6)
        extrude(amount=connector_depth)
        with Locations(outer_fitting.faces().sort_by(Axis.Z)[0]):
            CounterSinkHole(radius=connector_diameter/2, counter_sink_radius=connector_diameter/2+connector_pitch/2)
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
            length=(shaft_diameter-tube_outer_diameter)/8,
        )
        
    return Part(children=[outer_fitting.part, fitting_nut_thread,shaft_thread])

def BuildInternalFitting():
    fitting_nut_thread =  TrapezoidalThread(
        diameter=shaft_diameter+fitting_pitch,
        pitch=fitting_pitch,
        length=shaft_length-fitting_pitch/2,
        thread_angle = 30.0,
        external=False,
        hand="right",
        align=Align.CENTER,
        ).moved(Location((0,0,fitting_pitch/2)))

    with BuildPart() as inner_fitting:
        with BuildPart() as socket_base:
            add(SocketBase())
        with BuildPart(socket_base.faces().sort_by(Axis.Z)[-1]) as bend:
            add(Bend())
        with BuildPart(bend.faces().sort_by(Axis.Z)[-1]) as funnel:
            add(ConeFunnel(
                lower_radius=shaft_diameter/2 + fitting_depth, 
                upper_radius=(shaft_diameter/2 + fitting_depth) * funnel_top_scale, 
                inner_radius=tube_inner_diameter/2,
                height=funnel_length,
                minimum_wall = 1,
                )
            )
    return Part(children=[inner_fitting.part, fitting_nut_thread])


external_fitting = BuildExternalFitting()
internal_fitting = BuildInternalFitting()           

show(internal_fitting)
#show(external_fitting)

export_stl(external_fitting, "../stls/outer-fitting.stl",tolerance=.0005)
export_stl(internal_fitting, "../stls/inner-funnel.stl",tolerance=.0005)
