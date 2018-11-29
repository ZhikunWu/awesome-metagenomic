
## [prokka](https://github.com/tseemann/prokka): Rapid prokaryotic genome annotation

#### run prokka

```
$ prokka /home/wzk/Project/Leptosphaeria/assembly/ERR2259150/assembly.fasta --outdir /home/wzk/Project/Leptosphaeria/annotate/ERR2259150 --prefix MetaContig --cpus 40 --force
Can't locate Bio/Root/Version.pm in @INC (you may need to install the Bio::Root::Version module) (@INC contains: /home/wzk/anaconda3/envs/qiime/bin/../perl5 /home/wzk/anaconda3/envs/py35/bin/mirdeep2_0_0_8/lib/perl5 /home/wzk/anaconda3/envs/qiime/bin/MOCAT/src /home/wzk/anaconda3/envs/qiime/lib/perl5/site_perl/5.22.0/x86_64-linux-thread-multi /home/wzk/anaconda3/envs/qiime/lib/perl5/site_perl/5.22.0 /home/wzk/anaconda3/envs/qiime/lib/perl5/5.22.0/x86_64-linux-thread-multi /home/wzk/anaconda3/envs/qiime/lib/perl5/5.22.0 .) at /home/wzk/anaconda3/envs/qiime/bin/prokka line 32.
BEGIN failed--compilation aborted at /home/wzk/anaconda3/envs/qiime/bin/prokka line 32.
```

#### create envoronment prokka

Bio-perl is unfortunately not rebuilt for perl 5.26 yet.

So create the conda envoronment prokka

```
$ conda create -n prokka perl=5.22 prokka
```

run prokka

```
$ source activate prokka && prokka /home/wzk/Project/Leptosphaeria/assembly/ERR2259150/assembly.fasta --outdir /home/wzk/Project/Leptosphaeria/annotate/ERR2259150 --prefix MetaContig --cpus 40 --force
Can't locate XML/Simple.pm in @INC (you may need to install the XML::Simple module) (@INC contains: /home/wzk/anaconda3/envs/prokka/bin/../perl5 /home/wzk/anaconda3/envs/py35/bin/mirdeep2_0_0_8/lib/perl5 /home/wzk/anaconda3/envs/qiime/bin/MOCAT/src /home/wzk/anaconda3/envs/prokka/lib/perl5/site_perl/5.22.2/x86_64-linux-thread-multi /home/wzk/anaconda3/envs/prokka/lib/perl5/site_perl/5.22.2 /home/wzk/anaconda3/envs/prokka/lib/perl5/5.22.2/x86_64-linux-thread-multi /home/wzk/anaconda3/envs/prokka/lib/perl5/5.22.2 .) at /home/wzk/anaconda3/envs/prokka/bin/prokka line 27.
BEGIN failed--compilation aborted at /home/wzk/anaconda3/envs/prokka/bin/prokka line 27.
```



#### update XML/Simple
```
$ conda update -c bioconda perl-xml-simple
```

```
$ source activate prokka && prokka /home/wzk/Project/Leptosphaeria/assembly/ERR2259150/assembly.fasta --outdir /home/wzk/Project/Leptosphaeria/annotate/ERR2259150 --prefix MetaContig --cpus 40 --force
Can't locate Bio/Root/Version.pm in @INC (you may need to install the Bio::Root::Version module) (@INC contains: /home/wzk/anaconda3/envs/prokka/bin/../perl5 /home/wzk/anaconda3/envs/py35/bin/mirdeep2_0_0_8/lib/perl5 /home/wzk/anaconda3/envs/qiime/bin/MOCAT/src /home/wzk/anaconda3/envs/prokka/lib/site_perl/5.26.2/x86_64-linux-thread-multi /home/wzk/anaconda3/envs/prokka/lib/site_perl/5.26.2 /home/wzk/anaconda3/envs/prokka/lib/5.26.2/x86_64-linux-thread-multi /home/wzk/anaconda3/envs/prokka/lib/5.26.2 .) at /home/wzk/anaconda3/envs/prokka/bin/prokka line 32.
BEGIN failed--compilation aborted at /home/wzk/anaconda3/envs/prokka/bin/prokka line 32.

```




