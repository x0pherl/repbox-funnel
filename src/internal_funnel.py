"""Module providing parts for a repbox filament funnel and external fitting."""
from configparser import ConfigParser
from bd_warehouse.thread import TrapezoidalThread
from build123d import (BuildPart, BuildSketch,
                       Circle, RegularPolygon,
                       extrude, chamfer, Text, Compound,
                       Mode, Location, Locations,
                       Align, GeomType, SortBy, Axis, export_step, 
                       export_stl, revolve, fillet, vertices, add)
from ocp_vscode import show
from funnels import hex_funnel

REVISION_TEXT = "R1.0"

"""

"""
class InternalFunnel:
    def __init__(self, config_file):
        """
        Initialize the InternalFitting by loading a configuration file.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config = ConfigParser()
        self.load_config(config_file)

    def load_config(self, config_file):
        """
        Update config values by loading a configuration file.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config.read(config_file)

    @property
    def shaft_length(self):
        """
        Get the shaft length.

        Returns:
            float: The length of the shaft.
        """
        return self.config.getfloat('shaft', 'length', fallback=20)

    @shaft_length.setter
    def shaft_length(self, value):
        """
        Set the shaft length.

        Args:
            float: The length of the shaft.
        """
        self.config.set('shaft', 'length', str(value))

    @property
    def shaft_diameter(self):
        """
        Get the shaft diameter.

        Returns:
            float: The diameter of the shaft.
        """
        return self.config.getfloat('shaft', 'diameter', fallback=11.5)

    @shaft_diameter.setter
    def shaft_diameter(self, value):
        """
        Set the shaft diameter.

        Args:
            float: The diameter of the shaft.
        """
        self.config.set('shaft', 'diameter', str(value))

    @property
    def shaft_interference(self):
        """
        Get the shaft thread interference.

        Returns:
            float: The interference of the shaft thread.
        """
        return self.config.getfloat('shaft', 'interference', fallback=0.5)

    @shaft_interference.setter
    def shaft_interference(self, value):
        """
        Set the shaft thread interference. This is the
        amount the thread will overlap with the shaft. 
        Ajust if the threads don't seem properly fused 
        to the shaft. 

        Args:
            float: The interference of the shaft thread.
        """
        self.config.set('shaft', 'interference', str(value))

    @property
    def bend_angle(self):
        """
        Get the angle at which the funnel is bent.

        Returns:
            float: The angle at which the funnel is bent.
        """
        return self.config.getfloat('bend', 'angle', fallback=10)

    @property
    def connector_depth(self):
        """
        Get the depth of the connector.

        Returns:
            float: The depth of the connector.
        """
        return self.config.getfloat('connector', 'depth', fallback=6.5)

    @connector_depth.setter
    def connector_depth(self, value):
        """
        Set the depth of the connector.

        Args:
            float: The depth of the connector.
        """
        self.config.set('connector', 'depth', str(value))

    @property
    def connector_diameter(self):
        """
        Get the diameter of the connector.

        Returns:
            float: The diameter of the connector.
        """
        return self.config.getfloat('connector', 'diameter', fallback=10.1)

    @connector_diameter.setter
    def connector_diameter(self, value):
        """
        Set the diameter of the connector.

        Args:
            float: The diameter of the connector.
        """
        self.config.set('connector', 'diameter', str(value))

    @property
    def connector_pitch(self):
        """
        Get the pitch of the connector.

        Returns:
            float: The pitch of the connector.
        """
        return self.config.getfloat('connector', 'pitch', fallback=0.874)

    @connector_pitch.setter
    def connector_pitch(self, value):
        """
        Set the pitch of the connector.

        Args:
            float: The pitch of the connector.
        """
        self.config.set('connector', 'pitch', str(value))

    @property
    def fitting_diameter(self):
        """
        Get the diameter of the fitting.

        Returns:
            float: The diameter of the fitting.
        """
        return self.config.getfloat('fitting', 'diameter', fallback=17.5)

    @fitting_diameter.setter
    def fitting_diameter(self, value):
        """
        Set the diameter of the fitting.

        Args:
            float: The diameter of the fitting.
        """
        self.config.set('fitting', 'diameter', str(value))

    @property
    def fitting_depth(self):
        """
        Get the depth of the fitting.

        Returns:
            float: The depth of the fitting.
        """
        return self.config.getfloat('fitting', 'depth', fallback=4.5)

    @fitting_depth.setter
    def fitting_depth(self, value):
        """
        Set the depth of the fitting.

        Args:
            float: The depth of the fitting.
        """
        self.config.set('fitting', 'depth', str(value))

    @property
    def fitting_pitch(self):
        """
        Get the pitch of the fitting threads.

        Returns:
            float: The pitch of the fitting threads.
        """
        return self.config.getfloat('fitting', 'pitch', fallback=1.25)

    @fitting_pitch.setter
    def fitting_pitch(self, value):
        """
        Set the pitch of the fitting threads.

        Args:
            float: The pitch of the fitting threads.
        """
        self.config.set('fitting', 'pitch', str(value))

    @property
    def fitting_tolerance(self):
        """
        Get the tolerance of the fitting threads.

        Returns:
            float: The tolerance of the fitting threads.
        """
        return self.config.getfloat('fitting', 'tolerance', fallback=0.5)

    @fitting_tolerance.setter
    def fitting_tolerance(self, value):
        """
        Set the tolerance of the fitting threads.

        Args:
            float: The tolerance of the fitting threads.
        """
        self.config.set('fitting', 'tolerance', str(value))

    @property
    def funnel_length(self):
        """
        Get the length of the funnel.

        Returns:
            float: The length of the funnel.
        """
        return self.config.getfloat('funnel', 'length', fallback=40)

    @funnel_length.setter
    def funnel_length(self, value):
        """
        Set the length of the funnel.

        Args:
            float: The length of the funnel.
        """
        self.config.set('funnel', 'length', value)

    @property
    def funnel_top_scale(self):
        """
        Get the scale of the top of the funnel (A scale of 2 would mean that the top
        of the funnel is 2x larger than the base).

        Returns:
            float: The scale of the top of the funnel.
        """
        return self.config.getfloat('funnel', 'top_scale', fallback=1.5)

    @funnel_top_scale.setter
    def funnel_top_scale(self, value):
        """
        Set the scale of the top of the funnel (A scale of 2 would mean that the top
        of the funnel is 2x larger than the base).

        Args:
            float: The scale of the top of the funnel.
        """
        return self.config.set('funnel', 'top_scale', value)

    @property
    def hex_diameter(self):
        """
        Get the diameter of the external hexagon.

        Returns:
            float: The diameter of the external hexagon.
        """
        return self.config.getfloat('fitting', 'hex_diameter', fallback=21)

    @hex_diameter.setter
    def hex_diameter(self, value):
        """
        Set the diameter of the external hexagon.

        Args:
            float: The diameter of the external hexagon.
        """
        self.config.set('fitting', 'hex_diameter', str(value))

    @property
    def hex_depth(self):
        """
        Get the depth of the external hexagon.

        Returns:
            float: The depth of the external hexagon.
        """
        return self.config.getfloat('fitting', 'hex_depth', fallback=5)

    @hex_depth.setter
    def hex_depth(self, value):
        """
        Set the depth of the external hexagon.

        Args:
            float: The depth of the external hexagon.
        """
        self.config.set('fitting', 'hex_depth', str(value))

    @property
    def tube_inner_diameter(self):
        """
        Get the inner diameter of the PTFE tube path. Note: this is the
        value as printed but tolerance is added in the calculated
        size of the tube path.

        Returns:
            float: The inner diameter of the PTFE tube path.
        """
        return self.config.getfloat('tube', 'inner_diameter', fallback=3)

    @tube_inner_diameter.setter
    def tube_inner_diameter(self, value):
        """
        Set the inner diameter of the PTFE tube path. Note: this is the
        value as printed but tolerance is added in the calculated
        inner diameter of the tube.

        Args:
            float: The inner diameter of the PTFE tube path.
        """
        self.config.set('tube', 'inner_diameter', str(value))

    @property
    def tube_inner_tolerance(self):
        """
        Get the inner tolerance of the PTFE tube path. This value is 
        added to the inner diameter in the calculated size of the 
        inner diameter of the tube.

        Returns:
            float: The inner tolerance for the PTFE tube path.
        """
        return self.config.getfloat('tube', 'inner_tolerance', fallback=0.4)

    @tube_inner_tolerance.setter
    def tube_inner_tolerance(self, value):
        """
        Set the inner tolerance of the PTFE tube path. This value is 
        added to the inner diameter in the calculated size of the 
        inner diameter of the tube.

        Args:
            float: The inner tolerance for the PTFE tube path.
        """
        self.config.set('tube', 'inner_tolerance', str(value))

    @property
    def tube_outer_diameter(self):
        """
        Get the diameter of the PTFE tube path. Note: this is the
        value as printed but tolerance is added in the calculated
        size of the tube path.

        Returns:
            float: The diameter of the PTFE tube path.
        """
        return self.config.getfloat('tube', 'outer_diameter', fallback=6)

    @tube_outer_diameter.setter
    def tube_outer_diameter(self, value):
        """
        Set the diameter of the PTFE tube path. Note: this is the
        value as printed but tolerance is added in the calculated
        size of the tube path.

        Args:
            float: The diameter of the PTFE tube path.
        """
        self.config.set('tube', 'outer_diameter', str(value))

    @property
    def tube_outer_tolerance(self):
        """
        Get the tolerance of the PTFE tube path. This value is 
        added to the diameter in the calculated size of the 
        tube path.

        Returns:
            float: The tolerance for the PTFE tube path.
        """
        return self.config.getfloat('tube', 'outer_tolerance', fallback=0.5)

    @tube_outer_tolerance.setter
    def tube_outer_tolerance(self, value):
        """
        Set the tolerance of the PTFE tube path. This value is 
        added to the diameter in the calculated size of the 
        tube path.

        Args:
            float: The tolerance for the PTFE tube path.
        """
        self.config.set('tube', 'outer_tolerance', str(value))

    @property
    def font_path(self):
        """
        Get the path of the configured font used for embossing labels.

        Returns:
            string: The path of the configured font used for embossing labels.
        """
        return self.config.get('general', 'font-path', fallback='C:\\Windows\\Fonts\\arial.ttf')

    @font_path.setter
    def font_path(self, value):
        """
        Sets the path of the configured font to the value provided. If the
        path is invalid, Arial will be used instead.

        Args:
            string: A path to a valid font.
        """
        self.config.set('general', 'font-path', value)

    def socket_base(self, chamfer_thread=True):
        """Function generating the socket base -- a hexagonal nut with a revision label."""
        with BuildPart() as base_part:
            with BuildSketch():
                RegularPolygon(radius=self.hex_diameter/2, side_count=6)
                Circle((self.shaft_diameter+self.fitting_tolerance)/2, mode=Mode.SUBTRACT)
            extrude(amount=self.shaft_length)
            if chamfer_thread:
                chamfer(
                    base_part.edges()
                    .filter_by(GeomType.CIRCLE)
                    .sort_by(SortBy.RADIUS)
                    .sort_by(Axis.Z)[0],
                    length=self.fitting_pitch/2,
                    )
            fillet(base_part.edges().filter_by(Axis.Z), radius=self.hex_diameter/7)
            with BuildSketch(base_part.faces().sort_by(Axis.Y)[-1]):
                Text(
                    REVISION_TEXT,
                    font_path=self.font_path,
                    font_size=3,
                    align=(Align.CENTER, Align.CENTER)
                    )
            extrude(amount=-.4, mode=Mode.SUBTRACT)
            with BuildSketch(base_part.faces().sort_by(Axis.Y)[0]):
                Text(
                    f"ID{self.tube_inner_diameter}\nOD{self.tube_outer_diameter}",
                    font_path=self.font_path,
                    font_size=2,
                    align=(Align.CENTER, Align.CENTER)
                    )
            extrude(amount=-.4, mode=Mode.SUBTRACT)
        return Compound(label="base", children=[base_part.part])

    def bend(self):
        """Function generating the transitional bend with a path to bend the PTFE tube."""
        with BuildPart() as bend_part:
            with BuildSketch():
                with Locations((0, self.connector_diameter*2)):
                    RegularPolygon(radius=self.hex_diameter/2, side_count=6)
                    fillet(vertices(), radius=self.hex_diameter/8)
                    Circle((self.tube_outer_diameter+self.tube_outer_tolerance)/2,
                           mode=Mode.SUBTRACT)
            revolve(axis=Axis.X, revolution_arc=self.bend_angle)
        return Compound(label="base", children=[bend_part.part.moved(
            Location((0,self.connector_diameter*-2,0)))])

    @property
    def compound(self) -> Compound:
        """Returns a Compound for the complete internal funnel."""
        fitting_nut_thread =  TrapezoidalThread(
            diameter=self.shaft_diameter+self.fitting_tolerance,
            pitch=self.fitting_pitch,
            length=self.shaft_length,
            thread_angle = 30.0,
            external=False,
            end_finishes=("square","square"),
            hand="right",
            align=Align.CENTER,
            )

        with BuildPart() as inner_fitting:
            with BuildPart() as socket_base_part:
                add(self.socket_base(chamfer_thread=False))
            with BuildPart(socket_base_part.faces().sort_by(Axis.Z)[-1]) as bend_part:
                add(self.bend())
            with BuildPart(bend_part.faces().sort_by(Axis.Z)[-1]):
                add(hex_funnel(
                    lower_radius=self.shaft_diameter/2 +self.fitting_depth,
                    upper_radius=(self.shaft_diameter/2 + self.fitting_depth) * self.funnel_top_scale,
                    inner_radius=(self.tube_inner_diameter+self.tube_inner_tolerance)/2,
                    height=self.funnel_length,
                    minimum_wall = 1.5,
                    )
                )
        return Compound(label="filament funnel", children=[inner_fitting.part, fitting_nut_thread])

    def show(self):
        """
        Shows the OCP Cad Viewer Preview
        """
        show(self.compound)

    def export_stl(self,file_path,tolerance=.0001):
        """
        Exports as an STL file to the given directory
        
        Args:
            file_path: the path for the STL export
            tolerance: the level of mesh detail for the STL, defaults to .0001
        """
        export_stl(self.compound, file_path ,tolerance=tolerance)

    def export_step(self,file_path):
        """
        Exports as an STL file to the given directory
        
        Args:
            file_path: the path for the STL export
        """
        export_step(self.compound, file_path)
