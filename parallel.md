% Savio parallel processing training
% April 21, 2020
% Nicolas Chan, Christopher Hann-Soden, Chris Paciorek, Wei Feinstein

# Introduction

We'll do this mostly as a demonstration. We encourage you to login to your account and try out the various examples yourself as we go through them.

Much of this material is based on the extensive Savio documention we
have prepared and continue to prepare, available at our new
documentation site: [https://docs-research-it.berkeley.edu/services/high-performance-computing](https://docs-research-it.berkeley.edu/services/high-performance-computing) as well as our old site: [http://research-it.berkeley.edu/services/high-performance-computing](http://research-it.berkeley.edu/services/high-performance-computing).

The materials for this tutorial are available using git at the short URL ([https://tinyurl.com/brc-feb20](https://tinyurl.com/brc-apr20)), the  GitHub URL ([https://github.com/ucb-rit/savio-training-parallel-2020](https://github.com/ucb-rit/savio-training-parallel-2020)), or simply as a [zip file](https://github.com/ucb-rit/savio-training-parallel-2020/archive/master.zip).

# Outline

 - Introduction
   - Hardware
   - Parallel processing terms and concepts
   - Approaches to parallelization
     - Embarrassingly parallel computation
	 - Threaded computations
	 - Multi-process computations
   - Considerations in parallelizing your work
 - Submitting and monitoring parallel jobs on Savio
   - Job submission flags
   - MPI- and openMP- based submission examples
   - Monitoring jobs to check parallelization
 - Parallelization using existing software
   - How to look at documentation to understand parallel capabilities
   - Specific examples
 - Embarrassingly parallel computation
   - GNU parallel
   - Job submission details
 - Parallelization in Python, R, and MATLAB (time permitting)
   - High-level overview: threading versus multi-process computation
   - Dask and ipyparallel in Python
   - future and other packages in R
   - parfor in MATLAB

# Introduction: Savio

Savio is a cluster of hundreds of computers (aka 'nodes'), each with many CPUs
(cores), networked together. 

<center><img src="savio_diagram.jpeg"></center>

# Introduction: multi-core computers

Each computer has its own memory and multiple (12-56) cores per
machine.

<center><img src="generic_machine.jpeg"></center>

savio2 nodes: two Intel Xeon 12-core Haswell processors (24 cores per
node (a few have 28))

# Introduction: Terms and concepts

- Hardware terms
  - *cores*: We'll use this term to mean the different processing
    units available on a single node. All the cores share main memory.
    - *cpus* and *processors*: These generally have multiple cores,
      but informally we'll treat 'core', 'cpu', and 'processor' as
      being equivalent.
  - *hardware threads* / *hyperthreading*: on some processors, each
    core can have multiple hardware threads, which are sometimes
    viewed as separate 'cores'
  - *nodes*: We'll use this term to mean the different machines (computers (machines), each with their own distinct memory, that make up a cluster or supercomputer.

- Process terms
  - *processes*: individual running instances of a program.
    - seen as separate lines in `top` and `ps`
  - *software threads*: multiple paths of execution within a single
    process;the OS sees the threads as a single process, but one can
    think of them as 'lightweight' processes.
    - seen as >100% CPU usage in `top` and `ps`
  - *tasks*: individual computations needing to be done
    - *MPI tasks*: the individual processes run as part of an MPI
    computation
  - *workers*: the individual processes that are carrying out a
    (parallelized) computation (e.g., Python, R, or MATLAB workers
    controlled from the master Python/R/MATLAB process).
 
# High-level considerations

Parallelization:

 - Ideally we have no more (often the same number of) processes or
 processes+threads than the cores on a node.
 - We generally want at least as many computational tasks as cores
   available to us.

Speed:

- Getting data from the CPU cache for processing is fast.
- Getting data from main memory (RAM) is slower.
- Moving data across the network (e.g., between nodes) is much slower, as is reading data
off disk.
  - Infiniband networking between nodes and to /global/scratch is much
    faster than Ethernet networking to login nodes and to  /global/home/users
- Moving data over the internet is even slower.

# Introduction: types of parallelization

## Embarrassingly parallel computation

## Threaded computations

## Multi-process computations

## Distributed computations

## Other kinds of parallel computing

(find some pictures)

 - GPU computation
   - Thousands of slow cores
   - Groups of cores do same computation at same time in lock-step
   - Separate GPU memory
 - Spark/Hadoop
   - Data distributed across disks of multiple machines
   - Each processor works on data local to the machine
   - Spark tries to keep data in memory

# Parallel processing considerations

Often you want to strike the sweet spot between too few 

- Use all the cores on a node fully
  - Have as many worker processes as all the cores available
  - Have at least as many tasks as processes (often many more)
- Only use multiple nodes if you need more cores or more (total)
memory
- Starting up worker processes and sending data involves a
delay (latency)
  - Don't have very many tasks that each run very quickly
- Having tasks with highly variable completion times can lead to poor
  load-balancing (particularly with relatively few tasks)
- Writing code for computations with dependencies is much harder than
  embarrassingly parallel computation

# Submitting and monitoring parallel jobs on Savio (Nicolas)

# Parallelization using existing software (Christopher)

# Embarrassingly parallel computation (Wei)


# How to get additional help

 - For technical issues and questions about using Savio: 
    - brc-hpc-help@berkeley.edu
 - For questions about computing resources in general, including cloud computing: 
    - brc@berkeley.edu
    - (virtual) office hours: Wed. 1:30-3:00 and Thur. 9:30-11:00 
 - For questions about data management (including HIPAA-protected data): 
    - researchdata@berkeley.edu
    - (virtual) office hours: Wed. 1:30-3:00 and Thur. 9:30-11:00

Zoom links for virtual office hours:

 - Wednesday:  [https://berkeley.zoom.us/j/504713509](https://berkeley.zoom.us/j/504713509)
 - Thursday:  [https://berkeley.zoom.us/j/676161577](https://berkeley.zoom.us/j/676161577)

# Upcoming events and hiring

 - Research IT is hiring graduate students as domain
   consultants. Please chat with one of us if interested.
