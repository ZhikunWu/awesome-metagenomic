

##  [LTR_Finder](https://github.com/xzhub/LTR_Finder): an efficient program for finding full-length LTR retrotranspsons in genome sequences

The Program first constructs all exact match pairs by a suffix-array based algorithm and extends them to long highly similar pairs. Then Smith-Waterman algorithm is used to adjust the ends of LTR pair candidates to get alignment boundaries. These boundaries are subject to re-adjustment using supporting information of TG..CA box and TSRs and reliable LTRs are selected. Next, LTR_FINDER tries to identify PBS, PPT and RT inside LTR pairs by build-in aligning and counting modules. RT identification includes a dynamic programming to process frame shift. For other protein domains, LTR_FINDER calls ps_scan (from PROSITE, http://www.expasy.org/prosite/) to locate cores of important enzymes if they occur. Then possible ORFs are constructed based on that. At last, the program reports possible LTR retrotransposon models in different confidence levels according to how many signals and domains they hit.

#### install LTR_Finder

clone source
```
$ git clone https://github.com/xzhub/LTR_Finder.git
$ cd LTR_Finder/source/

$ ./ltr_finder
ltr_finder v1.07
Usage  : [options] <INPUT_FASTA_FILE>
         -o NUM     gap open penalty, default is 3
         -t NUM     gap extension penalty, default is 1
         -e NUM     gap end penalty, default is 1
         -m NUM     match score, default is 2
         -u NUM     unmatch score, default is -2
         -D NUM     Max distance between 5'&3'LTR, default is 20000
         -d NUM     Min distance between 5'&3'LTR, default is 1000
         -L NUM     Max length of 5'&3'LTR, default is 3500
         -l NUM     Min length of 5'&3'LTR, default is 100
         -p NUM     min length of exact match pair, default is 20
         -g NUM     Max gap between joined pairs, default is 50
         -G NUM     Max gap between RT sub-domains, default is 2
         -T NUM     Min sub-domains found in a RT domain, default is 4
         -j NUM     Threshold for join new sequence in existed alignment
                    new alignment similarity higher than this will be joined,
                    default is 0.70
         -J NUM     Threshold for split existed alignment to two part
                    new alignment similarity lower than this will be split,
                    set this threshold lower than -j, means turn it off,
                    default is 0.90
         -S NUM     output Score limit, default is 6.00, [0,10]
         -M NUM     min LTR similarity threshold, default is 0.00, [0,1]
         -B NUM     Boundary alignment sharpness threshold, higher one.
                     one of the two edge's sharpness must higher than
                     this threshold, default is 0.400, [0,1]
         -b NUM     Boundary alignment sharpness threshold, lower one.
                     both of the two edge's sharpness must higher than
                     this threshold, default is 0.400, [0,1]
         -r NUM     PBS detecting threshold, min tRNA match length: 14, [1,18]
         -w NUM     output format: [0]-full, 1-summary, 2-table.
         -O NUM     output alignment length(only affect -w0), default is 40
         -P STR     SeqIDs, will only calculate matched SeqID
                      POSIX style regular express is supported.
         -s filename      tRNA sequence file(FASTA format)
         -f filename      data file used to draw figure
         -a ps_scan_dir   Use ps_scan to predict protein domain
         -x         Output in html format
         -E         LTR must have edge signal
                    (at least two of PBS,PPT,TSR)
         -C         detect Centriole, delete highly repeat regions
         -F 01string      Filter to choose desired result,default is 0
                     10000000000 5'-LTR must have TG
                     01000000000 5'-LTR must have CA
                     00100000000 3'-LTR must have TG
                     00010000000 3'-LTR must have CA
                     00001000000 TSR must be found
                     00000100000 PBS must be found
                     00000010000 PPT must be found
                     00000001000 RT domain muse be found
                     00000000100 Integrase core must be found
                     00000000010 Integrase c-term must be found
                     00000000001 RNase H must be found
         -h         help



```

create soft links
```
$ cd /home/wzk/anaconda3/envs/evolution/bin && ln -s /home/wzk/anaconda3/envs/evolution/bin/LTR_Finder/source/ltr_finder  ltr_finder
```

#### run ltr_finder
```
$ ltr_finder ~/database/GENOME/arabidopsis/Arabidopsis_thaliana.TAIR10.dna.toplevel.fa  -w 2 -f figure > ltr_finder_result.txt
```




out file
```
$ head ltr_finder_result.txt
Program    : LTR_FINDER
Version    : 1.07

Predict protein Domains 1.992 second
>Sequence: 1 Len:30427671
index   SeqID   Location    LTR len Inserted element len    TSR PBS PPT RT  IN (core)   IN (c-term) RH  Strand  Score   Sharpness   Similarity
[ 1]    1   3780765-3785720 440,440 4956    CTTGT   N-N 3785266-3785280 N-N N-N N-N N-N +   6   0.457,0.5   1
[ 2]    1   4406006-4411120 162,162 5115    ATTAA   N-N 4410909-4410923 N-N N-N N-N N-N +   6   0.429,0.414 0.969
[ 3]    1   6538418-6543536 163,163 5119    AAAAA   N-N 6538665-6538679 N-N N-N N-N N-N -   6   0.486,0.471 1
[ 4]    1   7717356-7722547 440,440 5192    GACTG   N-N 7722093-7722107 N-N N-N N-N N-N +   6   0.529,0.486 0.973

```