#### the issue of parallel

the issue was an old version of parallel
```
$ conda create -n prokka prokka=1.13 minced=0.3.0 parallel=20180522
```


#### Arguments
```
$ prokka
Name:
  Prokka 1.13.3 by Torsten Seemann <torsten.seemann@gmail.com>
Synopsis:
  rapid bacterial genome annotation
Usage:
  prokka [options] <contigs.fasta>
General:
  --help             This help
  --version          Print version and exit
  --docs             Show full manual/documentation
  --citation         Print citation for referencing Prokka
  --quiet            No screen output (default OFF)
  --debug            Debug mode: keep all temporary files (default OFF)
Setup:
  --dbdir [X]        Prokka database root folders (default '/home/wzk/anaconda3/envs/prokka/db')
  --listdb           List all configured databases
  --setupdb          Index all installed databases
  --cleandb          Remove all database indices
  --depends          List all software dependencies
Outputs:
  --outdir [X]       Output folder [auto] (default '')
  --force            Force overwriting existing output folder (default OFF)
  --prefix [X]       Filename output prefix [auto] (default '')
  --addgenes         Add 'gene' features for each 'CDS' feature (default OFF)
  --addmrna          Add 'mRNA' features for each 'CDS' feature (default OFF)
  --locustag [X]     Locus tag prefix [auto] (default '')
  --increment [N]    Locus tag counter increment (default '1')
  --gffver [N]       GFF version (default '3')
  --compliant        Force Genbank/ENA/DDJB compliance: --addgenes --mincontiglen 200 --centre XXX (default OFF)
  --centre [X]       Sequencing centre ID. (default '')
  --accver [N]       Version to put in Genbank file (default '1')
Organism details:
  --genus [X]        Genus name (default 'Genus')
  --species [X]      Species name (default 'species')
  --strain [X]       Strain name (default 'strain')
  --plasmid [X]      Plasmid name or identifier (default '')
Annotations:
  --kingdom [X]      Annotation mode: Archaea|Bacteria|Bacteria|Bacteria|Mitochondria|Viruses (default 'Bacteria')
  --gcode [N]        Genetic code / Translation table (set if --kingdom is set) (default '0')
  --gram [X]         Gram: -/neg +/pos (default '')
  --usegenus         Use genus-specific BLAST databases (needs --genus) (default OFF)
  --proteins [X]     FASTA or GBK file to use as 1st priority (default '')
  --hmms [X]         Trusted HMM to first annotate from (default '')
  --metagenome       Improve gene predictions for highly fragmented genomes (default OFF)
  --rawproduct       Do not clean up /product annotation (default OFF)
  --cdsrnaolap       Allow [tr]RNA to overlap CDS (default OFF)
Matching:
  --evalue [n.n]     Similarity e-value cut-off (default '1e-09')
  --coverage [n.n]   Minimum coverage on query protein (default '80')
Computation:
  --cpus [N]         Number of CPUs to use [0=all] (default '8')
  --fast             Fast mode - only use basic BLASTP databases (default OFF)
  --noanno           For CDS just set /product="unannotated protein" (default OFF)
  --mincontiglen [N] Minimum contig size [NCBI needs 200] (default '1')
  --rfam             Enable searching for ncRNAs with Infernal+Rfam (SLOW!) (default '0')
  --norrna           Don't run rRNA search (default OFF)
  --notrna           Don't run tRNA search (default OFF)
  --rnammer          Prefer RNAmmer over Barrnap for rRNA prediction (default OFF)
```


#### prokka

first get into the prokka environment of conda

```
source activate prokka && prokka /home/wzk/Project/Leptosphaeria/assembly/ERR2259150/assembly.fasta --outdir /home/wzk/Project/Leptosphaeria/annotation/ERR2259150 --prefix assembly --cpus 10 --force
```


output files:
```
$ tree Prokka/
Prokka/
├── assembly.err
├── assembly.faa
├── assembly.ffn
├── assembly.fna
├── assembly.fsa
├── assembly.gbk
├── assembly.gff
├── assembly.log
├── assembly.sqn
├── assembly.tbl
├── assembly.tsv
└── assembly.txt

```