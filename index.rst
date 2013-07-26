.. Copyright © 2011 Pierre de Buyl, Peter Colberg and Felix Höfling
   
   This file is part of H5MD.
   
   H5MD is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.
   
   H5MD is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.
   
   You should have received a copy of the GNU General Public License
   along with H5MD.  If not, see <http://www.gnu.org/licenses/>.

H5MD : HDF5 for molecular data
==============================

H5MD is a file format specification, based upon `HDF5
<http://www.hdfgroup.org/HDF5/>`_, aimed at the efficient and portable storage
of molecular data (e.g. simulation trajectories, molecular structures, ...).
H5MD implements data models for a variety of computational problems, e.g.,
molecular simulation using molecular dynamics, or computational fluid dynamics
using multi-particle collision dynamics.

The first official release of the specification will contain particle
trajectories (positions, velocities, forces and species) as well as
thermodynamical observables. Afterwards, extensions will be considered on the
basis of discussion with users of H5MD.

H5MD is developed by Pierre de Buyl, Peter Colberg and Felix Höfling and is
available under the `GNU General Public License
<http://www.gnu.org/licenses/gpl.html>`_.

The draft represents the current state of the specification.

If you want to know more about or contribute to H5MD, please visit the `project
page <https://savannah.nongnu.org/p/h5md/>`_ of H5MD or join the `mailing list
<https://lists.nongnu.org/mailman/listinfo/h5md-user>`_.

Contents
--------

.. toctree::
   :maxdepth: 2

   draft
   discussion
   implementation
   software


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

