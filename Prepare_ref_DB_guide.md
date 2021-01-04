#Download and Format Full Mitochondrial Genomes Database for getLCA

Below is a step-by-step guide to prepare the reference database in order to apply the python scripts included in this folder.

1) Create a folder for DB files
```
    mkdir DBfiles_getLCA
    cd DBfiles_getLCA
```
2) Download and unpack mitochondrial reference database in fasta format

    wget ftp://ftp.ncbi.nlm.nih.gov/refseq/release/mitochondrion/mitochondrion.?.1.genomic.fna.gz
    gunzip mitochondrion.?.1.genomic.fna.gz
    cat mitochondrion.?.1.genomic.fna >> mitochondrion.genomic.fasta
    rm mitochondrion.?.1.genomic.fna
    
3) Download the NCBI index with gi numbers and their corresponding taxids

    wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/gi_taxid_nucl.dmp.gz
    gunzip gi_taxid_nucl.dmp.gz
    split -l 50000000 gi_taxid_nucl.dmp gi_taxid_nucl.dmp.
    rm gi_taxid_nucl.dmp
    
4) Change path to NCBI index in the file add_taxid2db.py:
open file 'add_taxid2db.py' on line 35, add the correct path to your 'gi_taxid_nucl.dmp' files

5) Add taxids to the fasta identifier in the database using the script 'add_taxid2db.py'

    python ../add_taxid2db.py mitochondrion.genomic.fasta

OPTIONAL, if you're using bowtie: 
6) Build bowtie2 index

    bowtie2-build mitochondrion.genomic.taxid.fasta mitochondrion.genomic.taxid.fasta

DONE!
Your DB should be in 'DBfiles_getLCA/mitochondrion.genomic.taxid.fasta
