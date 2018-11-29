#!/usr/bin/env python
# -*- coding:utf-8 -*-
from __future__ import division
import os
import collections
import math

#usage: snakemake -s BinSanity.rule.py --configfile BinSanity.rule.yaml -j 30

### plot the pipeline
#snakemake -s BinSanity.rule.py --configfile BinSanity.rule.yaml  --dag | dot -Tsvg > BinSanity.svg


#### in the anaconda environment qiime with python 2


THREADS = config["THREADS"]
IN_PATH = config["IN_PATH"]
SAMPLES = config["SAMPLES"]
PROJECTS = config["PROJECTS"]


rule all:
    input:
        expand(IN_PATH + '/clean/{sample}.clean.paired.R1.fq.gz', sample=SAMPLES),
        expand(IN_PATH + '/assembly/{project}/{project}.contigs.fa', project=PROJECTS),
        expand(IN_PATH + '/assembly/{project}/{project}.contigs_simplyId.fa', project=PROJECTS),
        expand(IN_PATH + '/mapping/{project}/{project}_sorted.bam', project=PROJECTS),
        expand(IN_PATH + '/assembly/{project}/{project}_coverage.cov', project=PROJECTS),
        expand(IN_PATH + '/assembly/{project}/binning/binsanity-logfile.txt', project=PROJECTS),
        expand(IN_PATH + '/assembly/{project}/binning-refine/binsanity-refine.log', project=PROJECTS),
        expand(IN_PATH + '/assembly/{project}/binning-lc/BinSanityLC-BinsanityLC-log.txt', project=PROJECTS),
        expand(IN_PATH + '/assembly/{project}/binning-wf/BinSanityWf.log', project=PROJECTS),



############################################### Quality Control #######################################
rule Trimmomatic:
    input: 
        fwd = IN_PATH + '/raw/{sample}_1.fastq.gz', 
        rev = IN_PATH + '/raw/{sample}_2.fastq.gz',
    output: 
        fwd = IN_PATH + '/clean/{sample}.clean.paired.R1.fq.gz',
        rev = IN_PATH + '/clean/{sample}.clean.paired.R2.fq.gz',
        fwd_un = IN_PATH + '/clean/{sample}.clean.unpaired.R1.fq.gz',
        rev_un = IN_PATH + '/clean/{sample}.clean.unpaired.R2.fq.gz',
    threads:
        THREADS
    log:
        IN_PATH + "/log/trim/{sample}.log",
    params:
        trimmomatic = config['trimmomatic'],
        ADAPTER = config['ADAPTER'],
    run:
        shell("java -jar {params.trimmomatic} PE -threads {threads} -phred33  {input.fwd} {input.rev} {output.fwd} {output.fwd_un} {output.rev} {output.rev_un} ILLUMINACLIP:{params.ADAPTER}:2:30:12 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:10  MINLEN:36  > {log} 2>&1 ")


rule fastqc:
    input:
        fwd_raw = IN_PATH + '/raw/{sample}.R1.fq.gz', 
        rev_raw = IN_PATH + '/raw/{sample}.R2.fq.gz',
        fwd_clean = rules.Trimmomatic.output.fwd,
        rev_clean = rules.Trimmomatic.output.rev,
    output:
        raw_fwd = IN_PATH + '/FastQC/raw/{sample}/{sample}.R1_fastqc.zip', 
        raw_rev = IN_PATH + '/FastQC/raw/{sample}/{sample}.R2_fastqc.zip',
        clean_fwd = IN_PATH + '/FastQC/clean/{sample}/{sample}.clean.paired.R1_fastqc.zip',  
        clean_rev = IN_PATH + '/FastQC/clean/{sample}/{sample}.clean.paired.R2_fastqc.zip',
    threads:
        THREADS
    log:
        raw = IN_PATH + "/log/fastqc/{sample}_raw.log",
        clean = IN_PATH + "/log/fastqc/{sample}_clean.log",
    params:
        FASTQC = config['fastqc'],
        raw_dir = IN_PATH + '/FastQC/raw/{sample}',
        clean_dir = IN_PATH + '/FastQC/clean/{sample}',
    run:
        shell('{params.FASTQC} --threads {threads} --extract -f fastq {input.fwd_raw} {input.rev_raw} -o {params.raw_dir} > {log.raw} 2>&1 ')
        shell('{params.FASTQC} --threads {threads} --extract -f fastq {input.fwd_clean} {input.rev_clean} -o {params.clean_dir} > {log.clean} 2>&1 ')


