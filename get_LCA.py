from get_LCA_functions import *
from get_LCA_from_samlines import *
import fileinput
import optparse

def main():
############################ Import arguments ##############    
    p = optparse.OptionParser()

    options, arguments = p.parse_args()
    infiles=arguments
    
############################ Loop over input files ##############
    
    prev_name=[]
    prev_text=[]
    
    for infile in infiles:

        outfile=infile.replace('.sam','')+'.getLCA'
        print '\nWriting to: '+outfile
        infile=open(infile,'r')
        outfile=open(outfile,'w')
        count_total=0
        
############################ loop over line in samfile ##############        
        for line in infile.readlines():
            
            
            text=line.split()
            if text[0] in ['@SQ','@PG','@HD']:
                continue
            
############################ find LCA from all lines with the same sequence identifier (field #1 in samfile) ##############   
            if text[0]!=prev_name and count_total!=0:
                
                outfile.write(get_LCA_from_sam(lines))
                count_total=0
            
            if count_total==0:
    
                prev_name=text[0]
                prev_text=text
                lines=[]
            lines.append(line)
            count_total+=1
        if 'lines' in locals():
            outfile.write(get_LCA_from_sam(lines))
        outfile.close()
           
        
    
if __name__ == '__main__':
    main()   



