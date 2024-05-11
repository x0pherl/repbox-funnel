"""Module providing parts for a repbox filament funnel and external fitting."""
from math import floor
from configparser import ConfigParser
from bd_warehouse.thread import TrapezoidalThread
from build123d import (BuildPart, BuildSketch,
                       Circle, RegularPolygon,
                       extrude, chamfer, Text, Compound,
                       Mode, Location, Locations, CounterSinkHole,
                       Align, GeomType, SortBy, Axis, export_step, export_stl)
from ocp_vscode import show

REVISION_TEXT = "R1.0"

"""

"""
class ExternalFitting:
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

    @property
    def compound(self) -> Compound:
        """Returns a Compound for the complete external fitting."""
        chamfer_radius = (self.shaft_diameter-
                          (self.tube_outer_diameter+self.tube_outer_tolerance))/8
        fitting_nut_thread =  TrapezoidalThread(
            diameter=self.connector_diameter,
            pitch=self.connector_pitch,
            length=self.connector_depth-self.connector_pitch/2,
            thread_angle = 30.0,
            external=False,
            hand="right",
            align=Align.CENTER,
            ).moved(Location((0,0,self.connector_pitch/2)))

        shaft_thread =  TrapezoidalThread(
            diameter=self.shaft_diameter,
            pitch=self.fitting_pitch,
            length=self.shaft_length-self.fitting_depth-chamfer_radius,
            thread_angle = 30.0,
            external=True,
            interference=self.shaft_interference,
            end_finishes=("square","chamfer"),
            hand="right",
            align=Align.CENTER,
            ).moved(Location((0,0,self.connector_depth+self.fitting_depth)))

        with BuildPart() as outer_fitting:
            with BuildSketch():
                RegularPolygon(radius=self.fitting_diameter/2, side_count=6)
            extrude(amount=self.connector_depth)
            with BuildSketch(outer_fitting.faces().sort_by(Axis.Y)[0]):
                Text(
                    REVISION_TEXT,
                    font_path=self.font_path,
                    font_size=3,
                    align=(Align.CENTER, Align.CENTER)
                    )
            extrude(amount=-.4, mode=Mode.SUBTRACT)
            with BuildSketch(outer_fitting.faces().sort_by(Axis.Y)[-1]):
                Text(
                    f"OD\n{floor(self.tube_outer_diameter)}mm",
                    font_path=self.font_path,
                    font_size=2,
                    align=(Align.CENTER, Align.CENTER)
                    )
            extrude(amount=-.4, mode=Mode.SUBTRACT)
            with Locations(outer_fitting.faces().sort_by(Axis.Z)[0]):
                CounterSinkHole(
                    radius=self.connector_diameter/2,
                    counter_sink_radius=self.connector_diameter/2+self.connector_pitch/2
                    )
            with BuildSketch(outer_fitting.faces().sort_by(Axis.Z)[-1]):
                Circle(self.shaft_diameter/2)
                Circle((self.tube_outer_diameter+self.tube_outer_tolerance)/2, mode=Mode.SUBTRACT)
            extrude(amount=self.fitting_depth)
            with BuildSketch(outer_fitting.faces().sort_by(Axis.Z)[-1]):
                Circle(self.shaft_diameter/2-1)
                Circle((self.tube_outer_diameter+self.tube_outer_tolerance)/2, mode=Mode.SUBTRACT)
            extrude(amount=self.shaft_length-self.fitting_depth)
            chamfer(
                outer_fitting.edges()
                .filter_by(GeomType.CIRCLE)
                .sort_by(SortBy.RADIUS)
                .sort_by(Axis.Z)[-1],
                length=chamfer_radius,
            )
        return Compound (label="External Fitting",
                        children=[Compound(label="Outer Fitting",
                                            children=[outer_fitting.part]),
                                    Compound(label="connector thread",
                                            children=[fitting_nut_thread]),
                                    Compound(label="shaft thread", children=[shaft_thread])])

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
