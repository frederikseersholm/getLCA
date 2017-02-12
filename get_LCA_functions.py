#!/usr/bin/env python

names=open('/PATH/to/FILE/taxdump/names.dmp','r')
nodes=open('/PATH/to/FILE/taxdump/nodes.dmp','r')


name={}
id_from_name={}
parent={}
rank={}
gi2taxid={}

lines_processed = 0
for line in names.readlines():
    lines_processed = lines_processed + 1
    if (lines_processed % 100000 == 0):
         print('names.dmp: processing line ' + str(lines_processed))
         
    text=line.replace('\t','').replace('\n','').split('|')
    text=text[0:4]
    
    id_from_name[text[1]]=text[0]
    if text[3]=='scientific name':
        name[text[0]]=text[1]          

lines_processed = 0        
for line in nodes.readlines():
    lines_processed = lines_processed + 1
    if (lines_processed % 100000 == 0):
         print('nodes.dmp: processing line ' + str(lines_processed))
    text=line.replace('\t','').replace('\n','').split('|')
    parent[text[0]]=text[1]
    rank[text[0]]=text[2]
parent['110190']='9606'
rank['110190']='subspecies'

def find_rankofparents(current_taxid):
    parents=[] 
    found = False
    while found == False:
        parents.append(rank[current_taxid])
        if (current_taxid == '1'):
            return(parents)
            found = True      
        else:
            current_taxid = parent[current_taxid]
def name1(taxid):
    textname=name[taxid]
    return(textname)
            
def find_family(current_taxid):
    parents=[] 
    found = False
    while found == False:
        parents.append(name[current_taxid])
        # find the rank of the parent
        if (current_taxid == '1'):
            return('NOFAMILY_FOUND')
            found = True
        elif (rank[current_taxid] == 'family'):
            return(name[current_taxid])
            found = True      
        else:
            current_taxid = parent[current_taxid]

def get_rank(lca):
    if lca!='NOMATCH_1_ID_only':
        name=lca.split(':')[0].replace('_',' ')
        
        try:
            taxid=id_from_name[name]
            rank1=rank[taxid]
        except:
            rank1='rank_not_found'
    else:
        rank1=lca
    return(rank1)


def find_parents(current_taxid):
    parents=[] 
    found = False
    while found == False:
        parents.append(name[current_taxid])
        # find the rank of the parent
        if (current_taxid == '1'):
            return(parents)
            found = True      
        else:
            current_taxid = parent[current_taxid]
            
def find_parents_w_rank(current_taxid):
    # first look up the taxid for the species of interest
    a=find_parents(current_taxid)
    b=find_rankofparents(current_taxid)
    return([i+';'+j for i,j in zip(a,b)])


def find_LCA(taxid1,taxid2):
    for i in find_parents(taxid1):
        if i in find_parents(taxid2):
            return(i)
            break

def taxidlist2LCA(taxid_list):
    count=0
    prev_LCA_id=[]
    for taxid in taxid_list:
        count+=1
        
        if count==1:
            prev_LCA_id=taxid
            continue
        else:
            try:
                prev_LCA_id=id_from_name[find_LCA(taxid,prev_LCA_id)]
            except:
                continue
    return(prev_LCA_id)


    
