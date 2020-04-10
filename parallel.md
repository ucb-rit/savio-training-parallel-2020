% Savio parallel processing training
% April 8, 2020
% BRC consultants TBD

# Introduction

We'll do this mostly as a demonstration. We encourage you to login to your account and try out the various examples yourself as we go through them.

Much of this material is based on the extensive Savio documention we have prepared and continue to prepare, available at [http://research-it.berkeley.edu/services/high-performance-computing](http://research-it.berkeley.edu/services/high-performance-computing).

The materials for this tutorial are available using git at the short URL ([https://tinyurl.com/brc-feb20](https://tinyurl.com/brc-apr20)), the  GitHub URL ([https://github.com/ucb-rit/savio-training-parallel-2020](https://github.com/ucb-rit/savio-training-parallel-2020)), or simply as a [zip file](https://github.com/ucb-rit/savio-training-parallel-2020/archive/master.zip).

# Outline


# Introduction

## General Parallelization Strategies
- Vector instructions (AVX2/AVX512)
- Parallelize over CPU cores*
- Parallelize over multiple nodes*

\* focusing on these strategies today

## Common Bottlenecks
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

# Submitting and Monitoring Jobs

## Available Hardware
- Partitions
  - savio (Intel Xeon E5-2670 v2): 164 nodes, 20 CPU cores each (Supports AVX2 instructions)
  - savio2 (Intel Xeon E5-2670 v3): 136 nodes, 24 CPU cores each (Supports AVX2 instructions)
  - and others...
- See the [Savio User Guide](https://research-it.berkeley.edu/services/high-performance-computing/user-guide/savio-user-guide) for more details.

## Slurm Scheduler
Slurm is a job scheduler which allows you to request resources and queue your job to run when available.

### Slurm Environment Variables (for parellelism)
Slurm provides various environment variables that your program can read that may be useful for managing how to distribute tasks. These are taken from the full list of Slurm environment variables listed on the [Slurm sbatch documentation](https://slurm.schedmd.com/sbatch.html).

- `$SLURM_NNODES` - Total number of nodes in the job's resource allocation. 
- `$SLURM_NODELIST` - List of nodes allocated to the job. 
- `$SLURM_JOB_CPUS_PER_NODE` - Count of processors available to the job on this node.
- `$SLURM_CPUS_PER_TASK` - Number of cpus requested per task.

## Submitting Parallel Jobs

Examples taken from: [Running your Jobs](https://research-it.berkeley.edu/services/high-performance-computing/running-your-jobs)

### OMP Job
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
#QoS:
#SBATCH --qos=qos_name
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

### OpenMPI job
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
# QoS:
#SBATCH --qos=qos_name
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


## Monitoring Jobs
How do I know if my job is using resources efficiently?

### While job is running
Using `srun` and `htop`:
```bash
srun -j $JOB_ID
uptime # check the load

# use htop for a visual representation of CPU usage
module load htop
htop
```

Using warewulf:
```bash
wwall -j $JOB_ID
```

### After the job has run
```bash
sacct -j $JOB_ID --format JobID,TotalCPU,CPUTime,NCPUs,Start,End
```
Not perfectly accurate, since it measures only the parent process of your job (not child processes). Ideally, `TotalCPU` will be as close as possible to `CPUTime`.

# How to get additional help

 - For technical issues and questions about using Savio: 
    - brc-hpc-help@berkeley.edu
 - For questions about computing resources in general, including cloud computing: 
    - brc@berkeley.edu
    - office hours: Wed. 1:30-3:00 and Thur. 9:30-11:00 here in AIS
 - For questions about data management (including HIPAA-protected data): 
    - researchdata@berkeley.edu
    - office hours: Wed. 1:30-3:00 and Thur. 9:30-11:00 here in AIS

# Upcoming events and hiring

 - Research IT is hiring graduate students as domain consultants. See flyers or talk to one of us.
