#!/usr/bin/env python



rule NanoFilt:
    input:
        fastq = IN_PATH + "/raw/{sample}.fastq.gz",
    output:
        fastq = IN_PATH + "/clean/{sample}.fastq",
    params:
        minLength = config["minLength"],
        minQuality = config["minQuality"],
        headcrop = config["headcrop"],
    log:
        IN_PATH + "/log/NanoFilt_{sample}.log"
    run:
        shell("gunzip -c {input.fastq}  | NanoFilt -q {params.minQuality} -l {params.minLength} --headcrop {params.headcrop} > {output.fastq} 2>{log}")


################################# quality of raw data #############################
rule nanoQC:
    input:
        fastq = IN_PATH + "/raw/{sample}.fastq.gz",
    output:
        html = IN_PATH + "/qualityControl/raw/nanoQC/{sample}/nanoQC.html",
    params:
        outdir = IN_PATH + "/qualityControl/raw/nanoQC/{sample}",
    log:
        IN_PATH + "/log/nanoQC_raw_{sample}.log"
    run:
        shell("nanoQC -o {params.outdir} {input.fastq} >{log} 2>&1")

rule NanoPlot:
    input:
        fastq = IN_PATH + "/raw/{sample}.fastq.gz",
    output:
        html = IN_PATH + "/qualityControl/raw/NanoPlot/{sample}/NanoPlot-report.html",
    threads:
        THREADS
    params:
        outdir = IN_PATH + "/qualityControl/raw/NanoPlot/{sample}",
        maxLength = config["maxLength"],
        NanoPlots = config["NanoPlots"],
    log:
        IN_PATH + "/log/NanoPlot_raw_{sample}.log"
    run:
        shell("NanoPlot -t {threads} --fastq {input.fastq} --maxlength {params.maxLength} -o {params.outdir} --plots {params.NanoPlots} >{log} 2>&1")  

##############################################################################################


################################# quality of clesn data #############################
rule nanoQC_clean:
    input:
        fastq = IN_PATH + "/clean/{sample}.fastq",
    output:
        html = IN_PATH + "/qualityControl/clean/nanoQC/{sample}/nanoQC.html",
    params:
        outdir = IN_PATH + "/qualityControl/clean/nanoQC/{sample}",
    log:
        IN_PATH + "/log/nanoQC_clean_{sample}.log"
    run:
        shell("nanoQC -o {params.outdir} {input.fastq} >{log} 2>&1")

rule NanoPlot_clean:
    input:
        fastq = IN_PATH + "/raw/{sample}.fastq.gz",
    output:
        html = IN_PATH + "/qualityControl/clean/NanoPlot/{sample}/NanoPlot-report.html",
    threads:
        THREADS
    params:
        outdir = IN_PATH + "/qualityControl/clean/NanoPlot/{sample}",
        maxLength = config["maxLength"],
        NanoPlots = config["NanoPlots"],
    log:
        IN_PATH + "/log/NanoPlot_raw_{sample}.log"
    run:
        shell("NanoPlot -t {threads} --fastq {input.fastq} --maxlength {params.maxLength} -o {params.outdir} --plots {params.NanoPlots} >{log} 2>&1")  

############################################################################################