rule trim_QC_stats:
    input:
        clean = expand(IN_PATH + '/FastQC/clean/{sample}/{sample}.clean.paired.R1_fastqc.zip',sample=SAMPLES),
        trim_clean_fwd = expand(IN_PATH + '/clean/{sample}.clean.paired.R1.fq.gz',sample=SAMPLES),
        trim_clean_rev = expand(IN_PATH + '/clean/{sample}.clean.paired.R2.fq.gz',sample=SAMPLES),
        trim_raw_fwd = expand(IN_PATH + '/raw/{sample}.R1.fq.gz',sample=SAMPLES), 
        trim_raw_rev = expand(IN_PATH + '/raw/{sample}.R2.fq.gz',sample=SAMPLES),
    output:
        qc = IN_PATH + '/QC/QC_trim_stats.xls',
    log:
        IN_PATH + "/log/trim_qc_stats.log",
    run:
        Input_qc_clean = ','.join(sorted([os.path.dirname(i) for i in input.clean]))
        Input_trim_clean_fwd =','.join(sorted(input.trim_clean_fwd))
        Input_trim_clean_rev =','.join(sorted(input.trim_clean_rev))
        Input_trim_raw_fwd =','.join(sorted(input.trim_raw_fwd))
        Input_trim_raw_rev =','.join(sorted(input.trim_raw_rev))
        shell('source activate py35 && python {SRC_DIR}/Trim_QC_stats.py -i {Input_qc_clean}  -o {output.qc} -d {IN_PATH} --raw_for {Input_trim_raw_fwd}   --raw_rev {Input_trim_raw_rev}  --clean_for {Input_trim_clean_fwd} --clean_rev {Input_trim_clean_rev} > {log} 2>&1 ')


###############################################################################################################

########################################## Assembly ###########################################################
rule MegahitAssembly:
    input:
        fq1 = expand(rules.Trimmomatic.output.fwd, sample=SAMPLES),
        fq2 = expand(rules.Trimmomatic.output.rev, sample=SAMPLES),
    output:
        contig = IN_PATH + '/assembly/{project}/{project}.contigs.fa',  # {project}.contigs.fa
    threads:
        THREADS
    params:
        out_dir = IN_PATH + '/assembly/{project}',
    log:
        IN_PATH + '/log/assembly_{project}.log'
    run:
        FQ1 = ",".join(input.fq1)
        FQ2 = ",".join(input.fq2)
        shell('megahit -1 {FQ1} -2 {FQ2} --num-cpu-threads {threads} --continue --out-dir  {params.out_dir} --out-prefix {wildcards.project} > {log} 2>&1') # {wildcards.project}

rule SimplyFasta:
    input:
        contig = rules.MegahitAssembly.output.contig,
    output:
        contig = IN_PATH + '/assembly/{project}/{project}.contigs_simplyId.fa',
    log:
        IN_PATH + '/log/mapping/{project}_SimplyFasta.log'
    run:
        shell("simplify-fasta -i {input.contig} -o {output.contig} >{log} 2>&1")

#######################################################################################


########################### Alignment reads to contigs ##############################
rule Bowtie2Build:
    input:
        config = rules.SimplyFasta.output.contig,
    output:
        index = IN_PATH + '/assembly/{project}/bowtie2Index/{project}.1.bt2',
    params:
        index = IN_PATH + '/assembly/{project}/bowtie2Index/{project}',
    log:
        IN_PATH + '/log/Bowtie2Build_{project}.log'
    run:
        shell("bowtie2-build {input.config} {params.index} >{log} 2>&1")

rule Bowtie2Align:
    input:
        index = rules.Bowtie2Build.output.index,
        fq1 = expand(rules.Trimmomatic.output.fwd, sample=SAMPLES),
        fq2 = expand(rules.Trimmomatic.output.rev, sample=SAMPLES),
    output:
        # sam = IN_PATH + '/assembly/{project}/bam/{project}.sam',
        sam = temp(IN_PATH + '/mapping/{project}/{project}.sam'),
    params:
        index = rules.Bowtie2Build.params.index,
    threads:
        THREADS
    log:
        IN_PATH + '/log/Bowtie2Align_{project}.log'
    run:
        FQ1 = ",".join(input.fq1)
        FQ2 = ",".join(input.fq2)
        shell("bowtie2 -x {params.index} -1 {FQ1} -2 {FQ2} -S {output.sam} --threads {THREADS} >{log} 2>&1")        



rule SAM2BAM:
    input:
        sam = rules.Bowtie2Align.output.sam,
    output:
        bam = temp(IN_PATH + '/mapping/{project}/{project}.bam'),
    params:
        PICARD = config['PICARD'],
    log:
        IN_PATH + "/log/{project}.bam_sort.log",
    run:
        shell('java -Xmx50g -jar {params.PICARD} SortSam INPUT={input.sam} OUTPUT={output.bam} SORT_ORDER=coordinate >{log} 2>&1')


rule MarkDuplicates:
    input:
        bam = rules.SAM2BAM.output.bam,
    output:
        bam = temp(IN_PATH + '/mapping/{project}/{project}_deduplicated.bam'),
        metrics = IN_PATH + '/mapping/{project}/{project}_dup_metrics.txt',
    params:
        PICARD = config['PICARD'],
    log:
        IN_PATH + "/log/{project}.markDuplicate.log",
    run:
        shell('java -Xmx50g -jar {params.PICARD} MarkDuplicates INPUT={input.bam} OUTPUT={output.bam} METRICS_FILE={output.metrics} REMOVE_DUPLICATES=false ASSUME_SORTED=true >{log} 2>&1')

