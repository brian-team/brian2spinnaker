from spynnaker.pyNN.models.abstract_models.abstract_population_vertex import \
    AbstractPopulationVertex
from spynnaker.pyNN.utilities import constants
from data_specification.enums.data_type import DataType
from spynnaker.pyNN.models.abstract_models.abstract_exp_population_vertex \
    import AbstractExponentialPopulationVertex
from spynnaker.pyNN.models.abstract_models.abstract_Izhikevich_vertex \
    import AbstractIzhikevichVertex
from spynnaker.pyNN.models.neural_properties.neural_parameter \
    import NeuronParameter


class IzhikevichCurrentExponentialPopulation(
        # TODO: Need to use Delta synapse, which hasn't yet been implemented in Python, but does what Brian needs
        AbstractPopulationVertex):

    # Just create a unique identifier here
    CORE_APP_IDENTIFIER = 0xad
    # This needs to be specified by the user probably, based on how much RAM
    # and CPU time it takes + data structure limitations
    _model_based_max_atoms_per_core = 256

    # noinspection PyPep8Naming
    def __init__(self, n_neurons, machine_time_step, timescale_factor,
                 spikes_per_second, ring_buffer_sigma, constraints=None,
                 label=None):

        # Instantiate the parent classes
        AbstractPopulationVertex.__init__(
            self, n_neurons=n_neurons, n_params=10, label=label,
            binary="IZK_curr_exp.aplx", constraints=constraints,
            max_atoms_per_core=IzhikevichCurrentExponentialPopulation._model_based_max_atoms_per_core,
            machine_time_step=machine_time_step,
            timescale_factor=timescale_factor,
            spikes_per_second=spikes_per_second,
            ring_buffer_sigma=ring_buffer_sigma)
        self._executable_constant = \
            IzhikevichCurrentExponentialPopulation.CORE_APP_IDENTIFIER

    @property
    def model_name(self):
        return "IZK_curr_exp"

    @staticmethod
    def set_model_max_atoms_per_core(new_value):
        IzhikevichCurrentExponentialPopulation.\
            _model_based_max_atoms_per_core = new_value

    def get_cpu_usage_for_atoms(self, vertex_slice, graph):
        """
        Gets the CPU requirements for a range of atoms
        """
        # 782 is the maximum value that lets you put 256 atoms on a core
        return 782 * ((vertex_slice.hi_atom - vertex_slice.lo_atom) + 1)

    def get_parameters(self):
        """
        Generate Neuron Parameter data (region 2):
        """

        # Get the parameters:
        # typedef struct neuron_t {
        #
        # // nominally 'fixed' parameters
        #     REAL         A;
        #     REAL         B;
        #     REAL         C;
        #     REAL         D;
        #
        # // Variable-state parameters
        #     REAL         V;
        #     REAL         U;
        #
        # // offset current [nA]
        #     REAL         I_offset;
        #
        # // current timestep - simple correction for threshold in beta version
        #     REAL         this_h;
        # } neuron_t;
        return [
            # Currently softfloat not defined on the Python side, so have to use S1615
            NeuronParameter(self._a, DataType.S1615),
            NeuronParameter(self._b, DataType.S1615),
            NeuronParameter(self._c, DataType.S1615),
            NeuronParameter(self._d, DataType.S1615),
            NeuronParameter(self._v_init, DataType.S1615),
            NeuronParameter(self._u_init, DataType.S1615),
            # delete this
            NeuronParameter(self.ioffset(self._machine_time_step),
                    DataType.S1615),
            #NeuronParameter(0, DataType.S1615) # no idea what this, delete it
        ]

    def is_population_vertex(self):
        return True

    #def is_exp_vertex(self):
    #    return True

    def is_recordable(self):
        return True

    #def is_izhikevich_vertex(self):
    #    return True



######################## Other files

# Folder structure:
# modelname/
#   __init__.py
#   modelname.py
#   model_binaries/
#      __init__.py
#      modelname.aplx (eventually)
#   neural_models/   (C/H files go here)


######################## This should be in modelname/__init__.py file


from modeldef import NameOfModel
from modelname import model_binaries

def _init_module():
    import logging
    import os
    import spynnaker.pyNN
    # register with SpyNNaker
    spynnaker.pyNN.register_binary_search_path(os.path.dirname(model_binaries.__file__))
    
_init_module()
 