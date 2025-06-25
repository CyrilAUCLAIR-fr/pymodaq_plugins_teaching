import numpy as np
from pymodaq_utils.math_utils import my_moment

from pymodaq_utils.utils import ThreadCommand
from pymodaq_data.data import DataToExport
from pymodaq_gui.parameter import Parameter

from pymodaq.control_modules.viewer_utility_classes import DAQ_Viewer_base, comon_parameters, main
from pymodaq.utils.data import DataFromPlugins, Axis
from qtpy import initial_api

from pymodaq_plugins_teaching.hardware.spectrometer import Spectrometer

from pymodaq_plugins_teaching.daq_viewer_plugins.plugins_1D.daq_1Dviewer_Photodiode import  DAQ_1DViewer_Photodiode


class PythonWrapperOfYourInstrument:
    #  TODO Replace this fake class with the import of the real python wrapper of your instrument
    pass

# TODO:
# (1) change the name of the following class to DAQ_0DViewer_TheNameOfYourChoice
# (2) change the name of this file to daq_0Dviewer_TheNameOfYourChoice ("TheNameOfYourChoice" should be the SAME
#     for the class name and the file name.)
# (3) this file should then be put into the right folder, namely IN THE FOLDER OF THE PLUGIN YOU ARE DEVELOPING:
#     pymodaq_plugins_my_plugin/daq_viewer_plugins/plugins_0D

class DAQ_1DViewer_Photodiode_Average_FWHM(DAQ_1DViewer_Photodiode):
    """ Instrument plugin class for a OD viewer.
    
    This object inherits all functionalities to communicate with PyMoDAQ’s DAQ_Viewer module through inheritance via
    DAQ_Viewer_base. It makes a bridge between the DAQ_Viewer module and the Python wrapper of a particular instrument.

    TODO Complete the docstring of your plugin with:
        * The set of instruments that should be compatible with this instrument plugin.
        * With which instrument it has actually been tested.
        * The version of PyMoDAQ during the test.
        * The version of the operating system.
        * Installation instructions: what manufacturer’s drivers should be installed to make it run?

    Attributes:
    -----------
    controller: object
        The particular object that allow the communication with the hardware, in general a python wrapper around the
         hardware library.
         
    # TODO add your particular attributes here if any

    """
    params = comon_parameters+[
        ## TODO for your custom plugin: elements to be added here as dicts in order to control your custom stage
        ]

    def grab_data(self, Naverage=1, **kwargs):
        """Start a grab from the detector

        Parameters
        ----------
        Naverage: int
            Number of hardware averaging (if hardware averaging is possible, self.hardware_averaging should be set to
            True in class preamble and you should code this implementation)
        kwargs: dict
            others optionals arguments
        """
        ## TODO for your custom plugin: you should choose EITHER the synchrone or the asynchrone version following

        # synchrone version (blocking function)
        # raise NotImplemented  # when writing your own plugin remove this line
        data_tot = self.controller.grab_spectrum()
        wavelength = self.controller.get_wavelength_axis()

        moments = my_moment(wavelength, data_tot)
        moments_bis = my_moment(data_tot, wavelength, )
        self.dte_signal.emit(DataToExport(name='myplugin',
                                          data=[DataFromPlugins(name='Spectrum', data=[data_tot],
                                                                dim='Data1D', labels=['intensité',],
                                                                axes=[Axis('wavelength',
                                                                           units='m',
                                                                           data=self.controller.get_wavelength_axis()*1e-9)]),
                                                DataFromPlugins(name='moyenne', data=[np.atleast_1d(moments[0])],
                                                                dim='Data0D', labels=['valeur'], ),
                                                DataFromPlugins(name='FWHM', data=[np.atleast_1d(moments[1])],
                                                                dim='Data0D', labels=['valeur'], )
                                                ]))
        #########################################################

        # asynchrone version (non-blocking function with callback)
        # raise NotImplemented  # when writing your own plugin remove this line
        # self.controller.your_method_to_start_a_grab_snap(self.callback)  # when writing your own plugin replace this line
        #########################################################


if __name__ == '__main__':
    main(__file__)
