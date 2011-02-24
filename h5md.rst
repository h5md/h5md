Specifications for the h5md file format
========================================

Objective
---------

h5md is aimed at becoming a specification to store molecular simulation data.
It is based on the `HDF5 <http://www.hdfgroup.org/HDF5/>`_ file format. h5md
stands for "hdf5 for molecular data".

It should facilitate portability of said data amongst simulation and analysis
programs.

General organization
--------------------

h5md defines a HDF5 group structure. Inside a group, a number of required
fields exist and should possess a conforming name and shape.

Several groups may exist in a file, allowing the description of several
subsystems. Multiple time steps are found inside a single dataset. One can then
obtain either a snapshot of the system at a given time or extract a single
trajectory via dataset slicing.

The file is allowed to possess non-conforming groups that contain other
information such as simulation parameters.

Standardized data elements
--------------------------

* atomic coordinates in 1,2 or 3D

  The coordinates are stored in the dataset named "position". The dataset has the
  dimensions \[variable\]\[N\]\[D\] where the variable dimension is present to
  accumulate timesteps.

* atomic velocities in 1,2 or 3D

  As for the coordinates in a dataset named "velocity"
  
* atomic forces in 1,2 or 3D

  As for the coordinates in a dataset named "force"
  
* species identifier (be it a number or a character ?) 


All arrays are stored in C-order as enforced by the HDF5 file format (see `§
3.2.5 <http://www.hdfgroup.org/HDF5/doc/UG/12_Dataspaces.html#ProgModel>`_). A C
or C++ program may thus declare r\[N\]\[D\] for the coordinates array while the
fortran program will declaire a r(D,N) array (appropriate index ordering for a
N atoms D dimensions system) and the hdf5 file will be the same.

Reserved names
--------------

Part of the h5md specification is a number of reserved names. This allows a data
analysis package to handle adequately the datasets with reserved names. Future
names should be kept concise but worded fully.

The present list of reserved names is:

* position
* velocity
* force

Data elements in discussion
---------------------------

* Reserved names

  At this time, position, velocity and force are reserved. How far should we
  specify? Other elements seem appropriate for reserved names: temperature, time
  step - DT, ...

* Topology

  There is the need to store topology for rigid bodies, elastic networks or
  proteins. The topology may be a connectivity table, contain bond lengths, ...

* Macroscopic variables

  These are variables that are computed during a simulation.

* Simulation parameters

  Box size, time step, used force field, per species mass, ...

* Scalar and vector fields

  May be used to store coarse grained or cell-based physical quantities.

