
## [tRNAscan-SE](http://lowelab.ucsc.edu/tRNAscan-SE/)

#### install using conda
```
$ conda install -c bioconda trnascan-se
```

#### [tRNAscan-SE安装要点](http://bbs.sciencenet.cn/forum.php?mod=viewthread&tid=3075997): https://vcru.wisc.edu/simonlab/bioinformatics/programs/install/trnascan-se.htm

#### install using source code

```
$ wget http://lowelab.ucsc.edu/software/tRNAscan-SE.tar.gz
$ tar -zxf tRNAscan-SE.tar.gz && cd tRNAscan-SE
$ make

To update your environment upon every login, you should
add the line:

source /home/wzk/anaconda3/envs/qiime/bin/tRNAscan-SE-1.3.1/setup.tRNAscan-SE

to your ".cshrc" file.

If you prefer to manually update your environment variables,
be sure to make the following changes:

1) Add /home/wzk/bin to your PATH variable
2) Add /home/wzk/bin to your PERl5LIB variable
3) Add /home/wzk/man to your MANPATH variable


$ make install
.
.
cp trnascan-1.4 covels-SE coves-SE eufindtRNA tRNAscan-SE /home/wzk/bin/.
cp -R tRNAscanSE /home/wzk/bin/
cp TPCsignal Dsignal *.cm gcode.* /home/wzk/lib/tRNAscan-SE/.
cp tRNAscan-SE.man /home/wzk/man/man1/tRNAscan-SE.1 

```

#### tRNAscan-SE parameter
```

$ tRNAscan-SE

tRNAscan-SE 1.3.1 (January 2012)

FATAL: No sequence file(s) specified.

Usage: tRNAscan-SE [-options] <FASTA file(s)>

  Scan a sequence file for tRNAs using tRNAscan, EufindtRNA &
   tRNA covariance models
          -- defaults to use with eukaryotic sequences 
             (use -B, -A, -O or -G to scan other types of sequences)

Basic Options
  -B         : search for bacterial tRNAs (use bacterial tRNA model)
  -A         : search for archaeal tRNAs  (use archaeal tRNA model)
  -O         : search for organellar (mitochondrial/chloroplast) tRNAs
  -G         : use general tRNA model (cytoplasmic tRNAs from all 3 domains included)

  -i         : search using Infernal cm analysis only (max sensitivity, very slow)
  -C         : search using Cove analysis only (high sensitivity, very slow)

  -o <file>  : save final results in <file>
  -f <file>  : save tRNA secondary structures to <file>
  -a         : output results in ACeDB output format instead of default
               tabular format
  -m <file>  : save statistics summary for run in <file>
               (speed, # tRNAs found in each part of search, etc)
  -H         : show both primary and secondary structure components to
               covariance model bit scores
  -q         : quiet mode (credits & run option selections suppressed)

  -h         : print full list (long) of available options

```


#### run tRNAscan-SE

```
$ tRNAscan-SE GCF_000003135.1_ASM313v1_genomic.fna  -o GCF_000003135.1_ASM313v1_genomic_tRNA.fna  -f GCF_000003135.1_ASM313v1_genomic_tRNA_structure.fna -m GCF_000003135.1_ASM313v1_genomic_tRNA_structure_stats.txt -a GCF_000003135.1_ASM313v1_genomic_tRNA_gene.fna --thread 10


tRNAscan-SE v.2.0 (December 2017) - scan sequences for transfer RNAs
Copyright (C) 2017 Patricia Chan and Todd Lowe
                   University of California Santa Cruz
Freely distributed under the GNU General Public License (GPLv3)

------------------------------------------------------------
Sequence file(s) to search:        GCF_000003135.1_ASM313v1_genomic.fna
Search Mode:                       Eukaryotic
Results written to:                GCF_000003135.1_ASM313v1_genomic_tRNA.fna
Output format:                     Tabular
Searching with:                    Infernal First Pass->Infernal
Isotype-specific model scan:       Yes
Covariance model:                  /home/wzk/anaconda3/envs/qiime/lib/tRNAscan-SE/models/TRNAinf-euk.cm
                                   /home/wzk/anaconda3/envs/qiime/lib/tRNAscan-SE/models/TRNAinf-euk-SeC.cm
Infernal first pass cutoff score:  10

Temporary directory:               /tmp
tRNA secondary structure
    predictions saved to:          GCF_000003135.1_ASM313v1_genomic_tRNA_structure.fna
Predicted tRNA sequences
    saved to:                      GCF_000003135.1_ASM313v1_genomic_tRNA_gene.fna
Search statistics saved in:        GCF_000003135.1_ASM313v1_genomic_tRNA_structure_stats.txt
------------------------------------------------------------

Status: Phase I: Searching for tRNAs with HMM-enabled Infernal
Status: Phase II: Infernal verification of candidate tRNAs detected with first-pass scan

```


