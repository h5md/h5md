Specifications for the h5mol file format
========================================

Objective
---------

h5mol is aimed at becoming a specification to store molecular simulation data.
It is based on the `HDF5 <http://www.hdfgroup.org/HDF5/>`_ file format.

It should facilitate portability of said data amongst simulation and analysis
programs.

General organization
--------------------

h5mol defines a HDF5 group structure. Inside a group, a number of required
fields exist and should possess a conforming name and shape.

Several groups may exist in a file, allowing either the description of several
subsystems or the storing of multiple time steps.

The file is allowed to possess non-conforming groups that contain other
information such as simulation parameters.

Standardized data elements
--------------------------

* atomic coordinates in 1,2 or 3D
* atomic velocities in 1,2 or 3D
* atomic forces in 1,2 or 3D
* species identifier (be it a number or a character ?) 


All arrays are stored in C-order as enforced by the HDF5 file format (see `§
3.2.5 <http://www.hdfgroup.org/HDF5/doc/UG/12_Dataspaces.html#ProgModel>`_). A C
or C++ program may thus declare r\[N\]\[D\] for the coordinates array while the
fortran program will declaire a r(D,N) array (appropriate index ordering for a
N atoms D dimensions system) and the hdf5 file will be the same.

Data elements in discussion
---------------------------

* Topology

  There is the need to store topology for rigid bodies, elastic networks or proteins. The topology may be a connectivity table, contain bond lengths, ...

* Macroscopic variables

  These are variables that are computed during a simulation.

* Simulation parameters

  Box size, time step, used force field, per species mass, ...

