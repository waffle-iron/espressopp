#  Copyright (C) 2012-2016 Max Planck Institute for Polymer Research
#  Copyright (C) 2008-2011 Max-Planck-Institute for Polymer Research & Fraunhofer SCAI
#  
#  This file is part of ESPResSo++.
#  
#  ESPResSo++ is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  
#  ESPResSo++ is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>. 


r"""
************************************************************************************
**LBOutputVzInTime** - controls output of the velocity component on a site in time
************************************************************************************
Child class derived from the abstract class :class:`espressopp.analysis.LBOutput`. 
It computes and outputs the velocity component :math:`v_z` in time on a specific
lattice site (the value used at the moment is :math:`{0.25*N_i, 0, 0}`).

.. function:: espressopp.analysis.LBOutputVzInTime(system,latticeboltzmann)

	:param system: system object defined earlier in the python-script
	:param latticeboltzmann: lattice boltzmann object defined earlier in the python-script

.. Note::

	this class should be called from external analysis class :class:`espressopp.integrator.ExtAnalyze`
	with specified periodicity of invokation and after this added to the integrator. See an example for details.

Example to call the profiler:

>>> # initialise profiler (for example with the name outputVzInTime) with system and
>>> # lattice boltzmann objects as parameters:
>>> outputVzInTime = espressopp.analysis.LBOutputVzInTime(system,lb)
>>>
>>> # initialise external analysis object (for example extAnalysisNum2) with
>>> # previously created profiler and periodicity of invocation in steps:
>>> extAnalysisNum2=espressopp.integrator.ExtAnalyze(outputVzInTime,100)
>>>
>>> # add the external analysis object as an extension to the integrator
>>> integrator.addExtension(extAnalysisNum2)


.. function:: espressopp.analysis.LBOutputVzInTime(system, latticeboltzmann)

		:param system: 
		:param latticeboltzmann: 
		:type system: 
		:type latticeboltzmann: 
"""
from espressopp.esutil import cxxinit
from espressopp import pmi

from espressopp.analysis.LBOutput import *
from _espressopp import analysis_LBOutput_VzInTime

class LBOutputVzInTimeLocal(LBOutputLocal, analysis_LBOutput_VzInTime):
    def __init__(self, system, latticeboltzmann):
	if not (pmi._PMIComm and pmi._PMIComm.isActive()) or pmi._MPIcomm.rank in pmi._PMIComm.getMPIcpugroup():
            cxxinit(self, analysis_LBOutput_VzInTime, system, latticeboltzmann)

if pmi.isController :
    class LBOutputVzInTime(LBOutput):
        __metaclass__ = pmi.Proxy
        pmiproxydefs = dict(
            cls =  'espressopp.analysis.LBOutputVzInTimeLocal',
            pmicall = ["writeOutput"]
            )
