Specifications for the H5MD file format
========================================

Objective
---------

H5MD is aimed at becoming a specification to store molecular simulation data.
It is based on the `HDF5 <http://www.hdfgroup.org/HDF5/>`_ file format. H5MD 
stands for "HDF5 for molecular data".

It should facilitate portability of said data amongst simulation and analysis
programs.

General organization
--------------------

H5MD defines a HDF5 group structure. Inside a group, a number of required
fields exist and should possess a conforming name and shape.

Several groups may exist in a file, allowing the description of several
subsystems. Multiple time steps are found inside a single dataset. One can then
obtain either a snapshot of the system at a given time or extract a single
trajectory via dataset slicing.

The file is allowed to possess non-conforming groups that contain other
information such as simulation parameters.

Global attributes
-----------------

A few global attributes are defined for convenience. These attributes are given
to the 'H5MD' group.

* creator: The name of the program that created the file.
* version: The version of the H5MD specification that the file conforms
  to. 'version' is a dimension \[2\] integer dataset. The first element is the
  major version number and the second element the minor version number.
* creation_time: The creation time of the file. It is an integer scalar dataset
  representing the number of seconds since the Epoch.


Standardized data elements
--------------------------

Trajectory group
^^^^^^^^^^^^^^^^

The trajectories are stored in the "trajectory" group. For each kind of
trajectory information there is a group that contains a "coordinates" dataset, a
"step" dataset and a "time" dataset.

* The "coordinates" dataset has dimensions \[variable\]\[N\]\[D\] where the
  variable dimension is present to accumulate time steps.

* The "step" dataset has dimensions \[variable\] and contains the integer step
  corresponding to the time step at which the corresponding data has been
  written to the "coordinates" dataset.

* The "time" dataset is as the "step" dataset, but contains the real value of
  the time.

* The coordinates are "position", "velocity", "force" and "species".
  
* The "species" dataset has dimensions \[N\] if the species do not change in the
  course of time, that is if there is no chemical reaction occurring, or of
  dimensions \[variable\]\[N\] if the species of particles may change in the
  course of time. The species are stored as 1-byte unsigned integers.

All arrays are stored in C-order as enforced by the HDF5 file format (see `§
3.2.5 <http://www.hdfgroup.org/HDF5/doc/UG/12_Dataspaces.html#ProgModel>`_). A C
or C++ program may thus declare r\[N\]\[D\] for the coordinates array while the
Fortran program will declare a r(D,N) array (appropriate index ordering for a
N atoms D dimensions system) and the hdf5 file will be the same.

The "position", "velocity" and "force" datasets possess an optional attribute
that is the unit of their respective data ("nm" for the position, for instance).

Trajectory subgroups
^^^^^^^^^^^^^^^^^^^^

Some simulations effectively take into account different kind of particles. For
example, a solvent (with a large number of particles) may only be needed for
checkpointing.
In this situation, the 'trajectory' group will contain *only* subgroups. Each of
these subgroups are then considered trajectory groups in themselves.

Storage of the time information in the trajectory group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To link data from the trajectory group datasets to a time in the simulation, two
datasets containing the integer time step (number of simulation steps) and the
physical time (the time in simulation or physical units, real-valued) are
necessary. They are present in the same group as a trajectory dataset. If all
data are dumped at equal times, "step" and "time" may be hard links to the
"step" and "time" datasets of another coordinates variable. If data are sampled
at different times (for instance, one needs the positions more frequently than
the velocities), "step" and "time" are unique to each coordinates variable.

In order to read the information, the procedure is similar in both cases: the
coordinate group contain the attributes either "step" and "time" as datasets or
as hard links.


Observables group
^^^^^^^^^^^^^^^^^

Macroscopic observables are stored as \[variable\] time series for scalar
observables and as \[variable\]\[d\] time series for d-dimensional vector
observables. The variable dimension allows to accumulate time-steps. The name of
the group holding these datasets is "observables". This group has the same
structure as "trajectory": for each observable there is a group containing three
datasets: the actual data in "samples" and the step and time datasets.

* total_energy
* interaction_energy
* kinetic_energy
* temperature

Program-dependent groups
------------------------

Some informations do not adequately fit a strict specification and can be
included in groups whose name is however specified. These names are listed here.

Parameters
^^^^^^^^^^

The "parameters" group may contain all parameters passed to initialize the
simulation. Example are: temperature, random number generator seed, ...

Profiling
^^^^^^^^^

The "profiling" group may contain information related to the timing of various
parts of the simulation.

Reserved names
--------------

Part of the H5MD specification is a number of reserved names. This allows a data
analysis package to handle adequately the datasets with reserved names. Future
names should be kept concise but worded fully.

The present list of reserved names is:

* coordinates
* creator
* datetime
* force
* version
* interaction_energy
* kinetic_energy
* observables
* parameters
* position
* profiling
* temperature
* total_energy
* velocity

Data elements in discussion
---------------------------

* Reserved names

  At this time, position, velocity and force are reserved. How far should we
  specify? Other elements seem appropriate for reserved names: temperature, time
  step - DT, ...

* Simulation box information

  Some information on the simulation box geometry could be included. As a minimal suggestion: box_origin = basis point in the D dimensions (lowest value reached by the position) , box_size (total linear size in each dimension)

* Topology

  There is the need to store topology for rigid bodies, elastic networks or
  proteins. The topology may be a connectivity table, contain bond lengths, ...

* Simulation parameters

  Box size, time step, used force field, per species mass, ...

* Scalar and vector fields

  May be used to store coarse grained or cell-based physical quantities.

* Species information

  Some simulations allow species to change in time via chemical reactions. The
  species thus need their own time-dependent dataset. To simplify matters, it is
  suggested to use a \[variable\]\[N\] dataset for such simulations but only a
  \[N\] dataset when the species are fixed in the course of time. Species may be
  specified by a 1-byte integer (8-bit, allowing 256 values).

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