#### output files:
```
$ head  GCF_000003135.1_ASM313v1_genomic_tRNA.fna
Sequence            tRNA    Bounds  tRNA    Anti    Intron Bounds   Inf       
Name            tRNA #  Begin   End     Type    Codon   Begin   End Score   Note
--------        ------  -----   ------  ----    -----   -----   ----    ------  ------
NZ_GG666849.1   1   51918   52005   Leu GAG 0   0   65.5    
NZ_GG666849.1   2   189861  189931  Gln TTG 0   0   52.5    
NZ_GG666849.1   3   192875  192947  Ala GGC 0   0   68.4    
NZ_GG666849.1   4   193037  193109  Ala GGC 0   0   68.4    
NZ_GG666849.1   5   205948  206021  Pro TGG 0   0   72.3    
NZ_GG666849.1   6   443679  443751  His GTG 0   0   72.5    
NZ_GG666849.1   7   487846  487773  Arg TCT 0   0   77.1    

$ head GCF_000003135.1_ASM313v1_genomic_tRNA_gene.fna
>NZ_GG666849.1.trna1 NZ_GG666849.1:51918-52005 (+) Leu (GAG) 88 bp Sc: 65.5
GCCCGGGTGGCGGAATGGTAGACGCGCTAGCTTGAGGTGCTAGTGCCTATTTTATACGGG
CGTACGGGTTCAAGTCCCGTCTCGGGCA
>NZ_GG666849.1.trna2 NZ_GG666849.1:189861-189931 (+) Gln (TTG) 71 bp Sc: 52.5
TCCCCCATGGTGTAATGGCAGCACACGGGTCTTTGGAACCCTTTGTCTTGGTTCGAGTCC
AGGTGGGGGAA
>NZ_GG666849.1.trna3 NZ_GG666849.1:192875-192947 (+) Ala (GGC) 73 bp Sc: 68.4
GGGGCTATAGCGCAGCTGGTAGCGCATCTCCATGGCATGGAGAGGGTCGGGGGTTCGAAT
CCCCCTAGCTCCA
>NZ_GG666849.1.trna4 NZ_GG666849.1:193037-193109 (+) Ala (GGC) 73 bp Sc: 68.4

$ head GCF_000003135.1_ASM313v1_genomic_tRNA_structure.fna
NZ_GG666849.1.trna1 (51918-52005)   Length: 88 bp
Type: Leu   Anticodon: GAG at 34-36 (51951-51953)   Score: 65.5
         *    |    *    |    *    |    *    |    *    |    *    |    *    |    *    |    *  
Seq: GCCCGGGTGGCGGAATGGTaGACGCGCTAGCTTGAGGTGCTAGTGCCTattTTATACGGGCGTACGGGTTCAAGTCCCGTCTCGGGCA
Str: >>>>>>>..>>>..........<<<.>>>>>.......<<<<<.>>>>.........<<<<..>>>>>.......<<<<<<<<<<<<.

NZ_GG666849.1.trna2 (189861-189931) Length: 71 bp
Type: Gln   Anticodon: TTG at 33-35 (189893-189895) Score: 52.5
         *    |    *    |    *    |    *    |    *    |    *    |    *    |
Seq: TCCCCCATGGTGTAATGGCAGCACACGGGTCTTTGGAACCCTTTGTCTTGGTTCGAGTCCAGGTGGGGGAA




$ cat  GCF_000003135.1_ASM313v1_genomic_tRNA_structure_stats.txt

tRNAscan-SE v.2.0 (December 2017) scan results (on host ubuntu)
Started: Mon Nov  5 21:29:31 EST 2018

------------------------------------------------------------
Sequence file(s) to search:        GCF_000003135.1_ASM313v1_genomic.fna
Search Mode:                       Eukaryotic
Results written to:                GCF_000003135.1_ASM313v1_genomic_tRNA.fna
Output format:                     Tabular
Searching with:                    Infernal First Pass->Infernal
Isotype-specific model scan:       Yes
Covariance model:                  /home/wzk/anaconda3/envs/qiime/lib/tRNAscan-SE/models/TRNAinf-euk.cm
                                   /home/wzk/anaconda3/envs/qiime/lib/tRNAscan-SE/models/TRNAinf-euk-SeC.cm
Infernal first pass cutoff score:  10

Temporary directory:               /tmp
tRNA secondary structure
    predictions saved to:          GCF_000003135.1_ASM313v1_genomic_tRNA_structure.fna
Predicted tRNA sequences
    saved to:                      GCF_000003135.1_ASM313v1_genomic_tRNA_gene.fna
Search statistics saved in:        GCF_000003135.1_ASM313v1_genomic_tRNA_structure_stats.txt
------------------------------------------------------------

First-pass Stats:
---------------
Sequences read:         114
Seqs w/at least 1 hit:  7
Bases read:             2396359 (x2 for both strands)
Bases in tRNAs:         4188
tRNAs predicted:        56
Av. tRNA length:        74
Script CPU time:        0.39 s
Scan CPU time:          26.18 s
Scan speed:             183.1 Kbp/sec

First pass search(es) ended: Mon Nov  5 21:29:53 EST 2018

Infernal Stats:
-----------
Candidate tRNAs read:     56
Infernal-confirmed tRNAs:     56
Bases scanned by Infernal:  5308
% seq scanned by Infernal:  0.1 %
Script CPU time:          0.36 s
Infernal CPU time:            21.84 s
Scan speed:               243.0 bp/sec

Infernal analysis of tRNAs ended: Mon Nov  5 21:30:12 EST 2018

Overall scan speed: 98271.8 bp/sec

tRNAs decoding Standard 20 AA:              56
Selenocysteine tRNAs (TCA):                 0
Possible suppressor tRNAs (CTA,TTA,TCA):    0
tRNAs with undetermined/unknown isotypes:   0
Predicted pseudogenes:                      0
                                            -------
Total tRNAs:                                56

tRNAs with introns:         0

|

Isotype / Anticodon Counts:

Ala     : 4   AGC:         GGC: 2       CGC: 1       TGC: 1     
Gly     : 5   ACC:         GCC: 3       CCC: 1       TCC: 1     
Pro     : 3   AGG:         GGG: 1       CGG: 1       TGG: 1     
Thr     : 5   AGT:         GGT: 2       CGT: 2       TGT: 1     
Val     : 5   AAC:         GAC: 2       CAC: 2       TAC: 1     
Ser     : 4   AGA:         GGA: 1       CGA: 1       TGA: 1       ACT:         GCT: 1     
Arg     : 5   ACG: 2       GCG:         CCG: 1       TCG:         CCT: 1       TCT: 1     
Leu     : 5   AAG:         GAG: 1       CAG: 1       TAG: 1       CAA: 1       TAA: 1     
Phe     : 1   AAA:         GAA: 1                               
Asn     : 3   ATT:         GTT: 3                               
Lys     : 2                             CTT: 1       TTT: 1     
Asp     : 2   ATC:         GTC: 2                               
Glu     : 2                             CTC: 1       TTC: 1     
His     : 1   ATG:         GTG: 1                               
Gln     : 2                             CTG: 1       TTG: 1     
Ile     : 1   AAT:         GAT: 1       CAT:         TAT:       
Met     : 3                             CAT: 3                  
Tyr     : 1   ATA:         GTA: 1                               
Supres  : 0                CTA:         TTA:         TCA:       
Cys     : 1   ACA:         GCA: 1                               
Trp     : 1                             CCA: 1                  
SelCys  : 0                                          TCA:       


```


#### Search model

```
  -E                          : search for eukaryotic tRNAs (default)
  -B                          : search for bacterial tRNAs
  -A                          : search for archaeal tRNAs
  -M <model>                  : search for mitochondrial tRNAs
                                  options: mammal, vert
  -O                          : search for other organellar tRNAs
  -G                          : use general tRNA model (cytoslic tRNAs from all 3 domains included)
```

search for bacterial tRNAs:
```
$ tRNAscan-SE GCF_000003135.1_ASM313v1_genomic.fna  -o GCF_000003135.1_ASM313v1_genomic_tRNA.fna  -f GCF_000003135.1_ASM313v1_genomic_tRNA_structure.fna -m GCF_000003135.1_ASM313v1_genomic_tRNA_structure_stats.txt -a GCF_000003135.1_ASM313v1_genomic_tRNA_gene.fna --thread 10 -B
```

