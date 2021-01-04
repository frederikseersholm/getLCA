#!/usr/bin/env python
from get_LCA_functions import *
from get_LCA_from_samlines import *
import fileinput
import optparse

def main():
############################ Import arguments ##############
    p = optparse.OptionParser()

    p.add_option("-l", "--length", dest="length", default=0,help="Ignores reads under this length [default = 0]")
    p.add_option("-d", "--distance", dest="distance", default=0,help="BP distance for alignments to be considered equally good [default = 0]")
    p.add_option("-i", "--idthreshold", dest="id_threshold", default=0.95, help="Ignores reads where the best alignment has less than a certain percentage identity to the refenrence [default=0.95]")
    options, arguments = p.parse_args()
    infiles=arguments

    #print options.length
    print('Length threshold: '+str(options.length))
    print('Identity threshold: '+str(options.id_threshold))
    print('Distance: '+str(options.distance))
############################ Loop over input files ##############

    prev_name=[]
    prev_text=[]

    for infile in infiles:

        outfile=infile.replace('.sam','')+'.getLCA'
        print('\nWriting to: '+outfile)
        infile=open(infile,'r')
        outfile=open(outfile,'w')
        count_total=0

############################ loop over line in samfile ##############
        for line in infile.readlines():

            if line=='\n':
		              continue
            text=line.split()

            if text[0] in ['@SQ','@PG','@HD']:
                continue

############################ find LCA from all lines with the same sequence identifier (field #1 in samfile) ##############
            if text[0]!=prev_name and count_total!=0:

                outfile.write(get_LCA_from_sam(lines,options.length,options.id_threshold,options.distance))
                count_total=0

            if count_total==0:

                prev_name=text[0]
                prev_text=text
                lines=[]
            lines.append(line)
            count_total+=1
        if 'lines' in locals():
            outfile.write(get_LCA_from_sam(lines,options.length,options.id_threshold,options.distance))
        outfile.close()



if __name__ == '__main__':
    main()
