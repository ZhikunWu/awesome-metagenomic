
## [repeatmasker](https://github.com/rmhubley/RepeatMasker): a program that screens DNA sequences for interspersed repeats and low complexity DNA sequences.

#### install repeatmasker
```
$ conda install -c bioconda repeatmasker
```


#### set exact species
```
$ RepeatMasker -parallel 30 -species bacterial  -html -gff -dir repeat assembly/ERR2259150/assembly.fasta 
RepeatMasker version open-4.0.7
Search Engine: NCBI/RMBLAST [ 2.6.0+ ]
RepeatMasker::initLibraries: Species "bacterial" is not known to RepeatMasker.
Here are some similar sounding (using Soundex) valid species names:
        -species "bactrocera tsuneonis"
        -species "bostaera"
        -species "bigeye thresher"
        -species "bactris trichophylla burret"
        -species "bactrocera facialis"
        -species "bactrocera icelus"
        -species "bactris gasipaes var. gasipaes"
        -species "bacidia arceutina"
        -species "bactrocera trivialis drew 1971"
        -species "bactrocera cf. cognata cue-lure"
        -species "bactrocera sp. k2"
        -species "bistorta affinis"
        ......
```

RepeatMasker::initLibraries: Species "bacterial" is not known to RepeatMasker.

#### run RepeatMasker
```
$ RepeatMasker -parallel 30 -species "bactra testudinea"  -html -gff -dir repeat assembly/ERR2259150/assembly.fasta 
RepeatMasker version open-4.0.7
Search Engine: NCBI/RMBLAST [ 2.6.0+ ]
Master RepeatMasker Database: /home/wzk/anaconda3/envs/evolution/share/RepeatMasker/Libraries/RepeatMaskerLib.embl ( Complete Database: dc20170127 )


Warning...unknown stuff <
>
Building general libraries in: /home/wzk/anaconda3/envs/evolution/share/RepeatMasker/Libraries/dc20170127/general
Building species libraries in: /home/wzk/anaconda3/envs/evolution/share/RepeatMasker/Libraries/dc20170127/bactra
   - 174 ancestral and ubiquitous sequence(s) for bactra
   - 0 lineage specific sequence(s) for bactra
cannot read file testudinea in /home/wzk/Project/Leptosphaeria

analyzing file assembly/ERR2259150/assembly.fasta

Some previous RepeatMasker output files were moved to the directory 
repeat/assembly.fasta.preThuNov82152002018.RMoutput 
in order not to overwrite them.


Checking for E. coli insertion elements
...

processing output: 
cycle 1 
cycle 2 
cycle 3 
cycle 4 
cycle 5 
cycle 6 
cycle 7 
cycle 8 
cycle 9 
cycle 10 
Generating output... 
masking
done

Output files can not be written to repeat. They can be found in the directory /home/wzk/Project/Leptosphaeria/RM_192513.ThuNov82200292018 instead. 
Consider using the -dir option.
```

#### you should create out directory firstly, and then run **RepeatMasker**
```
mkdir repeat && RepeatMasker -parallel 30 -species "bactra testudinea"  -html -gff -dir repeat assembly/ERR2259150/assembly.fasta

```


output files:

```
$ tree repeat/
repeat/
├── assembly.fasta.alert
├── assembly.fasta.cat
├── assembly.fasta.masked
├── assembly.fasta.out
├── assembly.fasta.out.gff
├── assembly.fasta.out.html
└── assembly.fasta.tbl

```

