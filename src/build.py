"loads configs, generates objects, and creates stl exports"
from external_fitting import ExternalFitting
from internal_funnel import InternalFunnel


external_fitting = ExternalFitting('2.5mmIDx4mmOD-settings.ini')
external_fitting.show()
external_fitting.export_stl('../stl/4mmOD-external-fitting.stl')

external_fitting = ExternalFitting('3mmIDx6mmOD-settings.ini')
external_fitting.show()
external_fitting.export_stl('../stl/6mmOD-external-fitting.stl')

internal_funnel = InternalFunnel('2mmIDx4mmOD-settings.ini')
internal_funnel.show()
internal_funnel.export_stl('../stl/2mmIDx4mmOD-internal-funnel.stl')

internal_funnel = InternalFunnel('2.5mmIDx4mmOD-settings.ini')
internal_funnel.show()
internal_funnel.export_stl('../stl/2.5mmIDx4mmOD-internal-funnel.stl')

internal_funnel = InternalFunnel('3mmIDx6mmOD-settings.ini')
internal_funnel.show()
internal_funnel.export_stl('../stl/3mmIDx6mmOD-internal-funnel.stl')
