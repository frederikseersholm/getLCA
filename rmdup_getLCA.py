import optparse

def main():
############################ Import arguments ##############    
    p = optparse.OptionParser()
    options, arguments = p.parse_args()
    infiles=arguments

############################ Loop over input files ##############
    for infile in infiles:
        outfile=infile.replace('.getLCA','')+'.rmdup.getLCA'
        print '\nWriting to: '+outfile
        outfile=open(outfile,'w')

        seqs=[]
        count=0
        seq_count=0
        for line in open(infile,'r').readlines():
            seq=line.split()[6].strip()
            seq_count+=1
            if seq not in seqs:
                count+=1
                outfile.write(line)
                seqs.append(seq)
        outfile.close
        print 'Total seqs '+str(seq_count)
        print 'Unique seqs: '+str(count)
        print 'Unique proportion: '+str(round(float(count)*100/seq_count,1))+'%'
if __name__ == '__main__':
    main()
