#!/usr/bin/env python
import subprocess
import argparse
import random
import tinyfasta
import os
import multiprocessing

#usage: python /home/wzk/anaconda3/envs/qiime/bin/signalp-4.1/SignalParallel.py --fasta  MetaContig.faa --threads 10 --outdir signalP --organism  euk

__author__ = "Zhikun Wu"
__email__ = "598466208@qq.com"
__date__ = "2018.11.06"

def check_dir(outdir):
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    if not outdir.endswith("/"):
        outdir = outdir + "/"
    return outdir

def split_file(fa_file, threads, outdir):
    print("@@@ Start to split the input fasta file to several files based on the threads.")
    outdir = outdir.rstrip("/") + "_temp"
    outdir = check_dir(outdir)   
    threads = int(threads)
    cmd = "grep -c '^>' %s" % fa_file
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    out, err = p.communicate()
    seqNum = int(out.strip())
    ### Sequence limit reached: Max 10000 sequences are allowed for SignalP
    maxRun = 10000

    ### get the file number and read number per file.
    if seqNum > threads * maxRun:
        if seqNum % maxRun == 0:
            fileNum = seqNum // maxRun
        else:
            fileNum = seqNum // maxRun + 1
        readNum = maxRun
    else:
        if seqNum // threads == 0:
            readNum = seqNum / threads
        else:
            readNum = seqNum // (threads-1)
        fileNum = threads
    count = 0
    preRegion = 0
    file = outdir + 'temp-' + str(preRegion)
    file_h = open(file, "w")
    for record in tinyfasta.FastaParser(fa_file):
        desc = str(record.description)
        seq = str(record.sequence)
        count += 1
        region = count // readNum
        if region == preRegion + 1 and count % readNum != 0:
            file_h.close()
            preRegion = region
            file = outdir + 'temp-' + str(preRegion)
            file_h = open(file, "w")
            file_h.write("%s\n%s\n" % (desc, seq))
        else:
            file_h.write("%s\n%s\n" % (desc, seq))
    file_h.close()


def run_signalP(file, organism, file_out):
    cmd = "signalp -t %s -f short %s >  %s" % (organism, file, file_out)
    os.system(cmd)


def run_signalP_parallel(outdir, organism):
    print("@@@ Run SignalP to predict the secreted protein parallelly.")
    tempdir = outdir.rstrip("/") + "_temp/"
    tempOut = outdir.rstrip("/") + "_out/"
    tempOut = check_dir(tempOut)
    files = os.listdir(tempdir)
    out_files = [tempOut + f for f in files]
    files = [tempdir + f for f in files]
    Process = []
    for i in range(len(files)):
        process = multiprocessing.Process(target=run_signalP, args=(files[i], organism, out_files[i]))
        Process.append(process)

    for p in Process:
        p.start()
    for p in Process:
        p.join()


def join_out_files(outdir):
    print("@@@ Successfully run SignalP, now combine the results and delete temp directories.")
    tempdir = outdir.rstrip("/") + "_temp/"
    tempOut = outdir.rstrip("/") + "_out/"
    out_file = outdir + "gene_secreted_protein_prediction.xls"
    files = os.listdir(tempOut)
    files = [tempOut + f for f in files]
    for i in range(len(files)):
        if i == 0:
            cmd = "cat %s > %s" % (files[i], out_file)
        else:
            cmd = "sed '1,2d' %s >> %s" % (files[i], out_file)
        os.system(cmd)

    ## delete the temp directory
    cmd1 = "rm -r %s" % tempdir
    cmd2 = "rm -r %s" % tempOut
    os.system(cmd1)
    os.system(cmd2)
    print("@@@ Finish all process.")




def main():
    parser = argparse.ArgumentParser(description="Run SignalP to prediction the protein parallelly.")
    parser.add_argument("-f", "--fasta", help="The input fasta file.")
    parser.add_argument("-t", "--threads", help="The threads to run SignalP.")
    parser.add_argument("-g", "--organism", help="The organism, such as [euk|gram+|gram-]")
    parser.add_argument("-o", "--outdir", help="The output directory.")
    args = parser.parse_args()

    outdir = check_dir(args.outdir)
    split_file(args.fasta, args.threads, outdir)
    run_signalP_parallel(outdir, args.organism)
    join_out_files(outdir)


if __name__ == "__main__":
    main()