details for output files:
```
$ head assembly.fasta.alert
The following E coli IS elements could not be confidently clipped out:
  IS2#ARTEFACT in NZ_GG666937.1: 5 - 233


$ head assembly.fasta.cat
16 21.15 0.00 0.00 NZ_GG666849.1 38469 38506 (592280) (GCA)n#Simple_repeat 1 38 (0) m_b1s252i0

  NZ_GG666849.1      38469 GCAGCCGGAGCAGCAGCGTCGGCAGCCGGAGCAGCAGC 38506
                                v v         iv i     v v         
  (GCA)n#Simple          1 GCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGCAGC 38

Matrix = Unknown
Transitions / transversions = 0.40 (2/5)
Gap_init rate = 0.00 (0 / 37), avg. gap size = 0.0 (0 / 0)


$ head assembly.fasta.masked
>NZ_GG666849.1 Bifidobacterium longum subsp. longum ATCC 55813 SCAFFOLD1, whole genome shotgun sequence
AACCCCGTGGAGTTCACACAACAAGGTGTATTTAGTCAAGTCGGTGTTTC
GTGTTTCGTCACTGATTTTTTTCACTGCGGAAAAACACTGCCGAACCCGC
CCAACAAACATTGAAGCAATACAGCACGGCGTGTACCAGAAGATCATCTC
CTGTTACACGCACGAGGACCGGCGCAAGGGACGGGGCATGATGGCCGAGC
TCATCGAATCCCTCGCCGTCAAAGGCGGTGCGCCCGGATGCCCCGAACTG
CTTCAACGTGACGCCCACACGTCCCAATTCGCCGTGCACGCGCGCCCAGT
CGGGCTGCTCGTGGGCACTCTCGATCGCACCCCTGCCGGGAAACAGCAGG
GCATACACCTCGTCATCGGTTTTTGTCCTCCACACCACCGTAGGAGACAC
CGAGCCGGTCGGCGGCGTCGAACACATTGATCACGCTGTGCTTCGACATG


$ head assembly.fasta.out
   SW   perc perc perc  query          position in query        matching     repeat           position in repeat
score   div. del. ins.  sequence       begin  end      (left)   repeat       class/family   begin  end    (left)  ID

   16   21.1  0.0  0.0  NZ_GG666849.1   38469  38506 (592280) + (GCA)n       Simple_repeat       1     38    (0)   1  
   12   14.7  3.3  0.0  NZ_GG666849.1   41350  41379 (589407) + (CTGAGC)n    Simple_repeat       1     31    (0)   2  
   12   21.1  2.5  2.5  NZ_GG666849.1   42680  42719 (588067) + (CGG)n       Simple_repeat       1     40    (0)   3  
   14   10.4  3.0  3.0  NZ_GG666849.1   71378  71410 (559376) + (CGCTTG)n    Simple_repeat       1     33    (0)   4  
   12    5.6  0.0  0.0  NZ_GG666849.1   72091  72109 (558677) + (GCC)n       Simple_repeat       1     19    (0)   5  
   13   25.8  0.0  0.0  NZ_GG666849.1   75617  75654 (555132) + (TGCTATT)n   Simple_repeat       1     38    (0)   6  
   12   24.5  2.2  2.2  NZ_GG666849.1   81907  81951 (548835) + (CGA)n       Simple_repeat       1     45    (0)   7  


$ head assembly.fasta.out.gff
##gff-version 2
##date 2018-11-08
##sequence-region assembly.fasta
NZ_GG666849.1   RepeatMasker    similarity  38469   38506   21.1    +   .   Target "Motif:(GCA)n" 1 38
NZ_GG666849.1   RepeatMasker    similarity  41350   41379   14.7    +   .   Target "Motif:(CTGAGC)n" 1 31
NZ_GG666849.1   RepeatMasker    similarity  42680   42719   21.1    +   .   Target "Motif:(CGG)n" 1 40
NZ_GG666849.1   RepeatMasker    similarity  71378   71410   10.4    +   .   Target "Motif:(CGCTTG)n" 1 33
NZ_GG666849.1   RepeatMasker    similarity  72091   72109    5.6    +   .   Target "Motif:(GCC)n" 1 19
NZ_GG666849.1   RepeatMasker    similarity  75617   75654   25.8    +   .   Target "Motif:(TGCTATT)n" 1 38
NZ_GG666849.1   RepeatMasker    similarity  81907   81951   24.5    +   .   Target "Motif:(CGA)n" 1 45


$ head assembly.fasta.tbl
==================================================
file name: assembly.fasta           
sequences:           114
total length:    2396359 bp  (2372858 bp excl N/X-runs)
GC level:         60.25 %
bases masked:       9468 bp ( 0.40 %)
==================================================
               number of      length   percentage
               elements*    occupied  of sequence
--------------------------------------------------

```




