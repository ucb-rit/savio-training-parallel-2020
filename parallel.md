% Savio parallel processing training
% April 21, 2020
% Nicolas Chan, Wei Feinstein, Christopher Hann-Soden, Chris Paciorek

# Introduction

We'll do this mostly as a demonstration. We encourage you to login to your account and try out the various examples yourself as we go through them.

Much of this material is based on the extensive Savio documention we
have prepared and continue to prepare, available at our new
documentation site: [https://docs-research-it.berkeley.edu/services/high-performance-computing](https://docs-research-it.berkeley.edu/services/high-performance-computing) as well as our old site: [http://research-it.berkeley.edu/services/high-performance-computing](http://research-it.berkeley.edu/services/high-performance-computing).

The materials for this tutorial are available using git at the short URL ([https://tinyurl.com/brc-apr20](https://tinyurl.com/brc-apr20)), the  GitHub URL ([https://github.com/ucb-rit/savio-training-parallel-2020](https://github.com/ucb-rit/savio-training-parallel-2020)), or simply as a [zip file](https://github.com/ucb-rit/savio-training-parallel-2020/archive/master.zip).

# Outline

 - Introduction (Chris)
   - Hardware
   - Parallel processing terms and concepts
   - Approaches to parallelization
     - Embarrassingly parallel computation
	 - Threaded computations
	 - Multi-process computations
   - Considerations in parallelizing your work
 - Submitting and monitoring parallel jobs on Savio (Nicolas)
   - Job submission flags
   - MPI- and openMP- based submission examples
   - Monitoring jobs to check parallelization
 - Parallelization using existing software (Christopher)
   - How to look at documentation to understand parallel capabilities
   - Specific examples
 - Embarrassingly parallel computation (Wei)
   - GNU parallel
   - Job submission details
 - Parallelization in Python, R, and MATLAB (Chris; time permitting)
   - Dask and ipyparallel in Python
   - future and other packages in R
   - parfor in MATLAB

# Introduction: Savio

Savio is a cluster of hundreds of computers (aka 'nodes'), each with many CPUs
(cores), networked together. 

<center><img src="figures/savio_diagram.jpeg"></center>

# Introduction: multi-core computers

Each computer has its own memory and multiple (12-56) cores per
machine.

<center><img src="figures/generic_machine.jpeg"></center>

savio2 nodes: two Intel Xeon 12-core Haswell processors (24 cores per
node (a few have 28))

So a cartoon representation of a cluster like Savio is like [this](https://waterprogramming.wordpress.com/2017/07/21/developing-parallelised-code-with-mpi-for-dummies-in-c-part-12/).

# Introduction: Terms and concepts

- Hardware terms
  - **cores**: We'll use this term to mean the different processing
    units available on a single node. All the cores share main memory.
    - **CPUs** and **processors**: These generally have multiple cores,
      but informally we'll treat 'core', 'cpu', and 'processor' as
      being equivalent.
    - **hardware threads** / **hyperthreading**: on some processors, each
    core can have multiple hardware threads, which are sometimes (but
    not on Savio)  viewed as separate 'cores'
  - **nodes**: We'll use this term to mean the different machines (computers), each with their own distinct memory, that make up a cluster or supercomputer.

- Process terms
  - **processes**: individual running instances of a program.
    - seen as separate lines in `top` and `ps`
  - **software threads**: multiple paths of execution within a single
    process; the OS sees the threads as a single process, but one can
    think of them as 'lightweight' processes.
    - seen as >100% CPU usage in `top` and `ps`
  - **workers**: the individual processes that are carrying out a
    (parallelized) computation (e.g., Python, R, or MATLAB workers
    controlled from the master Python/R/MATLAB process).
  - **(computational) tasks**: individual computations needing to be done
    - easily confused with **MPI tasks**: the individual processes run
    as part of an MPI computation.
	- easily confused with **SLURM tasks**: the number of individual
    processes you plan to run. 


# Introduction: High-level considerations

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
  - Infiniband networking between compute nodes and to /global/scratch is much
    faster than Ethernet networking to login nodes and to  /global/home/users
- Moving data over the internet is even slower.


# Introduction: Common Bottlenecks

- Constrained by memory (RAM) bandwidth
  - For example, each thread is loading lots of data into memory
- Constrained by filesystem bandwidth
  - For example, 10 nodes all trying to read the same large file on scratch
- [Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law): Your task must take at least as long as the sequential part.
  - For example, if every task has to load a Python library that takes 10 seconds, then your job will take at least 10 seconds. If not all the tasks are running at the same time, then it will take much more than that.
  
Possible solutions:
  
 - Fewer tasks per node will reduce strain on memory
   - You would still be given exclusive access to the node (and charged for that), so there will be a tradeoff here with the cost. It's possible running fewer tasks will give you better performance so you take less time and save money, but you are also running fewer tasks at a time. The sweet spot will depend on your particular task.
 - Reduce number of filesystem operations
 - Find ways to reduce sequential bottlenecks

# Introduction: Types of parallelization

- Embarrassingly parallel computation of multiple jobs on one or more nodes*
- Parallelize one job over CPU cores*
- Parallelize one job over multiple nodes*
- Vector instructions (AVX2/AVX512) allow vectorized arithmetic on recent
  Intel CPUs (e.g., savio2, savio3 nodes)

\* focusing on these strategies today

# Types of parallelization: Embarrassingly parallel computation

Aka: naturally, pleasingly, perfectly parallel

You have a certain number of computational tasks to carry out and
there are no dependencies between the tasks.

  - Naturally parallel
  - Pleasingly parallel
  - Perfectly parallel

E.g., process multiple datasets, or do a parameter sweep over multiple
parameter sets.

Tools:

   - [GNU parallel](https://www.gnu.org/software/parallel/parallel_tutorial.html#GNU-Parallel-Tutorial) (standard Linux tool)*
   -
   [ht_helper (Savio-specific tool)](https://research-it.berkeley.edu/services/high-performance-computing/user-guide/hthelper-script)
   - SLURM job arrays (careful, one job per node...)

\* focusing on this approach today

# Types of parallelization: Threaded computations

- Single process controls execution
- Use of code libraries that allow the process to split a computation
(see [this OpenMP example](demos/openmp_example.c)
across multiple software threads (still one process)
```
  PID  USER  PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                                                  
15876 zhang  20   0 17.321g 0.015t  91828 S 410.6  5.9  14158:58 python                                                   
```
- Threads share memory and data structures (beware 'race' conditions)
- Single node ONLY!

<center><img src="figures/threads.gif"></center>

(Image provided by [https://computing.llnl.gov/tutorials/openMP](https://computing.llnl.gov/tutorials/openMP).)

# Types of parallelization: Threaded computations (part 2)

Examples in standard software:

 - MATLAB threads some computations behind the scenes
   - vectorized calculations
   - linear algebra (MKL)
 - If set up appropriately (true on Savio), R and Python rely on
threaded linear algebra (OpenBLAS)

Rolling your own:

- OpenMP (for C/C++/Fortran)
- pthreads (for C/C++)
- Intel threaded building blocks (TBB) (for C++)

# Types of parallelization: Multi-process computations

Standard software (e.g., Python, R, MATLAB) allow you to start up
multiple workers and farm out independent computations.

- Master process controls execution
- Workers are separate processes
```
  PID USER      PR  NI    VIRT    RES    SHR S  %CPU %MEM     TIME+ COMMAND                                                  
21718 lin-er    20   0 1171176 930020   4704 R 100.0  0.7   1:18.90 R                                                        
21729 lin-er    20   0 1173352 931888   4524 R 100.0  0.7   1:05.89 R                                                        
21714 lin-er    20   0 1189080 947924   4704 R 100.0  0.7   1:18.95 R                                                        
21715 lin-er    20   0 1151192 909984   4704 R 100.0  0.7   1:18.97 R                                                        
21716 lin-er    20   0 1174212 933056   4704 R 100.0  0.7   1:18.93 R                                                        
```
- Often have more computational tasks than workers
- Examples:
  - Python: Dask, ipyparallel, ray
  - R: future, foreach, parallel::parLapply
  - MATLAB: parfor
- Easy to run on one node with limited (1-2 lines of code) setup
- Many of these can run across multiple nodes but require **user** to
  set things up (see examples in last section of this material).

# Types of parallelization:  Distributed computations

Traditional high-performance computing (HPC) runs a large computation
by (carefully) splitting the computation amongst communicating MPI
workers (MPI 'tasks' or 'ranks').

```bash
$ mpicc mpi_example.c -o mpi_example
$ mpirun -np 20 mpi_example
# Hello from MPI process 2 out of 20 on savio2.n0070
# Hello from MPI process 0 out of 20 on savio2.n0096
# Hello from MPI process 18 out of 20 on savio2.n0070
# Hello from MPI process 7 out of 20 on savio2.n0098
# <snip>
```

Comments:

 - multiple (e.g., 20 above) copies of the same executable are run at
 once (SPMD)
 - code behaves differently based on the ID ('rank') of the process
 - processes communicate by sending 'messages'
 - MPI can be used on a single node if desired.
 - OpenMPI is the standard MPI library but there are others
 - Can run threaded code within MPI processes

# Introduction: Other kinds of parallel computing

 - GPU computation
   - Thousands of slow cores
   - Groups of cores do same computation at same time in lock-step
   - Separate GPU memory
   - Users generally don't code for a GPU directly but use packages such as
   Tensorflow or PyTorch
   - Multi-GPU computation has some commonalities with multi-node MPI work
 - Spark/Hadoop
   - Data distributed across disks of multiple machines
   - Each processor works on data local to the machine
   - Spark tries to keep data in memory

# Parallel processing considerations

- Use all the cores on a node fully.
  - Have as many worker processes as all the cores available.
  - Have at least as many computational tasks as processes (often many more).
- Use multiple nodes if you need more cores or more (total)
memory.
- Starting up worker processes and sending data involves a
delay (latency).
  - Don't have very many tasks that each run very quickly.
  - Don't send many small chunks of data.
- Having tasks with highly variable completion times can lead to poor
  load-balancing (particularly with relatively few tasks).
- Writing code for computations with dependencies is much harder than
  embarrassingly parallel computation.


# Submitting and Monitoring Jobs

# Submitting jobs: Available Hardware
- Partitions
  - savio (Intel Xeon E5-2670 v2): 164 nodes, 20 CPU cores each (Supports AVX2 instructions)
  - savio2 (Intel Xeon E5-2670 v3): 136 nodes, 24 CPU cores each (Supports AVX2 instructions)
  - and others...
- See the [Savio User Guide](https://research-it.berkeley.edu/services/high-performance-computing/user-guide/savio-user-guide#Hardware) for more details.

# Submitting jobs: Slurm Scheduler
Slurm is a job scheduler that allows you to request resources and queue your job to run when available.

## Slurm Environment Variables (for parellelism)
Slurm provides various environment variables that your program can read that may be useful for managing how to distribute tasks. These are taken from the full list of Slurm environment variables listed on the [Slurm sbatch documentation](https://slurm.schedmd.com/sbatch.html).

- `$SLURM_NNODES` - Total number of nodes in the job's resource allocation. 
- `$SLURM_NODELIST` - List of nodes allocated to the job. 
- `$SLURM_JOB_CPUS_PER_NODE` - Count of processors available to the job on this node.
- `$SLURM_CPUS_PER_TASK` - Number of cpus requested per task.

# Submitting Parallel Jobs

Examples taken from: [Running your Jobs](https://research-it.berkeley.edu/services/high-performance-computing/running-your-jobs)

## OpenMP Job
Notice that we set `--cpus-per-task` and then access the environment variable to set the OMP number of threads to use. If you have another way of doing multithreaded tasks, you can use the same `$SLURM_CPUS_PER_TASK` environment variable.
```bash
#!/bin/bash
# Job name:
#SBATCH --job-name=test
#
# Account:
#SBATCH --account=account_name
#
# Partition:
#SBATCH --partition=partition_name
#
# Request one node:
#SBATCH --nodes=1
#
# Specify one task:
#SBATCH --ntasks-per-node=1
#
# Number of processors for single task needed for use case (example):
#SBATCH --cpus-per-task=4
#
# Wall clock limit:
#SBATCH --time=00:00:30
#
## Command(s) to run (example):
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
./a.out
```

## OpenMPI job
Notice we request 2 nodes and have 20 tasks per node. We could also leave out the number of nodes requested and simply say 40 tasks, and then Slurm would know we need 2 nodes since we said to use 1 CPU per task.
```bash
#!/bin/bash
# Job name:
#SBATCH --job-name=test
#
# Account:
#SBATCH --account=account_name
#
# Partition:
#SBATCH --partition=partition_name
#
# Number of nodes needed for use case:
#SBATCH --nodes=2
#
# Tasks per node based on number of cores per node (example):
#SBATCH --ntasks-per-node=20
#
# Processors per task:
#SBATCH --cpus-per-task=1
#
# Wall clock limit:
#SBATCH --time=00:00:30
#
## Command(s) to run (example):
module load gcc openmpi
mpirun ./a.out
```


# Monitoring Jobs
How do I know if my job is using resources efficiently?

### While job is running
Using `srun` and `htop`:

```bash
srun --jobid=$JOB_ID --pty bash -i
uptime # check the load

# use htop for a visual representation of CPU usage
module load htop
htop
```

Using warewulf (might not be working):
```bash
wwall -j $JOB_ID
```

Using [metacluster](http://metacluster.lbl.gov/warewulf) (imprecise but can give general idea if you know which nodes you're on):

### After the job has run
```bash
sacct -j $JOB_ID --format JobID,TotalCPU,CPUTime,NCPUs,MaxRSS,Start,End
```
Not perfectly accurate, since it measures only the parent process of your job (not child processes). Ideally, `TotalCPU` will be as close as possible to `CPUTime`.

# Parallelization using existing software

Many times you simply want to use an existing tool to perform an analysis. Parallelization depends on how the developer designed the software, and ease of use usually depends on how well documented the software is.

There are three main ways in which parallelization parameters are set:

- command line arguments
- compilation options that produce separate executables
- configuration files

# Command line arguments

Usually command line tools have arguments to set the level of parallelization. e.g.

- `-t`  "threads"
- `-p`  "processes"
- `-n`  "number of processes/threads"
- `-c`  "cores"

# Bowtie2

Bowtie2 is a popular read aligner used in bioinformatics. Next generation sequencing tools often produce millions or billions of short sequences, or "reads". Figuring out which part of the genome these reads came from is a common task called "alignment". This task is highly parallelizable because (once an index is made) aligning each read can be done independently.

From the Manual, under Building from source:

> By default, Bowtie 2 uses the Threading Building Blocks library (TBB) for this. [If TBB is not available] Bowtie 2 can be built with make NO_TBB=1 to use pthreads or Windows native multithreading instead.

From the manual, under Performance Options:

```bash
-p/--threads NTHREADS
```

> Launch NTHREADS parallel search threads (default: 1). Threads will run on separate processors/cores and synchronize when parsing reads and outputting alignments. Searching for alignments is highly parallel, and speedup is close to linear. Increasing -p increases Bowtie 2’s memory footprint. E.g. when aligning to a human genome index, increasing -p from 1 to 8 increases the memory footprint by a few hundred megabytes. This option is only available if bowtie is linked with the pthreads library (i.e. if BOWTIE_PTHREADS=0 is not specified at build time).

# Bowtie2 uses multithreading:

- Can use all the cores on a node easily
- Can not be run across multiple nodes
- Further parallelization will require splitting up the inputs & merging results after

# BLAST

The Basic Local Alignment Search Tool (BLAST) is another very common alignment tool designed not to find which location in a genome a short sequence comes from but to identify the origin of a larger sequence from a database of all known sequences.

BLASTing many queries

- BLAST takes input files with multiple queries
- Some speedup is achieved by batch searching - multiple queries are scanned against the DB at once
- Batching can increase memory use

Buried in the appendices of the BLAST documentation is this option:

```bash
-num_threads
```

> Number of threads (CPUs) to use in blast search.

The implementation here is not well documented, but it's safe to assume this means threading with shared memory, and thus won't work across nodes. Still, a few quick tests shows that [the `-num_threads` option results in a non-linear speedup that quickly levels off around -num_threads 4.](https://voorloopnul.com/blog/how-to-correctly-speed-up-blast-using-num_threads/)

# BLAST is an excellent candidate for GNU parallel or ht_helper.

- covered in the next section
- splitting your queries and running multiple instances of BLAST is faster than the -num_threads option

# GATK

The Genome Analysis Tool Kit is a tool for making statistical inferences about genotypes or gene frequencies from sets of alignments like those produced by Bowtie2. The GATK manual is very large (many different tools), and parralelization documentation doesn't jump out. Fortunately, GATK has a [large helpful community producing guides.](https://gatkforums.broadinstitute.org/gatk/discussion/1975/how-can-i-use-parallelism-to-make-gatk-tools-run-faster)

GATK uses different terminology

 - Machines vs Nodes
 - "data threads" and "cpu threads"
 - scatter-gather (general technique) to describe multi-node processing (paradigm)

The key options, usable in some tools, are

```bash
-nt / --num_threads
```

> controls the number of data threads sent to the processor

```bash
-nct / --num_cpu_threads_per_data_thread
```

> controls the number of CPU threads allocated to each data thread

Reading the guides, `-nt` duplicates the data in memory because `-nt` "threads" cannot share memory, while `-nct` threads use shared memory. This paradigm is sometimes refered to as processes/threads, rather than data-threads/cpu-threads.

# GATK has multiple levels of parallelization

- Different tools
- Different resource needs
- Different recommended configurations

NCT = Threads (Shared memory)   
NT = "data threads" (Indpendent memory)   
SG = "scatter gather" (Multiple nodes)*    

<table class="table table-striped table-bordered table-condensed"><thead><tr><th align="left">Tool</th>
<th align="left">Full name</th>
<th align="left">Type of traversal</th>
<th align="center">NT</th>
<th align="center">NCT</th>
<th align="center">SG</th>
</tr></thead><tbody><tr><td align="left">RTC</td>
<td align="left">RealignerTargetCreator</td>
<td align="left">RodWalker</td>
<td align="center">+</td>
<td align="center">-</td>
<td align="center">-</td>
</tr><tr><td align="left">IR</td>
<td align="left">IndelRealigner</td>
<td align="left">ReadWalker</td>
<td align="center">-</td>
<td align="center">-</td>
<td align="center">+</td>
</tr><tr><td align="left">BR</td>
<td align="left">BaseRecalibrator</td>
<td align="left">LocusWalker</td>
<td align="center">-</td>
<td align="center">+</td>
<td align="center">+</td>
</tr><tr><td align="left">PR</td>
<td align="left">PrintReads</td>
<td align="left">ReadWalker</td>
<td align="center">-</td>
<td align="center">+</td>
<td align="center">-</td>
</tr><tr><td align="left">RR</td>
<td align="left">ReduceReads</td>
<td align="left">ReadWalker</td>
<td align="center">-</td>
<td align="center">-</td>
<td align="center">+</td>
</tr><tr><td align="left">HC</td>
<td align="left">HaplotypeCaller</td>
<td align="left">ActiveRegionWalker</td>
<td align="center">-</td>
<td align="center">(+)</td>
<td align="center">+</td>
</tr><tr><td align="left">UG</td>
<td align="left">UnifiedGenotyper</td>
<td align="left">LocusWalker</td>
<td align="center">+</td>
<td align="center">+</td>
<td align="center">+</td>
</tr></tbody></table>

# Scatter Gather in GATK

- GATK supports use of WDL (Workflow Description Language) to script multi-node capable processing
- this is a scripting language to generate multiple GATK calls
- probably easier to use GNU parallel for multi-node parallelism

# Compilation options/Separate executables

Some software can use either multithreading or MPI.

- MPI implementation requires additional libraries (e.g. OpenMPI)
- this functionality is toggled on/off at compilation

# IQ-TREE

IQ-TREE is a phylogenetics package that makes a maximum-likelihood estimation of the evolutionary history of a set of sequences (i.e. an evolutionary tree).

```bash
-nt
```

> Specify the number of CPU cores for the multicore version. A special option `-nt` AUTO will tell IQ-TREE to automatically determine the best number of cores given the current data and computer.

Some testing will probably be necessary to learn how memory usage and runtime scale with more threads, but the AUTO parameter is a nice convenience feature implemented by some developers.

There is also an MPI version which must be compiled seperately, creating a second binary "iqtree-mpi".

```bash
module load gcc
module load openmpi
cmake -DIQTREE_FLAGS=mpi ..
```

The multicore version is very easy to use on a single node, but large analyses must use the MPI version.

# Config Files & Environment Variables

Sometimes the parallelization settings are set in configuration files or in environment variables, rather than as arguments to the execution call.

# Abaqus

Abaqus is a popular finite element analysis software. Physicist, engineers, and others use this software to test when their designs will break or light on fire, among other things.

`abaqus_v6.env` is a Python syntax config file that is read when Abaqus runs.

- cpus
- gpus
- memory
- mp_mode

# Embarrassingly parallel computation

### Let's blast to align protein sequences 

```
[user@n0002 BRC]$ cat blast.sh 
blastp -query protein1.faa -db db/img_v400_PROT.00 -out *protein1.seq
blastp -query protein2.faa -db db/img_v400_PROT.00 -out protein2.seq 
blastp -query protein3.faa -db db/img_v400_PROT.00 -out protein3.seq
```
### Parallel on one compute node 
```
blastp -query protein1.faa -db db/img_v400_PROT.00 -out protein1.seq &
blastp -query protein2.faa -db db/img_v400_PROT.00 -out protein2.seq &
blastp -query protein3.faa -db db/img_v400_PROT.00 -out protein3.seq &
wait
```
### What about more than one nodes
```
ssh -n node1 "blastp -query protein1.faa -db db/img_v400_PROT.00 -out protein1.seq" &
ssh -n node1 "blastp -query protein1.faa -db db/img_v400_PROT.00 -out protein1.seq" &
...
ssh -n node2 "blastp -query protein1.faa -db db/img_v400_PROT.00 -out protein1.seq" &
```
### Blast with GNU parallel
`parallel -a blast.sh`

# What is GNU parallel
- A shell tool for executing independent jobs in parallel using one or more computers. 
- Dynamically distribute the commands across all of the nodes and cores being requested. 
- A job can be a single command or a small script 
- See the [GNU Parallel User Guide](https://www.gnu.org/software/parallel/) for more details.
  
### GNU parallel command line
- A job can be a single command 
    - parallel [options] [command [arguments]] < list_of_arguments
- A script that has to be run for each of the lines in the input
    - parallel [options] [command [arguments]] (::: arguments|:::: argfile(s)| -a task.list)

# A typical use case: single application fed with different parameter sets
### from the command line:
   - parallel [OPTIONS] COMMAND {} ::: TASKLIST   
   - **{}**: parameter holder which is automatically replaced with one line from the tasklist.
```
[user@n0002 BRC]$ parallel echo {} ::: a b c
   a
   b
   c   
   
   [user@n0002 BRC]$ parallel --link echo {1}{2} ::: a b c ::: 1 2 3
   a 1
   b 2   
   c 3
   
   [user@n0002 BRC]$ parallel echo {} ::: `seq 3`
   1
   2
   3
```
### from an input file
    - parallel [OPTIONS] COMMAND {} :::: TASKLIST.LST
    - parallel –a TASKLIST.LST [OPTIONS] COMMAND {} 
```
[user@n0002 BRC]$ parallel echo {} :::: blast.sh 

[user@n0002 BRC]$ parallel -a blast.sh echo {}
blastp -query protein1.faa -db db/img_v400_PROT.00 -out protein1.seq 
blastp -query protein2.faa -db db/img_v400_PROT.00 -out protein2.seq 
blastp -query protein3.faa -db db/img_v400_PROT.00 -out protein3.seq
```
# Examples

**Task parameters and command options** 
```
[user@n0002 BRC]$ cat hostname.sh
		 #!/bin/bash
		 echo "using input: $1 $2"
		 echo `hostname` "copy input to output " >$2 ; cat $1 >> $2 
		 
[user@n0002 BRC]$ cat input.lst
		 input/test0.input
   		 input/test1.input
		 ...
		 
[user@n0002 BRC]$ parallel -j 4 -a input.lst ./hostname.sh {} output/{./}.out
```
- Whereas
   	- -j: job# per node, 0: launch as much as core# permits.
	- -a: task input list
	- {}: 1st parameter to hostname.sh, taking one line from input.lst per task
	- {./} remove input file extension and path
	- output/{./}.out: 2nd parameter to hostname.sh		

**More command options**

```
[user@n0002 BRC]$  parallel --slf hostfile --wd $WORKDIR --joblog runtask.log --resume --progres --jobs 4 -a input.lst sh hostname.sh {} output/{./}.out
```

	- --slf: sshloginfile (node list)
	- --wd: workdir, default is $HOME
	- --joblog: log of completed tasks
	- --resume: resume from previous unfinished task 
	- --progress: display task progress as standard output


# logfile
```
[wfeinstein@n0002 BRC]$ head -3 runtask.log
Seq	Host	Starttime	JobRuntime	Send	Receive	Exitval	Signal	Command
10	:	1586815193.782	     0.043	0	48	0	0	sh hostname.sh input/test9.input output/test9.out
2	:	1586815193.757	     0.094	0	48	0	0	sh hostname.sh input/test1.input output/test1.out
```
Logfile pairs with the resume option. Note the logfile has to be
removed should you rerun the parameter set at debugging state

# Example: input from a command list 

```
[user@n0002 BRC]$ cat commands.lst 
	echo "host = " '`hostname`'
	sh -c "echo today date = ; date" 
	echo "ls = " `ls`
	...
	
[user@n0002 BRC] parallel -j 0 < commands.lst
host =  ln002.brc
today date = Tue Apr 14 22:51:17 PDT 2020
...
```

# Example: MPI applications using GNU Parallel
- Traditional MPI job
```	
[user@n0002 BRC]$ mpirun -np 2 ./hello_rank 1 
Hello1 from processor n0030.es1, rank 0 out of 2 processors
Hello1 from processor n0030.es1, rank 1 out of 2 processors

[user@n0002 BRC]$ time for index in `seq 40`; do  mpirun -np 2 ./a.out $index; done
Hello1 from processor n0030.es1, rank 0 out of 2 processors
Hello1 from processor n0030.es1, rank 1 out of 2 processors
Hello2 from processor n0030.es1, rank 0 out of 2 processors
Hello2 from processor n0030.es1, rank 1 out of 2 processors
...
real	0m11.473s
user	0m3.486s
sys	0m7.072s
```
- launch independent MPI tasks in parallel 
```
[user@n0002 BRC]$ time parallel -j 10 mpirun -np 2 ./hello_rank ::: `seq 40`
Hello2 from processor n0030.es1, rank 1 out of 2 processors
Hello2 from processor n0030.es1, rank 0 out of 2 processors
Hello5 from processor n0030.es1, rank 1 out of 2 processors
Hello5 from processor n0030.es1, rank 0 out of 2 processors
Hello1 from processor n0030.es1, rank 0 out of 2 processors
Hello1 from processor n0030.es1, rank 1 out of 2 processors
...
real	0m3.565s
user	0m3.208s
sys	0m9.577s
```
# Job submission sample
We request 2 nodes as the showcase. Number of nodes to request depends on the the tasklist size. 

```
#!/bin/bash
#SBATCH --job-name=gnu-parallel
#SBATCH --account=account_name
#SBATCH --partition=partition_name
#SBATCH --nodes=2
#SBATCH --time=2:00:00
## Command(s) to run (example):

module load gnu-parallel/2019.03.22
export WORKDIR="/your/path"
export JOBS_PER_NODE=8
echo $SLURM_JOB_NODELIST |sed s/\,/\\n/g > hostfile
cd $WORKDIR

PARALLEL="parallel --progress -j $JOBS_PER_NODE --slf hostfile --wd $WORKDIR --joblog runtask.log --resume"
$PARALLEL -a input.lst sh hostname.sh {} output/{/.}.out    
```
# Parallelization in Python, R, and MATLAB

- Support for threaded computations:

  - Python: threaded linear algebra when linked to a parallel BLAS (e.g., OpenBLAS)
  - R: threaded linear algebra when linked to a parallel BLAS (e.g., OpenBLAS)
  - MATLAB: threaded linear algebra via MKL plus automatic threading of
various functions

- Support for multi-process parallelization

  - Python
    - Parallel map operations via  *ipyparallel*, *Dask*, other packages
    - Distributed data structures and calculations via *Dask*
  - R
    - Parallel for loops with *foreach* (via *doParallel*, *doFuture*, *doMPI*, *doSNOW*)
    - parallel map operations with `future.apply::future_lapply`, `parallel::parLapply`, `parallel::mclapply`
  - MATLAB: Parallel for loops via `parfor`

# Dask and ipyparallel in Python

Single node parallelization:

|Python package|key functions|details|
|------|-------|-------|
|Dask|futures or `map`| 'processes' or 'distributed' schedulers|
|Dask|distributed data structures (arrays, dfs, bags)|various schedulers|
|ipyparallel|`apply` or `map`|start workers via `ipcluster`|

Multi-node parallelization:

|Python package|key functions|details|
|------|-------|-------|
|Dask|futures or `map`| 'distributed' scheduler, start workers in shell|
|Dask|distributed data structures (arrays, dfs, bags)|see above|
|ipyparallel|`apply` or `map`|start workers via `ipcontroller` + `srun ipengine`|

See these materials for details:

- [Dask](https://github.com/berkeley-scf/tutorial-dask-future)
- [ipyparallel](https://research-it.berkeley.edu/services/high-performance-computing/using-python-savio#Parallel-Processing)


# Multi-node parallelization in Python via Dask

Example SLURM script:

```
#!/bin/bash
#SBATCH --partition=savio2
#SBATCH --account=account_name
#SBATCH --ntasks=48
#SBATCH --time=00:20:00
module load python/3.6
export SCHED=$(hostname)
dask-scheduler&
sleep 30
# Start one worker per SLURM 'task' (i.e., core)
srun dask-worker tcp://${SCHED}:8786 &   # might need ${SCHED}.berkeley.edu
sleep 60
```

Example Python code:

```
 # Connect to the cluster via the scheduler.
import os, dask
from dask.distributed import Client
c = Client(address = os.getenv('SCHED') + ':8786')
n = 100000000
p = 96

 # example use of futures
futures = [dask.delayed(calc_mean)(i, n) for i in range(p)]
results = dask.compute(*futures)

 # example use of map()
inputs = [(i, n) for i in range(p)]
future = c.map(calc_mean_vargs, inputs)
results = c.gather(future)
```


# future and other packages in R

Single node parallelization:

|R package|key functions|details|
|------|-------|-------|
|future|`future.apply::future_lapply`| 'multiprocess' plan|
|future|`foreach` + `doFuture`|'multiprocess' plan|
|foreach|`foreach`|use `doParallel`|
|parallel|`parLapply`|use `makeCluster`|
|parallel|`mclapply`|only on Linux / MacOS as uses forking|

Multi-node parallelization:

|R package|key functions|details|
|------|-------|-------|
|future|`future.apply::future_lapply`| 'cluster' plan|
|future|`foreach` + `doFuture`|'cluster' plan|
|foreach|`foreach`|use `doSNOW` or `doMPI`|
|parallel|`parLapply`|use `makeCluster` with multiple hosts|

See these tutorials for details:

- [future](https://github.com/berkeley-scf/tutorial-dask-future)
- [single node parallelization](https://github.com/berkeley-scf/tutorial-parallel-basics)
- [multiple node parallelization](https://github.com/berkeley-scf/tutorial-parallel-distributed)


# Multi-node parallelization in R via future

Example SLURM script:

```
#!/bin/bash
#SBATCH --partition=savio2
#SBATCH --account=account_name
#SBATCH --ntasks=48
#SBATCH --time=00:20:00
module load r
module load r-packages # often useful
R CMD BATCH --no-save run.R run.Rout
```

Example R code:

```
library(future)
workers <- system('srun hostname', intern = TRUE)
cl <- parallel::makeCluster(workers)
plan(cluster, workers = cl)

 # example use of parallel sapply 
 # This example simply verifies we're actually connected to the workers.
future_sapply(seq_along(workers), function(i) system('hostname', intern = TRUE))

 # example use of foreach
library(doFuture)
results <- foreach(i = 1:200) %dopar% {
   # your code here
}
```

Note: One can also directly pass the vector of worker names to the `workers` argument of `plan()`, which should invoke `future::makeClusterPSOCK`, but I was having trouble with that hanging on Savio at one point.


# parfor in MATLAB on one node

Example job script:

```
#!/bin/bash
#SBATCH --partition=savio2
#SBATCH --account=account_name
#SBATCH --cpus-per-task=24
#SBATCH --time=00:20:00
module load matlab
matlab -nodisplay -nosplash -nodesktop -r run.m
```

Example MATLAB code:

```
parpool(str2num(getenv('SLURM_CPUS_PER_TASK')));
parfor i = 1:n
 % computational code here
end
```


# parfor in MATLAB on multiple nodes

- See
[these instructions for MATLAB version 2017b](https://research-it.berkeley.edu/services/high-performance-computing/using-matlab-savio/running-matlab-jobs-across-multiple-savio)
   - limited to 32 workers (but each worker can do threaded
   computations)
- For use with MATLAB 2019b, please email us.
   - no limit on the number of workers


# How to get additional help

 - For technical issues and questions about using Savio: 
    - brc-hpc-help@berkeley.edu
 - For questions about computing resources in general, including cloud computing: 
    - brc@berkeley.edu
    - (virtual) office hours: Wed. 1:30-3:00 and Thur. 9:30-11:00 
 - For questions about data management (including HIPAA-protected data): 
    - researchdata@berkeley.edu
    - (virtual) office hours: Wed. 1:30-3:00 and Thur. 9:30-11:00

Zoom links for virtual office hours: [https://research-it.berkeley.edu/programs/berkeley-research-computing/research-computing-consulting](https://research-it.berkeley.edu/programs/berkeley-research-computing/research-computing-consulting)

# Upcoming events and hiring

 - Research IT is hiring graduate students as domain
   consultants. Please chat with one of us if interested.