rule AddGroup:
    input:
        bam = rules.MarkDuplicates.output.bam,
    output:
        bam = IN_PATH + '/mapping/{project}/{project}_sorted.bam',
    params:
        PICARD = config['PICARD'],
    log:
        IN_PATH + "/log/{project}.addGroup.log",
    run:
        shell('java -jar {params.PICARD} AddOrReplaceReadGroups INPUT={input.bam} OUTPUT={output.bam} SORT_ORDER=coordinate RGID=1 RGPL=Illumina RGLB={wildcards.project} RGPU={wildcards.project} RGSM={wildcards.project} >{log} 2>&1')

#############################################################################################


########################## Binning using four methods of BinSanity ############################################
rule GetIds:
    input:
        contig = rules.SimplyFasta.output.contig,
    output:
        ids = IN_PATH + '/assembly/{project}/{project}_ids.txt',
    params:
        contigLen = 1000,
        in_dir = rules.MegahitAssembly.params.out_dir,
    log:
        IN_PATH + '/log/mapping/{project}_GetIds.log'
    run:
        shell("get-ids -f {params.in_dir} -l {wildcards.project}.contigs_simplyId.fa  -o {output.ids} -x {params.contigLen}")

rule Coverage:
    input:
        contig = rules.SimplyFasta.output.contig,
        ids = rules.GetIds.output.ids,
        bam = rules.AddGroup.output.bam,
    output:
        coverage = IN_PATH + '/assembly/{project}/{project}_coverage.cov',
        lognorm = IN_PATH + '/assembly/{project}/{project}_coverage.cov.x100.lognorm',
    params:
        indir = IN_PATH + '/mapping/{project}/',
        cov = IN_PATH + '/assembly/{project}/{project}_coverage',
    log:
        IN_PATH + '/log/mapping/{project}_Coverage.log'
    run:
        shell("Binsanity-profile -i {input.contig} -s {params.indir} --ids {input.ids} -c {params.cov} >{log} 2>&1")


rule Binsanity:
    input:
        lognorm = rules.Coverage.output.lognorm,
    output:
        log = IN_PATH + '/assembly/{project}/binning/binsanity-logfile.txt',
    params:
        indir = IN_PATH + '/assembly/{project}/',
        outdir = IN_PATH + '/assembly/{project}/binning',
        preference = -3,
    log:
        IN_PATH + '/log/mapping/{project}_Binsanity.log'
    run:
        shell("Binsanity -f {params.indir} -l {wildcards.project}.contigs_simplyId.fa -p {params.preference} -c {input.lognorm} -o {params.outdir} >{log} 2>&1")

rule BinsanityRefine:
    input:
        lognorm = rules.Coverage.output.lognorm,
    output:
        log = IN_PATH + '/assembly/{project}/binning-refine/binsanity-refine.log',
    params: 
        indir = IN_PATH + '/assembly/{project}/',
        outdir = IN_PATH + '/assembly/{project}/binning-refine',
        preference = -3,
    log:
        IN_PATH + '/log/mapping/{project}_BinsanityRefine.log'
    run:
        shell("Binsanity-refine -f {params.indir} -l {wildcards.project}.contigs_simplyId.fa -p {params.preference} -c {input.lognorm} -o {params.outdir} >{log} 2>&1")

rule BinsanityLC:
    input:
        lognorm = rules.Coverage.output.lognorm,
    output:
        log = IN_PATH + '/assembly/{project}/binning-lc/BinSanityLC-BinsanityLC-log.txt', 
    params: 
        indir = IN_PATH + '/assembly/{project}/',
        outdir = IN_PATH + '/assembly/{project}/binning-lc',
        preference = -3,
    threads:
        THREADS
    log:
        IN_PATH + '/log/mapping/{project}_binningLC.log'
    run:
        shell("Binsanity-lc -f {params.indir} -l {wildcards.project}.contigs_simplyId.fa -p {params.preference} -c {input.lognorm} -o {params.outdir} --threads {threads} >{log} 2>&1")

rule BinsanityWF:
    input:
        lognorm = rules.Coverage.output.lognorm,
    output:
        log = IN_PATH + '/assembly/{project}/binning-wf/BinSanityWf.log', 
    params: 
        indir = IN_PATH + '/assembly/{project}/',
        outdir = IN_PATH + '/assembly/{project}/binning-wf',
        preference = -3,
    threads:
        THREADS
    log:
        IN_PATH + '/log/mapping/{project}_binningWF.log'
    run:
        shell("Binsanity-wf -f {params.indir} -l {wildcards.project}.contigs_simplyId.fa -p {params.preference} -c {input.lognorm} -o {params.outdir} --threads {threads} >{log} 2>&1")


################################################################################################

