#!/usr/bin/python3
# @author: Joseph Sevigny

from Bio import SeqIO
import os, gzip

class mess_with_font:
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    Red = '\033[91m'
    Green = '\033[92m'
    Blue = '\033[94m'
    Yellow = '\033[93m'
    Grey = '\033[90m'
    Default = '\033[99m'

def extract_file_names(search_term, path_to_dir):
    '''extracts a set of file names that contain a search term and returns it as a list'''
    filenames = []
    file_list = os.listdir(path_to_dir)
    for file_name in file_list:
        if search_term in file_name:
           filenames.append(file_name)
    return filenames

def rev_comp(seq):
    """Reverses, complements and returns sequence"""
    rev_seq = seq[::-1]
    compliment_dict = {'A':'T', 'T':'A', 'C':'G', 'G':'C'}
    rev_comp_seq = ''
    for nuc in rev_seq:
        if nuc in ['A', 'T', 'G', 'C']:
            rev_comp_seq += compliment_dict[nuc]
    return rev_comp_seq

def extract_region(fasta, header_search, start, stop, output_name, direction, header_addition):
    """ PURPOSE: Extracts a specified region from a fasta using header_search, coordinates, and direction(+-),
                        and writes to append able output
        USAGE: extract_region(fasta, header_search, start, stop, output_name, direction, header_addition)"""
    with open(output_name, "a") as my_fasta:
        for seq_record in SeqIO.parse(fasta, "fasta"):
            if header_search in str(seq_record.id):
                my_seq = (str(seq_record.seq[start-1:stop]))
                my_fasta.write(">" + header_addition + str(len(my_seq)) + "_"+ str(seq_record.id) + "\n")
                if direction == "-":
                    rev_seq = rev_comp(my_seq)
                    my_fasta.write(rev_seq + "\n")
                else:
                    my_fasta.write(my_seq + "\n")

def parse_gff(gff_line):
    '''input a line from a gff and return the important attributes'''
    try:
        header, program, gene_identity, start, stop, tmp, direction, product = gff_line.split("\t")
    except ValueError:
        header, program, gene_identity, start, stop, tmp, direction, tmp2, product = gff_line.split("\t")
        #gene_identity = gene_id[5:11]
    ###try and convert all to the same format
    #gene_identity = gene_identity.lower(); gene_identity = gene_identity.replace("nd", "nad").replace("cyt","co").replace("\n", "")
    return header, gene_identity, start, stop, direction, product

def match_fasta_gff(fastas, gffs):
    fa_gff_dict = {}
    for fa in fastas:
        for gff in gffs:
            if gff.endswith(".gz"):
                tmp_gff = gff.replace(".gff.gz", '')
            else:
                tmp_gff = gff.replace(".gff", '') # just make sure .gz is not in the line
            tmp_gff = tmp_gff.replace("_", ""); tmp_gff = tmp_gff.replace("-", "") 
            fatmp = fa.replace("_", ""); fatmp = fatmp.replace("-", "") 
            if tmp_gff in fatmp:
                fa_gff_dict[fa] = gff # fills the dictionary with fasta and matching gff

    return fa_gff_dict