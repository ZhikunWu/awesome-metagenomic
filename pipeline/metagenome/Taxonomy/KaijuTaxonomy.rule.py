#!/usr/bin/env python

################################ Taxonomy assignment with kaiju ##########################

## Taxonomy assignment based on 8407 genomes from NCBI using kaiju 
rule kaiju:
    input:
        fq1 = IN_PATH + '/clean/{sample}/{sample}.clean.paired.R1.fq.gz',
        fq2 = IN_PATH + '/clean/{sample}/{sample}.clean.paired.R2.fq.gz',
    output:
        out = IN_PATH + '/kaiju/{sample}.kaiju.txt',
    threads:
        THREADS
    params:
        dmp = config["kaiju_nodes"],
        fmi = config["kaiju_db"],
    log:
        IN_PATH + '/log/kaiju/{sample}_kaiju.log'
    run:
        shell('kaiju -t {params.dmp} -f {params.fmi} -z {threads} -i {input.fq1} -j {input.fq2} -o {output.out} >{log} 2>&1')

rule kaiju2Krona:
    input:
        kaiju = rules.kaiju.output.out,
    output:
        krona = IN_PATH + '/kaiju/{sample}.krona.txt',
    params:
        node = config["kaiju_nodes"],
        name = config["kaiju_names"],
    log:
        IN_PATH + '/log/kaiju/{sample}_kaiju2Krona.log'
    run:
        shell('kaiju2krona -t {params.node} -n {params.name} -i {input.kaiju} -o {output.krona} >{log} 2>&1')

rule Kronahtml:
    input:
        krona = rules.kaiju2Krona.output.krona,
    output:
        html = IN_PATH + '/kaiju/{sample}.krona.html',
    log:
        IN_PATH + '/kaiju/{sample}_Kronahtml.log'
    run:
        shell('ktImportText -o {output.html} {input.krona} >{log} 2>&1')

rule TaxaContent:
    input:
        kaiju = rules.kaiju.output.out,
    output:
        content = IN_PATH + '/kaiju/{sample}.taxa_content.txt',
        # taxa = IN_PATH + '/kaiju/{sample}.taxonomy_name.txt',
    params:
        dmp = config["kaiju_nodes"],
        name = config["kaiju_names"],
        taxonomic_rank = 'species',
    log:
        IN_PATH + '/kaiju/{sample}_TaxaContent.log'
    run:
        #-u  Unclassified reads are not contained in the output.
        shell('kaijuReport  -t {params.dmp} -n {params.name} -i {input.kaiju} -r {params.taxonomic_rank}  -u -p -o {output.content} >{log} 2>&1')
        # shell('addTaxonNames  -t {params.dmp} -n {params.fmi} -i {input.kaiju}  -u -p -o {output.taxa} >>{log}')


#################################################################################################