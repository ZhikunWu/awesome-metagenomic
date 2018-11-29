
##  [RepeatModeler](https://github.com/rmhubley/RepeatModeler)

#### install RepeatModeler

```
$ conda install -c bioconda repeatmodeler
```

Arguments:
```
$ RepeatModeler
No database indicated

NAME
    RepeatModeler - Model repetitive DNA

SYNOPSIS
      RepeatModeler [-options] -database <XDF Database>

DESCRIPTION
    The options are:

    -h(elp)
        Detailed help

    -database
        The prefix name of a XDF formatted sequence database containing the
        genomic sequence to use when building repeat models. The database
        may be created with the WUBlast "xdformat" utility or with the
        RepeatModeler wrapper script "BuildXDFDatabase".

    -engine <abblast|wublast|ncbi>
        The name of the search engine we are using. I.e abblast/wublast or
        ncbi (rmblast version).

    -pa #
        Specify the number of shared-memory processors available to this
        program. RepeatModeler will use the processors to run BLAST searches
        in parallel. i.e on a machine with 10 cores one might use 1 core for
        the script and 9 cores for the BLAST searches by running with "-pa
        9".

    -recoverDir <Previous Output Directory>
        If a run fails in the middle of processing, it may be possible
        recover some results and continue where the previous run left off.
        Simply supply the output directory where the results of the failed
        run were saved and the program will attempt to recover and continue
        the run.

    -srand #
        Optionally set the seed of the random number generator to a known
        value before the batches are randomly selected ( using Fisher Yates
        Shuffling ). This is only useful if you need to reproduce the sample
        choice between runs. This should be an integer number.

SEE ALSO
        RepeatMasker, WUBlast

COPYRIGHT
     Copyright 2005-2017 Institute for Systems Biology

AUTHOR
     Robert Hubley <rhubley@systemsbiology.org>
     Arian Smit <asmit@systemsbiology.org>

```

#### first you should create the database for fasta using **BuildDatabase**
```
$ BuildDatabase -name assembly/ERR2259150/assembly  assembly/ERR2259150/assembly.fasta

Building database ERR2259150_db:
  Adding assembly/ERR2259150/assembly.fasta to database
Number of sequences (bp) added to database: 114 ( 2396359 bp )

```

out files:
```
-rw-r--r-- 1 4.1K Nov  9 01:48 ERR2259150_db.nhr
-rw-r--r-- 1 1.5K Nov  9 01:48 ERR2259150_db.nin
-rw-r--r-- 1  912 Nov  9 01:48 ERR2259150_db.nnd
-rw-r--r-- 1   52 Nov  9 01:48 ERR2259150_db.nni
-rw-r--r-- 1  488 Nov  9 01:48 ERR2259150_db.nog
-rw-r--r-- 1 586K Nov  9 01:48 ERR2259150_db.nsq
-rw-r--r-- 1 1.9K Nov  9 01:48 ERR2259150_db.translation

```



#### run RepeatModeler
```
$ RepeatModeler -database   assembly/ERR2259150/assembly > assembly_RepeatModeler.txt
```

