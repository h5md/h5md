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

Data elements in discussion
---------------------------

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

* Date and time tracking

  HDF5 allows to track creation times and more, via the H5Pset_obj_track_times
  function. See the
  `HDF5 Reference Manual
  <http://www.hdfgroup.org/HDF5/doc/RM/RM_H5P.html#Property-SetObjTrackTimes>`_
  .


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
