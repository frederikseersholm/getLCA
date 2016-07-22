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
        print 'No output file specified, writing to: '+outfile
    else:
        outfile=options.outfile
###################
    count=0
    gi_list=[]
    for record in SeqIO.parse(fastafile,format='fasta'):

        gi_nr=record.description.split('|')[1]
        if gi_nr not in gi_list:
            gi_list.append(gi_nr)
            
###################
    gi_dict={}
    for gi_nr in gi_list:
        gi_dict[gi_nr]='TAXID_NOT_FOUND'
####################
    count=0
    filelist=glob.glob('/Users/frederikseersholm1/Frederik/Uni/Kandidat/Master_thesis/midden_project_merged/Databases/gi_taxid_nucl.dmp.*')

    for gi_name in filelist:
        count+=1
        #if count>1:
        #    break
        print '\nprocessing file '+str(count)+' of '+str(len(filelist))+'\n'
        gi=open(gi_name,'r')
        gi2taxid={}
        
        lines_processed = 0
        for line in gi.readlines():
            lines_processed = lines_processed + 1
            if (lines_processed % 5000000 == 0):
                sys.stdout.write('-')
            
            text=line.split()
            gi2taxid[text[0]]=text[1]
        
        gi.close()
        
        for gi_nr in gi_list:
            if gi_dict[gi_nr]=='TAXID_NOT_FOUND':
                try:
                    gi_dict[gi_nr]=gi2taxid[gi_nr]
                
                except:
                    gi_dict[gi_nr]='TAXID_NOT_FOUND'
        
    print '\n"gi_taxid_nucl.dmp"-files loaded into memory \n'    
    count=0
    outfile=open(outfile,'w')
    for record in SeqIO.parse(fastafile,format='fasta'):
        #count+=1
        #if count>100:
        #    break
        
        #print record.description.split('|')[1]
        try:
            gi=record.description.split('|')[1]
            #print gi
            #print gi_dict[gi]
            taxid=gi_dict[gi]
        except:
            taxid='TAXID_NOT_FOUND_in_dict'
            #print gi2taxid[gi]
            
        record.description=taxid+'|'+record.description
        #print record.description+'\t'+str(len(record))
        
        
        outfile.write('>'+str(record.description)+'\n'+str(record.seq)+'\n')
    outfile.close()

#####################
if __name__ == '__main__':
    main()