#!/usr/bin/python
# Author: Mónica Padilla , Date: Sept 3rd, 2019
# Usage: python3 RNAtoProt.py -seq <RNAseq_file> -o <protein_file>
# Description: Takes as input a RNA string and output its translation to Protein

import sys

if __name__=='__main__':
    # Input validations
    if len(sys.argv) <= 2:
        print("\n Error: RNA sequence file was not introduced or not indicated.")
        print(" Usage: python3 RNAtoProt.py -seq <RNAseq_file> -o <protein_file>\n ")
        exit(1)

    # Recognize arguments
    outfile = 'not specified'
    while( len(sys.argv) > 1):
        if sys.argv[1] == '-seq':
            sys.argv.pop(1)
            RNAfile = sys.argv.pop(1)
        elif sys.argv[1] == '-o':
            sys.argv.pop(1)
            outfile = sys.argv.pop(1)
        elif sys.argv[1] == '-h':
            sys.argv.pop(1)
            print(" Usage: python3 RNAtoProt.py -seq <RNAseq_file> -o <protein_file> ")
            print("\tRNAseq_file must be a one-row file")
            print("\tIf no output file is specified, it will be printed ")

#########################################
#              CODON TREES              #
#########################################

def Utree(codon,aaseq):
    nt = 1
    if codon[nt] == 'U':
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('F')
        else :  aaseq.append('L')
        return
    elif codon[nt] == 'C':
        aaseq.append('S')
        return
    elif codon[nt] == 'A':
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('Y')
        else : writeOut(aaseq)
        return
    else :
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('C')
        elif codon[nt] == 'A' : writeOut(aaseq)
        else : aaseq.append('W')
        return

def Ctree(codon, aaseq):
    nt = 1
    if codon[nt] == 'U':
        aaseq.append('L')
        return
    elif codon[nt] == 'C':
        aaseq.append('P')
        return
    elif codon[nt] == 'A':
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('H')
        else : aaseq.append('Q')
        return
    else :
        aaseq.append('R')
        return

def Atree(codon,aaseq):
    nt = 1
    if codon[nt] == 'U':
        nt = 2
        if codon[nt] == 'G': aaseq.append('M')
        else :  aaseq.append('I')
        return
    elif codon[nt] == 'C':
        aaseq.append('T')
        return
    elif codon[nt] == 'A':
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('N')
        else : aaseq.append('K')
        return
    else :
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('S')
        else : aaseq.append('R')
        return

def Gtree(codon,aaseq):
    nt = 1
    if codon[nt] == 'U':
        aaseq.append('V')
        return
    elif codon[nt] == 'C':
        aaseq.append('A')
        return
    elif codon[nt] == 'A':
        nt = 2
        if codon[nt] == 'U' or codon[nt] == 'C' : aaseq.append('D')
        else : aaseq.append('E')
        return
    else :
        aaseq.append('G')
        return

##########################################
def writeOut(aaseq):
    seqstr = [str(aa) for aa in aaseq]
    if outfile != 'not specified':
        out = open(outfile, 'w')
        out.write("".join(seqstr))
    else :
        print("".join(seqstr))


#########################################
#              MAIN                     #
#########################################

def main():
    aaseq = [] # initialize amino acid sequence

    # Read RNA sequence
    infile = open(RNAfile) # read text by default
    for row in infile:
        listrow = list(row)
        n = len(listrow)
        # Read first base of each codon and identify aa in trees
        for pos in range(0,n,3):
            if listrow[pos] == 'U':
                Utree(listrow[pos:pos+3], aaseq)
            elif listrow[pos] == 'C':
                Ctree(listrow[pos:pos+3], aaseq)
            elif listrow[pos] == 'A':
                Atree(listrow[pos:pos+3], aaseq)
            elif listrow[pos] == 'G':
                Gtree(listrow[pos:pos+3], aaseq)
            elif listrow[pos] != '\n':
                print(" Error: input file was not an RNA sequence.\n")
                exit(1)

main()
