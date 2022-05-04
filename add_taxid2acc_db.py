#!/usr/bin/env python
import optparse
import sys

#from get_LCA_functions import *
from Bio import SeqIO

import glob
def main():

    p = optparse.OptionParser()
    p.add_option('--outfile', '-o')
    options, arguments = p.parse_args()
    fastafile=arguments[0]
    if options.outfile is None:
        outfile=fastafile.replace('.fasta','.taxid.fasta')
        print('No output file specified, writing to: '+outfile)
    else:
        outfile=options.outfile
###################
    count=0
    gi_list=[]
    for record in SeqIO.parse(fastafile,format='fasta'):
        if '|' in record.description:
            split_header=record.description.split('|')
            gi_nr=[split_header[i+1] for i,j in enumerate(split_header) if j=='ref'][0]
            if gi_nr not in gi_list:
                gi_list.append(gi_nr)
        else:
            split_header=record.description.split(' ')
            gi_nr=split_header[0]
            if gi_nr not in gi_list:
                gi_list.append(gi_nr)
            else:
                continue
###################
    gi_dict={}
    for gi_nr in gi_list:
        gi_dict[gi_nr]='TAXID_NOT_FOUND'
####################
    count=0

    #filelist=glob.glob('/willerslev/users-shared/science-snm-willerslev-cqr376/software/getLCA/DBfiles_getLCA/fix_add_taxid2acc_db/nucl_gb.test')
    #filelist=glob.glob('/willerslev/users-shared/science-snm-willerslev-cqr376/software/getLCA/DBfiles_getLCA/Accession2taxid/nucl_gb.accession2taxid.ae')
    filelist=glob.glob('/willerslev/users-shared/science-snm-willerslev-cqr376/software/getLCA/DBfiles_getLCA/Accession2taxid/nucl_*.accession2taxid*.??')
    for gi_name in filelist:
        count+=1
        #if count>2:
        #    break
        print('\nprocessing file '+str(count)+' of '+str(len(filelist))+'\n')
        gi=open(gi_name,'r')
        gi2taxid={}

        lines_processed = 0
        for line in gi.readlines():
            lines_processed = lines_processed + 1
            if (lines_processed % 5000000 == 0):
                sys.stdout.write('-')

            text=line.split()
            gi2taxid[text[1]]=text[2]

        gi.close()

        for gi_nr in gi_list:
            if gi_dict[gi_nr]=='TAXID_NOT_FOUND':
                try:
                    gi_dict[gi_nr]=gi2taxid[gi_nr]

                except:
                    gi_dict[gi_nr]='TAXID_NOT_FOUND'


    print('\n"gi_taxid_nucl.dmp"-files loaded into memory \n')
    count=0
    outfile=open(outfile,'w')
    for record in SeqIO.parse(fastafile,format='fasta'):
        #count+=1
        #if count>100:
        #    break
        if '|' in record.description:
            split_header=record.description.split('|')
            gi=[split_header[i+1] for i,j in enumerate(split_header) if j=='ref'][0]

        else:
            split_header=record.description.split(' ')
            gi=split_header[0]
        #else:
        #    gi='not_found'

        taxid=gi_dict.get(gi,'TAXID_NOT_FOUND_in_dict')
        record.description=taxid+'|'+record.description
        outfile.write('>'+str(record.description)+'\n'+str(record.seq)+'\n')
    outfile.close()

#####################
if __name__ == '__main__':
    main()
