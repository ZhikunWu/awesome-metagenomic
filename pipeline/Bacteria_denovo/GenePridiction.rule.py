
rule Prokka:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        ffn = IN_PATH + '/annotation/{project}/Prokka/assembly.ffn',
        faa = IN_PATH + '/annotation/{project}/Prokka/assembly.faa',
    log:
        IN_PATH + '/log/prokkaAnno_{project}.log'
    threads:
        THREADS 
    params:
        out_dir = IN_PATH + '/annotation/{project}/Prokka',
    run:
        #Bio-perl is unfortunately not rebuilt for perl 5.26 yet.
        #So create the conda envoronment prokka
        shell("echo 'source activate prokka && prokka {input.contig} --outdir {params.out_dir} --prefix assembly --cpus {threads} --force  >> {log} 2>&1' ")
        shell('source activate prokka && prokka {input.contig} --outdir {params.out_dir} --prefix assembly --cpus {threads} --force  >> {log} 2>&1')


rule tRNAscanSE:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        tRNA = IN_PATH + "/annotation/{project}/tRNAscan/assembly_tRNA.fna",
        gene = IN_PATH + "/annotation/{project}/tRNAscan/assembly_tRNA_gene.fna",
        structure = IN_PATH + "/annotation/{project}/tRNAscan/assembly_tRNA_structure.fna",
        stats = IN_PATH + "/annotation/{project}/tRNAscan/assembly_tRNA_structure_stats.fna",
    threads:
        THREADS 
    log:
        IN_PATH + '/log/tRNAscanSE_{project}.log' 
    run:
        shell("tRNAscan-SE {input.contig}  -o {output.tRNA}  -f {output.structure} -m {output.stats} -a {output.gene} --thread {threads} >{log} 2>&1")

############################### detect TEs based on Repbase library #######################
rule RepeatMasker:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        out = IN_PATH + "/annotation/{project}/RepeatMasker/assembly.fasta.out",
    params:
        outdir = IN_PATH + "/annotation/{project}/RepeatMasker/",
        species = config["species"],
    threads:
        THREADS
    log:
        IN_PATH + '/log/RepeatMasker_{project}.log' 
    run:
        shell("RepeatMasker -parallel {threads} -species {params.species}  -html -gff -dir {params.outdir} {input.contig} >{log} 2>&1")
##############################################################################################


############################### construct de novo repeat library  ##########################
rule BuildDatabase:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        nhr = IN_PATH + "/annotation/{project}/RepeatModeler/assembly.nhr",
    params:
        prefix = IN_PATH + "/annotation/{project}/RepeatModeler/assembly",
    log:
        IN_PATH + '/log/BuildDatabase_{project}.log' 
    run:
        shell('echo "BuildDatabase -name {params.prefix} {input.contig} >{log} 2>&1" ')
        shell("BuildDatabase -name {params.prefix} {input.contig} >{log} 2>&1")


rule RepeatModeler:
    input:
        nhr = IN_PATH + "/annotation/{project}/RepeatModeler/assembly.nhr",
    output:
        out = IN_PATH + "/annotation/{project}/RepeatModeler/assembly_RepeatModeler.txt",
    params:
        prefix = IN_PATH + "/annotation/{project}/RepeatModeler/assembly",
    log:
        IN_PATH + '/log/RepeatModeler_{project}.log' 
    run:
        shell("RepeatModeler -database {params.prefix} > {output.out} 2>&1")


rule LTRFinder:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        figure = IN_PATH + "/annotation/{project}/LTRFinder/figure.txt",
        ltr = IN_PATH + "/annotation/{project}/LTRFinder/LTR.txt",
    params:
        LTRFinderFormat = config["LTRFinderFormat"],
    log:
        IN_PATH + '/log/LTRFinder_{project}.log' 
    run:
        shell("ltr_finder {input.contig}  -w {params.LTRFinderFormat} -f {output.figure} > {output.ltr} 2>{log}")

###################################################################################################



rule TandemRepeatFinder:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        trf =  IN_PATH + "/annotation/{project}/TandemRepeatFinder/TandemRepeat.txt",
    params:
        TandemRepeat = config["TandemRepeat"],
        outdir = IN_PATH + "/annotation/{project}/TandemRepeatFinder",
    log:
        IN_PATH + '/log/TandemRepeatFinder_{project}.log' 
    run:
        ### add "-h" to suppress html output
        if not os.path.exists(params.outdir):
            os.makedirs(params.outdir)
        shell("cd {params.outdir} && trf {input.contig} {params.TandemRepeat} -f -d -m -ngs > {output.trf} 2>{log} && cd -")
