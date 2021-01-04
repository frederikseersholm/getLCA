# getLCA

## GUIDE TO RUN THE SCRIPT getLCA.py

#### 1) Download and unpack the getLCA master
```
git clone https://github.com/frederikseersholm/getLCA
cd getLCA
```
2) Download the NCBI taxonomy files, names.dmp and nodes.dmp
```
    mkdir taxdump
    wget ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz
    tar -xzf taxdump.tar.gz -C taxdump
    rm taxdump.tar.gz
```
3) Update the paths to names.dmp and nodes.dmp on line 3 and 4 in the script get_LCA_functions.py

4) Map reads to DB using bowtie (or a mapper of your choice) - see [Prepare_ref_DB_guide.md](https://github.com/frederikseersholm/getLCA/blob/master/Prepare_ref_DB_guide.md) 
 ```
    bowtie2 -k 500 -p 24 -f -x $DB -U $infile --no-unal > $filename.unsorted.sam
 ```   
5) Sort samfile
```
    sort -k1 $filename.unsorted.sam > $filename.sam
    rm $filename.unsorted.sam
```
6) Assign LCA
```
    python get_LCA.py $filename.sam
```    
OPTIONAL:
7) Report a sorted list of vertebrate species assigned below family level:
```
    cat $filename.getLCA|grep -v 'NOMATCH'|grep 'genus\|family\|species\|subfamily\|subspecies\|subgenus'|grep 'Vertebrata'|awk '{print $2}'|sort|uniq -c|sort -nk1|awk -F ':' '{print $1}'
```
