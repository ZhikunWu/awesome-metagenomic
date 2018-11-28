#!/usr/bin/env python

################################## Assign Taxonomy using MetaPhlAn #######################

rule Bowtie2:
    input:
        fq1 = IN_PATH + '/clean/{sample}/{sample}.clean.paired.R1.fq.gz',
        fq2 = IN_PATH + '/clean/{sample}/{sample}.clean.paired.R2.fq.gz',
    output:
        sam = temp(IN_PATH + '/MetaPhlAn/mapping/{sample}.sam'),
        taxa = IN_PATH + "/MetaPhlAn/{sample}.txt",
    threads:
        THREADS
    params:
        MetaPhlAnIndex = config["MetaPhlAnIndex"],
    log:
        IN_PATH + '/log/MetaPhlAn/{sample}_bowtie2.log'
    run:
        shell("bowtie2 -x {params.MetaPhlAnIndex} -1 {input.fq1} -2 {input.fq2} -S {output.sam} --threads {threads} >{log} 2>&1")
        shell("metaphlan2.py --input_type sam   --nproc {threads} --tax_lev a --ignore_eukaryotes {output.sam} {output.taxa} 2>>{log}")


rule MetaPhlAn:
    input:
        sam = rules.Bowtie2.output.sam,
    output:
        taxa = IN_PATH + "/MetaPhlAn/{sample}.txt",
    threads:
        THREADS
    log:
        IN_PATH + '/log/MetaPhlAn/{sample}_MetaPhlAn.log'
    run:
        # shell("metaphlan2.py --input_type multifastq {input.fq1},{input.fq2} --nproc {threads} --tax_lev a --ignore_eukaryotes -o {output.taxa} --bowtie2out {output.sam} >{log} 2>&1")
        shell("metaphlan2.py --input_type sam   --nproc {threads} --tax_lev a --ignore_eukaryotes {input.sam} {output.taxa} >{log} 2>&1")

rule MergeTaxa:
    input:
        taxa = expand(IN_PATH + "/MetaPhlAn/{sample}.txt", sample=SAMPLES),
    output:
        taxa = IN_PATH + "/MetaPhlAn/Samples_taxonomy.txt",
    params:
        #It is a script modifed from MetaPhlAn
        merge_metaphlan_tables = SRC_DIR + "/merge_metaphlan_tables.py",
        # merge_metaphlan_tables = config["merge_metaphlan_tables"],
    log:
        IN_PATH + '/log/MetaPhlAn/merge_MetaPhlAn.log'
    run:
        INPUTS = ",".join(input.taxa)
        shell("python {params.merge_metaphlan_tables} {INPUTS} > {output.taxa} 2>{log}")


rule HclustHeatmap:
"""
This picture was plotted using script in MetaPhlAn, it is not beatuful.
"""
    input:
        taxa = rules.MergeTaxa.output.taxa,
    output:
        png = IN_PATH + "/MetaPhlAn/Samples_taxonomy_heatmap.png",
    params:
        metaphlan_hclust_heatmap = config["metaphlan_hclust_heatmap"],
        colour = "YlOrRd",
        topTaxa = 25,
        minValue = 0.05
    log:
        IN_PATH + '/log/MetaPhlAn/merge_MetaPhlAn_heatmap.log'
    run:
        shell("python {params.metaphlan_hclust_heatmap} -c {params.colour} --top {params.topTaxa} --minv {params.minValue} -s log --in {input.taxa} --out {output.png} >{log} 2>&1")


###############################################################################################