####  the library of RepeatMasker

```
$ tree /home/wzk/anaconda3/envs/evolution/share/RepeatMasker/Libraries
/home/wzk/anaconda3/envs/evolution/share/RepeatMasker/Libraries
├── dc20170127
│   ├── bactra
│   │   ├── rmblastdb.log
│   │   ├── specieslib
│   │   ├── specieslib.nhr
│   │   ├── specieslib.nin
│   │   ├── specieslib.nsq
│   │   └── speciesMeta.pm
│   └── general
│       ├── at.lib
│       ├── at.lib.nhr
│       ├── at.lib.nin
│       ├── at.lib.nsq
│       ├── is.lib
│       ├── is.lib.nhr
│       ├── is.lib.nin
│       ├── is.lib.nsq
│       ├── l1.lib
│       ├── l1.lib.nhr
│       ├── l1.lib.nin
│       ├── l1.lib.nsq
│       ├── refineableHash.dat
│       ├── rmblastdb.log
│       ├── simple.lib
│       ├── simple.lib.nhr
│       ├── simple.lib.nin
│       └── simple.lib.nsq
├── DfamConsensus.embl
├── Dfam.hmm
├── README.meta
├── RepeatAnnotationData.pm
├── RepeatMaskerLib.embl
├── RepeatPeps.lib
├── RepeatPeps.readme
├── RMRBMeta.embl
└── taxonomy.dat

```

detail for RepeatMaskerLib.embl
```
$ less RepeatMaskerLib.embl

CC ****************************************************************
CC                                                                *
CC   RepeatMasker Combined Library                                *
CC    This is a merged file of external library sources.          *
CC    See the original libraries for detailed copyright           *
CC    and licensing restrictions.                                 *
CC                                                                *
CC   Sources:                                                     *
CC    Dfam_Consensus RELEASE 20170127;                            *

CC                                                                *
CC   RepeatMasker software and database development and           *
CC   maintenance are currently funded by an NIH/NHGRI             *
CC   R01 grant HG02939-01 to Arian Smit.  RepBase Update          *
CC   development and maintenance are funded by NIH/NLM grant      *
CC   No.2P41LM006252-07A1 to Jerzy Jurka.                         *
CC                                                                *
CC ****************************************************************
XX
ID   IS1 repeatmasker; DNA; ???; 768 BP.
XX
KW   ARTEFACT/.
XX
CC   IS1 DNA
XX
CC   RepeatMasker Annotations:
CC        Type: ARTEFACT
CC        SubType: 
CC        Species: root
CC        SearchStages: 10
CC        BufferStages:
XX
SQ   Sequence 768 BP; 178 A; 194 C; 215 G; 181 T; 0 other;
     ggtgatgctg ccaacttact gatttagtgt atgatggtgt ttttgaggtg ctccagtggc   60
     ttctgtttct atcagctgtc cctcctgttc agctactgac ggggtggtgc gtaacggcaa   120
     aagcaccgcc ggacatcagc gctatctctg ctctcactgc cgtaaaacat ggcaactgca   180
     gttcacttac accgcttctc aacccggtac gcaccagaaa atcattgata tggccatgaa   240
     tggcgttgga tgccgggcaa cagcccgcat tatgggcgtt ggcctcaaca cgattttacg   300
     tcacttaaaa aactcaggcc gcagtcggta acctcgcgca tacagccggg cagtgacgtc   360

```
