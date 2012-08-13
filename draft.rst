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

Specifications for the H5MD file format - Draft
===============================================

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
information such as simulation parameters. Only the "h5md" group is mandatory in
a H5MD file. The other data groups are optional, allowing the user to store only
relevant data. Inside each group, every dataset is again optional. Within
time-dependent groups, the "step", "time" and "value" datasets are however
mandatory as they form an important part of the specification.

The groups that are part of the H5MD specifications are

* h5md: Group containing, as attributes, information on the file itself.
* parameters: Group containing the parameters for a simulation/dataset, such as
  the spatial dimension of the system or simulation parameters.
* trajectory: Group containing the trajectory of the system (positions, ...).
* observables: Group containing all time-dependent variables in the system,
  except the ones found in the "trajectory group".

All time dependent data (whether in "trajectory" or "observables") is organized
into HDF5 groups that contain time information in addition to the data.

Global attributes
-----------------

A few global attributes are defined for convenience. These attributes are given
to the 'h5md' group.

* creator: The name of the program that created the file.
* creator_version: The version of the program that created the file, as a string
  containing proper identification for the given program.
* version: The version of the H5MD specification that the file conforms
  to. 'version' is a dimension \[2\] integer dataset. The first element is the
  major version number and the second element the minor version number.
* creation_time: The creation time of the file. It is an integer scalar dataset
  representing the number of seconds since the Epoch.
* author: The name of the author of the simulation/experiment. It is of the
  form "Real Name <email@domain.tld>", where the email is optional.

The content of this group is::

    h5md
     +-- creator
     +-- creator_version
     +-- version
     +-- creation_time
     +-- author

Storage of the time information for time-dependent datasets
-----------------------------------------------------------

To link data the data of a time dependent dataset to a time in the simulation,
H5MD defines a group structure containing, in addition to the data, the
corresponding integer time step information (number of simulation steps) and
physical time information (the time in simulation or physical units,
real-valued).

As an example, here is the data for the position in a group of particles::

    trajectory
      \-- group1
           \-- position
                \-- value
                \-- step
                \-- time

where the first dimension of "value" must match the unique dimension of "step"
and "time".

The "step" dataset must be of integer datatype to allow exact temporal matching
of data from one data group to another within the same file.

If several datasets are dumped at equal times, "step" and "time" may be hard
links to the "step" and "time" datasets of one data group. If data are sampled
at different times (for instance, one needs the positions more frequently than
the velocities), "step" and "time" are unique to each data group.

Standardized data elements
--------------------------

Trajectory group
^^^^^^^^^^^^^^^^

The trajectories are stored in the "trajectory" group. The trajectory group
itself is only a container for groups that represent different parts of the
system under consideration. There may be one or several groups in the trajectory
group, as needed, but the trajectory group may only contain groups.
Inside of these subgroups, for each kind of trajectory information there is a
group that contains datasets "value", "step", and "time".

* Standardised subgroups are "position", "velocity", "force" and "species".

* The "value" dataset holds the actual data and has dimensions
  \[variable\]\[N\]\[D\], where the variable dimension is present to accumulate
  time steps.

* The "step" dataset has dimensions \[variable\] and contains the integer step
  corresponding to the time step at which the corresponding data has been
  written to the "coordinates" dataset.

* The "time" dataset is as the "step" dataset, but contains the real value of
  the time.

* The "species/value" dataset has dimensions \[N\] if the species do not
  change in the course of time, that is if there is no chemical reaction
  occurring, or of dimensions \[variable\]\[N\] if the species of particles may
  change in the course of time. The species dataset should be of an integer
  datatype only. Also, as the species may change less often than other
  variables, if the species data is absent for a given time step, the most
  recent data for the species should be fetched instead.

All arrays are stored in C-order as enforced by the HDF5 file format (see `§
3.2.5 <http://www.hdfgroup.org/HDF5/doc/UG/12_Dataspaces.html#ProgModel>`_). A C
or C++ program may thus declare r\[N\]\[D\] for the coordinates array while the
Fortran program will declare a r(D,N) array (appropriate index ordering for a
N atoms D dimensions system) and the hdf5 file will be the same.

The "position", "velocity" and "force" datasets possess an optional attribute
that is the unit of their respective data ("nm" for the position, for instance).

The content of the trajectory group is the following::

    trajectory
     \-- group1
          \-- position
          |    \-- value
          |    \-- step
          |    \-- time
          \-- velocity
          |    \-- value
          |    \-- step
          |    \-- time
          \-- force
          |    \-- value
          |    \-- step
          |    \-- time
          \-- species
          |    \-- value
          |    \-- step
          |    \-- time

Box specification
^^^^^^^^^^^^^^^^^

The box specification is stored in the observables group, as a group. The type
of box is stored as an attribute to this box group ::

  observables
   \-- box
        +-- type
   ...

The box type can be "cuboid" or "triclinic". Depending on this information,
additional data is stored.

Cuboid box
""""""""""

* edges: A vector specifying the length of the box in the D dimensions of
  space.
* offset: A vector specifying the lower coordinate for all directions.

Triclinic box
"""""""""""""

* edges: A set of D×D-dimensional matrices with the rows specifying the
  directions and lengths of the edges of the box.
* offset: A vector specifying the lower coordinate for all directions.

Time dependence
"""""""""""""""

For all box kinds, if the data for edges,offset is stored as a single dataset,
it is considered fixed in time. Else, it should comply to the step, time and
value organization.

For instance, a cuboid box that changes in time would appear as ::

  observables
   \-- box
        +-- type
        \-- edges
             \-- step [var]
             \-- time [var]
             \-- value [var][D]
        \-- offset
             \-- step [var]
             \-- time [var]
             \-- value [var][D]

where "type" is set to "cuboid".


Observables group
^^^^^^^^^^^^^^^^^

Macroscopic observables are stored as \[variable\] time series for scalar
observables and as \[variable\]\[d\] time series for d-dimensional vector
observables. The variable dimension allows to accumulate time steps. The name of
the group holding these datasets is "observables". This group has the same
structure as "trajectory": for each observable there is a group containing three
datasets: the actual data in "value" and the step and time datasets.
Observables representing only a subset of the particles may be stored in
appropriate subgroups similarly to the "trajectory" tree.

The following names should be obeyed for the corresponding observables:

* total_energy
* potential_energy
* kinetic_energy
* pressure
* temperature

The content of the observables group is the following::

    observables
     \-- obs1
     |    \-- value
     |    \-- step
     |    \-- time
     \-- obs2
     |    \-- value
     |    \-- step
     |    \-- time
     \-- group1
     |    \-- obs3
     |         \-- value
     |         \-- step
     |         \-- time
     \-- ...

Program-dependent groups
------------------------

Some informations do not adequately fit a strict specification and can be
included in groups whose name is however specified. These names are listed here.

Parameters
^^^^^^^^^^

The "parameters" group may contain all parameters passed to initialize the
simulation. Example are: temperature, random number generator seed, initial box
size, ...

Profiling
^^^^^^^^^

The "profiling" group may contain information related to the timing of various
parts of the simulation.

