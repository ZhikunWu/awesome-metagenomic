
## Deal with Oxford Nanopore data


### Trimming and filtering using Nanopore data using [NanoFilt](https://github.com/wdecoster/nanofilt)

Install NanoFilt

```
$ conda install -c bioconda nanofilt 
```

Arguments of NanoFilt
```
$ NanoFilt --help
usage: NanoFilt [-h] [-v] [--logfile LOGFILE] [-l LENGTH]
                [--maxlength MAXLENGTH] [-q QUALITY] [--minGC MINGC]
                [--maxGC MAXGC] [--headcrop HEADCROP] [--tailcrop TAILCROP]
                [-s SUMMARY] [--readtype {1D,2D,1D2}]

Perform quality and/or length and/or GC filtering of (long read) fastq data.           Reads on stdin.

General options:
  -h, --help            show the help and exit
  -v, --version         Print version and exit.
  --logfile LOGFILE     Specify the path and filename for the log file.

Options for filtering reads on.:
  -l LENGTH, --length LENGTH
                        Filter on a minimum read length
  --maxlength MAXLENGTH
                        Filter on a maximum read length
  -q QUALITY, --quality QUALITY
                        Filter on a minimum average read quality score
  --minGC MINGC         Sequences must have GC content >= to this. Float between 0.0 and 1.0. Ignored if
                        using summary file.
  --maxGC MAXGC         Sequences must have GC content <= to this. Float between 0.0 and 1.0. Ignored if
                        using summary file.

Options for trimming reads.:
  --headcrop HEADCROP   Trim n nucleotides from start of read
  --tailcrop TAILCROP   Trim n nucleotides from end of read

Input options.:
  -s SUMMARY, --summary SUMMARY
                        Use summary file for quality scores
  --readtype {1D,2D,1D2}
                        Which read type to extract information about from summary. Options are 1D, 2D or
                        1D2

EXAMPLES:
  gunzip -c reads.fastq.gz | NanoFilt -q 10 -l 500 --headcrop 50 | minimap2 genome.fa - | samtools sort -O BAM -@24 -o alignment.bam -
  gunzip -c reads.fastq.gz | NanoFilt -q 12 --headcrop 75 | gzip > trimmed-reads.fastq.gz
  gunzip -c reads.fastq.gz | NanoFilt -q 10 | gzip > highQuality-reads.fastq.gz

```


Run NanoFilt

```
$ gunzip -c ERR2259150.fastq.gz  | NanoFilt -q 10 -l 500 --headcrop 50 > ERR2259150_filt.fastq
```


### Quality control using [nanoQC](https://github.com/wdecoster/nanoQC)

Install nanoQC
```
$ conda install -c bioconda nanoqc
```

Arguments of nanoQC:
```
$ nanoQC --help
usage: nanoQC [-h] [-v] [-o OUTDIR] [-l MINLEN] fastq

Investigate nucleotide composition and base quality.

positional arguments:
  fastq                 Reads data in fastq.gz format.

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         Print version and exit.
  -o OUTDIR, --outdir OUTDIR
                        Specify directory in which output has to be created.
  -l MINLEN, --minlen MINLEN
                        Filters the reads on a minimal length of the given
                        range. Also plots the given length/2 of the begin and
                        end of the reads.

```


Run nanoQC
```
$ nanoQC -o ERR2259150_raw ERR2259150.fastq.gz
```



Output files:

```
$ tree ERR2259150_raw
ERR2259150_raw
├── nanoQC.html
└── NanoQC.log

```

The quality plotting is in report **nanoQC.html**



### Quality control using [NanoPlot](https://github.com/wdecoster/NanoPlot)

Install NanoPlot
```
$ conda install -c bioconda nanoplot
```

Arguments:
```
$ NanoPlot
usage: NanoPlot [-h] [-v] [-t THREADS] [--verbose] [--store] [--raw]
                [-o OUTDIR] [-p PREFIX] [--maxlength N] [--minlength N]
                [--drop_outliers] [--downsample N] [--loglength]
                [--percentqual] [--alength] [--minqual N] [--runtime_until N]
                [--readtype {1D,2D,1D2}] [--barcoded] [-c COLOR]
                [-f {eps,jpeg,jpg,pdf,pgf,png,ps,raw,rgba,svg,svgz,tif,tiff}]
                [--plots [{kde,hex,dot,pauvre} [{kde,hex,dot,pauvre} ...]]]
                [--listcolors] [--no-N50] [--N50] [--title TITLE]
                [--font_scale FONT_SCALE] [--dpi DPI]
                (--fastq file [file ...] | --fasta file [file ...] | --fastq_rich file [file ...] | --fastq_minimal file [file ...] | --summary file [file ...] | --bam file [file ...] | --cram file [file ...] | --pickle pickle)
NanoPlot: error: one of the arguments --fastq --fasta --fastq_rich --fastq_minimal --summary --bam --cram --pickle is required

```

Run NanoPlot:
```
$ NanoPlot -t 10 --fastq ERR2259150.fastq.gz --maxlength 40000 -o NanoPlot_raw --plots hex dot 
```

output files:
```
$ tree NanoPlot_raw
NanoPlot_raw
├── HistogramReadlength.png
├── LogTransformed_HistogramReadlength.png
├── MaxLength-40000_LengthvsQualityScatterPlot_dot.png
├── MaxLength-40000_LengthvsQualityScatterPlot_hex.png
├── NanoPlot_20181108_0757.log
├── NanoPlot-report.html
├── NanoStats_post_filtering.txt
├── NanoStats.txt
├── Weighted_HistogramReadlength.png
├── Weighted_LogTransformed_HistogramReadlength.png
└── Yield_By_Length.png

```
