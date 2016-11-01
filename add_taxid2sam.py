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
    samfile=arguments[0]
    if options.outfile is None:
        outfile=samfile.replace('.sam','.taxid.sam')
        print 'No output file specified, writing to: '+outfile
    else:
        outfile=options.outfile
    samfile1=open(samfile,'r')
###################
    count=0
    gi_list=[]
    for line in samfile1.readlines():
	record_description=line.split('\t')[2]
        gi_nr=record_description.split('|')[1]
        if gi_nr not in gi_list:
            gi_list.append(gi_nr)
    samfile1.close()            
###################
    gi_dict={}
    for gi_nr in gi_list:
        gi_dict[gi_nr]='TAXID_NOT_FOUND'
####################
    count=0
    filelist=glob.glob('/home/trold13/data/genomes/DBfiles_getLCA/gi_taxid_nucl.dmp.*')

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
    samfile1=open(samfile,'r')
    for line in samfile1.readlines():
        #count+=1
        #if count>100:
        #    break
        
        #print record.description.split('|')[1]
        try:
	    record_description=line.split('\t')[2]
            gi=record_description.split('|')[1]
            #print gi
            #print gi_dict[gi]
            taxid=gi_dict[gi]
        except:
            taxid='TAXID_NOT_FOUND_in_dict'
            #print gi2taxid[gi]
         
        outline=line.split('\t')
	outline[2]=taxid+'|'+outline[2]
        
        
        outfile.write('\t'.join(outline))
    outfile.close()

#####################
if __name__ == '__main__':
    main()
