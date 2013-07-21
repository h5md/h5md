.. Copyright © 2011-2013 Pierre de Buyl, Peter Colberg and Felix Höfling
   
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

Data elements in discussion
---------------------------

Extensions: Storage of time-dependent data
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Time-averaged data
==================

Time-averaged data are stored for some applications, for example the potential
energy is computed every 200 simulation steps but only the average of 50 such
computations is stored (every 10⁴ steps). Additional statistical information
along with the mean value is stored by extending the triple ``value``,
``step``, ``time``:

The structure of such a data group is ::

    data_group
     \-- value [var][...]
          +-- (unit)
     \-- error [var][...]
     \-- count [var]
     \-- step [var]
     \-- time [var]
          +-- (unit)

* The ``value`` dataset is as before, but stores the arithmetic mean of the
  data sampled since the last output to this group.

* The ``error`` dataset stores the statistical error of the mean value, given
  by :math:`\sqrt{\sigma^2/(N-1)}` with the variance :math:`\sigma^2` and the
  number of sampled data points :math:`N`. The error is 0 in case of :math:`N=1`.
  The dimension of the dataset must agree with those of ``value`` and its
  (optional) unit is inferred from ``value``.

* The ``count`` dataset is of integer type and stores the number :math:`N` of
  sampled data points used.  The dimension of the dataset is variable and must
  agree with the first dimension of ``value``.

Note that the statistical variance and the standard deviation are easily
obtained from combining the datasets ``error`` and ``count`` and need not to be
stored explicitly.


Extensions: Observables group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Particle number
===============

The data stored in ``/observable`` represent averages over all particles or
subsets thereof. The root group or each subgroup carries an integer attribute
``particles`` stating the number of particles involved in the average. If this
number varies, the attribute is replaced by a group ``particles`` obeying the
``value``, ``step``, ``time`` scheme.

The content of the observables group has the following structure ::

    observables
     \-- box
     \-- particles
     |    \-- value [var]
     |    \-- step [var]
     |    \-- time [var]
     \-- obs1
     |    \-- value [var]
     |    \-- step [var]
     |    \-- time [var]
     \-- obs2
     |    \-- value [var][D]
     |    \-- step [var]
     |    \-- time [var]
     \-- group1
     |    +-- particles
     |    \-- obs3
     |         \-- value [var][D][D]
     |         \-- step [var]
     |         \-- time [var]
     \-- ...


Further suggestions
^^^^^^^^^^^^^^^^^^^

* Simulation box information

  Some information on the simulation box geometry could be included. For now,
  the box size is included in the observables group. Symmetry groups could be
  included in the future.

* Topology

  There is the need to store topology for rigid bodies, elastic networks or
  proteins. The topology may be a connectivity table, contain bond lengths, ...

* Scalar and vector fields

  May be used to store coarse grained or cell-based physical quantities.

* The "density" dataset has dimensions \[variable\]\[Nx\]\[Ny\]\[Nz\] where the
  variable dimension allows to accumulate steps, and Nx, Ny and Nz are the
  number of data points in each dimension. This dataset possesses the attributes
  "x0" and "dx", both of dimension "D" (the dimensionality of the system). "x0"
  stores the center of the 0-th cell (the \[0,0,0\] cell) and "dx" stores the
  cell spacing. The notation from "x" to "z" is given as an example and other
  ranks can be given for other dimensionalities.

* The "velocity_field" dataset has dimensions \[variable\]\[Nx\]\[Ny\]\[Nz\]\[D\]
  where "D" is the dimensionality of the system. It stores a cell-baed velocity
  field. The same remark as for the "x", "y" and "z" variables as for the
  "density" dataset applies.

* Tracking history of authors and creator programs

  It would be desirable to track authors and creator programs.
  This could be achieved by replacing the respective attributes in ``/hm5d`` by
  datasets of variable dimension. The object tracking of these datasets may
  then be matched (approximately) with the creation/modification times of other
  datasets.

* Parallel issues

  Although not a specification in itself, one advantage of using HDF5 is the
  Parallel-HDF5 extension for MPI environments. File written by parallel
  programs should be identical to programs written by serial programs.

  An issue remains however: as particles move in space, they may belong to
  varying CPUs. A proposition to this problem is to send all particles, as a
  copy, to their original CPU and to write them from there using collective IO
  calls. Particles for which the ordering is not important (for instance solvent
  particles that may be required for checkpointing only) could be written from
  their actual CPU without recreating the original order.
