#!/usr/bin/env python
import yaml
import os
import sys


IN_PATH = config["IN_PATH"]
PIPE_DIR = config["PIPE_DIR"]
THREADS = config["THREADS"]
ThreadFold = config["ThreadFold"]
SAMPLES = config["SAMPLES"]
PROJECTS = config["PROJECTS"]


include: PIPE_DIR + "/Nano_QualityControl.rule.py"
include: PIPE_DIR + "/GenePridiction.rule.py"


rule all:
    input:
        expand(IN_PATH + "/clean/{sample}.fastq", sample=SAMPLES),
        expand(IN_PATH + "/qualityControl/raw/nanoQC/{sample}/nanoQC.html", sample=SAMPLES),
        expand(IN_PATH + "/qualityControl/raw/NanoPlot/{sample}/NanoPlot-report.html", sample=SAMPLES),
        expand(IN_PATH + '/annotation/{project}/Prokka/assembly.faa', project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/tRNAscan/assembly_tRNA_gene.fna", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/RepeatMasker/assembly.fasta.out", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/RepeatModeler/assembly_RepeatModeler.txt", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/LTRFinder/LTR.txt", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/TandemRepeatFinder/TandemRepeat.txt", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/LTRFinder/finder.scn", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta.mod.pass.list", project=PROJECTS),
        expand(IN_PATH + "/assembly/{project}/assembly.fasta.mod.out.LAI", project=PROJECTS),
        expand(IN_PATH + "/assembly/{project}/assembly_index.esq", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/LTRharvest/assembly_ltrharvest.gff3", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/LTRharvest/assembly_ltrdigest.gff3", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/RepeatScout/seq_freq.txt", project=PROJECTS),
        expand(IN_PATH + "/annotation/{project}/RepeatScout/seq_repeat.txt", project=PROJECTS),