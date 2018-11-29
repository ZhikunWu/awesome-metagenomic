
## [ Tandem Repeats Finder](https://tandem.bu.edu/trf/trf.html)

#### install Tandem Repeats Finder
```
$ conda install -c bioconda trf 
```

#### run trf
```
$ trf File = assembly/ERR2259150/assembly.fasta  Match = 2  Mismatch = 7  Delta = 7 PM = 80  PI = 10   Minscore = 50   MaxPeriod = 2000 > trf_out.txt 

Tandem Repeats Finder, Version 4.09
Copyright (C) Dr. Gary Benson 1999-2012. All rights reserved.

```

run trf successfully
```
$ trf assembly/ERR2259150/assembly.fasta 2 7 7 80 10 50 2000 > trf_out.txt -ngs > trf_out.txt
```

out files:
```
-rw-r--r-- 1 3.4K Nov  9 03:37 assembly.fasta.2.7.7.80.10.50.2000.summary.html
-rw-r--r-- 1  22K Nov  9 03:37 assembly.fasta.s1.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1  41K Nov  9 03:37 assembly.fasta.s1.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 2.4K Nov  9 03:37 assembly.fasta.s18.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1 2.3K Nov  9 03:37 assembly.fasta.s18.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1  18K Nov  9 03:37 assembly.fasta.s2.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1  32K Nov  9 03:37 assembly.fasta.s2.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 6.8K Nov  9 03:37 assembly.fasta.s3.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1  12K Nov  9 03:37 assembly.fasta.s3.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 5.5K Nov  9 03:37 assembly.fasta.s4.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1 8.4K Nov  9 03:37 assembly.fasta.s4.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 4.2K Nov  9 03:37 assembly.fasta.s5.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1 5.5K Nov  9 03:37 assembly.fasta.s5.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 5.0K Nov  9 03:37 assembly.fasta.s6.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1 7.2K Nov  9 03:37 assembly.fasta.s6.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 3.3K Nov  9 03:37 assembly.fasta.s7.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1 4.2K Nov  9 03:37 assembly.fasta.s7.2.7.7.80.10.50.2000.1.txt.html
-rw-r--r-- 1 9.9K Nov  9 03:37 assembly.fasta.s8.2.7.7.80.10.50.2000.1.html
-rw-r--r-- 1  17K Nov  9 03:37 assembly.fasta.s8.2.7.7.80.10.50.2000.1.txt.html


```

```
$ head -n 2 trf_out.txt
@NZ_GG666849.1 Bifidobacterium longum subsp. longum ATCC 55813 SCAFFOLD1, whole genome shotgun sequence
24383 24525 61 2.3 61 84 4 182 27 21 25 25 1.99 TCGTGAAGAACGTACACTGAATCGTCGTCAACGTACGGTTTTCACGAAATGGCAGCTCATC TCGTGAAGAACGTACACTGAATCGTCGTCAACGTACGGTTTTCACGAAATGGGGCCTCATCTCGTGAAGAACGTACACTGAGTCATTCTGAGCGTACGGTTTTCACGAAATGGCAGCTGATTTCGTGAAGAACGTACGCTGAA GTACGCTGAGTTGCGGTGAGTGTACGGTTTCCGCGAAATCATCCCTAATT GATGCCCCCGGTGTCACTGATGACTGTTTTCGGTATGGAAGGCGGCGCAG
```



donnot output html files:
```
$ trf assembly/ERR2259150/assembly.fasta 2 7 7 80 10 50 2000 -h -ngs > trf_out.txt
```