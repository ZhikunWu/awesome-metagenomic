
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


############################### LTR finder  ##########################

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
#########################################################################

####################################### RepeatScout   #######################################
rule RepeatScoutFreq:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        freq = IN_PATH + "/annotation/{project}/RepeatScout/seq_freq.txt",
    log:
        IN_PATH + '/log/RepeatScoutFreq_{project}.log'
    params:
        lmers = 14,
    run:
        shell("build_lmer_table -l {params.lmers} -sequence {input.contig} -freq {output.freq} >{log} 2>&1")


rule RepeatScoutRepeat:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
        freq = IN_PATH + "/annotation/{project}/RepeatScout/seq_freq.txt",
    output:
        repeat = IN_PATH + "/annotation/{project}/RepeatScout/seq_repeat.txt",
    params:
        lmers = 14,
    log:
        IN_PATH + '/log/RepeatScoutRepeat_{project}.log'
    run:
        shell("RepeatScout -sequence {input.contig} -freq {input.freq} -l {params.lmers} -output {output.repeat} >{log} 2>&1")

#######################################################################################




############################# LTRharvest and LTRdigest ################################
rule suffixerator:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        indexname = IN_PATH + "/assembly/{project}/assembly_index.esq",
    params:
        indexname = "assembly_index",
        outdir = IN_PATH + "/assembly/{project}/",
    log:
        IN_PATH + '/log/suffixerator_{project}.log' 
    run:
        shell("cd {params.outdir} && gt suffixerator -db {input.contig} -indexname {params.indexname} -tis -suf -lcp -des -ssp -sds -dna >{log} 2>&1")


rule LTRharvest:
    input:
        indexname = IN_PATH + "/assembly/{project}/assembly_index.esq",
    output:
        gff = IN_PATH + "/annotation/{project}/LTRharvest/assembly_ltrharvest.gff3",
        seq = IN_PATH + "/annotation/{project}/LTRharvest/assembly_ltrharvest.fa",
    params:
        indexname = IN_PATH + "/assembly/{project}/assembly_index",
    log:
        IN_PATH + '/log/LTRharvest_{project}.log' 
    run:
        shell("gt ltrharvest -index  {params.indexname}  -out {output.seq} -gff3 {output.gff}  >{log} 2>&1")


rule LTRdigest:
    input:
        gff = IN_PATH + "/annotation/{project}/LTRharvest/assembly_ltrharvest.gff3",
    output:
        digest = IN_PATH + "/annotation/{project}/LTRharvest/assembly_ltrdigest.gff3",
    params:
        indexname = IN_PATH + "/assembly/{project}/assembly_index",
    log:
        IN_PATH + '/log/LTRdigest_{project}.log' 
    run:
        shell("gt ltrdigest {input.gff} {params.indexname} > {output.digest} 2>{log}")

##########################################################################################

######################### assessment of assembly genome ####################################
rule LTRFinderSCN:
    input:
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        scn = IN_PATH + "/annotation/{project}/LTRFinder/finder.scn",
    log:
        IN_PATH + '/log/LTRFinderSCN_{project}.log'
    params:
        LTR_similarity = 0.5,
    run:
        shell("ltr_finder -D 20000 -d 1000 -L 3500 -l 100 -p 20 -C -M {params.LTR_similarity} {input.contig} > {output.scn} 2>{log}")   


rule LTR_retriever:
    input:
        finder = IN_PATH + "/annotation/{project}/LTRFinder/finder.scn",
        contig = IN_PATH + "/assembly/{project}/assembly.fasta",
    output:
        pass_list = IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta.mod.pass.list",
        out = IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta.mod.out",
    threads:
        THREADS
    params:
        LTR_retriever = config["LTR_retriever"],
        outdir = IN_PATH + "/annotation/{project}/LTRretriever",
        contig = IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta",
    log:
        IN_PATH + '/log/LTR_retriever_{project}.log'
    run:
        if not os.path.exists(params.outdir):
            os.makedirs(params.outdir)
        shell(" cp {input.contig} {params.outdir} && \
            {params.LTR_retriever}/LTR_retriever -threads {threads} -genome {params.contig} -infinder {input.finder} >{log} 2>&1 ")

rule LTR_LAI:
    input:
        contig = IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta",
        pass_list = IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta.mod.pass.list",
        out = IN_PATH + "/annotation/{project}/LTRretriever/assembly.fasta.mod.out",
    output:
        LAI = IN_PATH + "/assembly/{project}/assembly.fasta.mod.out.LAI",
    threads:
        THREADS
    params:
        LTR_retriever = config["LTR_retriever"],
        outdir = IN_PATH + "/annotation/{project}/LTRretriever",
    log:
        IN_PATH + '/log/LTR_LAI_{project}.log'
    run:
        shell("{params.LTR_retriever}/LAI -t {threads} -genome {input.contig}  -intact {input.pass_list} -all {input.out} >{log} 2>&1")
        if not os.path.exists(output.LAI):
            cmd = "touch %s" % output.LAI
            os.system(cmd)

###########################################################################################





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



###################################################################################################



################################# Tandem Repeats #####################################
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

######################################################################################
