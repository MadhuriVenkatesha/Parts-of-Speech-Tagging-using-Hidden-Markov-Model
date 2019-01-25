import math
import sys
def add_transition_emission(pre_tag,word,trans,emis,tag_set): #This function initializes the transition counts of a sentence 
    if word=='':
        first_tag='END'
    else:
        ref=word.split('/')
        first_word=''.join(ref[:-1])
        first_tag=ref[-1]
        tag_set.append(first_tag)
        try:
            temp=emis[first_tag]
        except:
            emis[first_tag]={}
        try_catch(emis,first_tag,first_word)
        """try:
            emis[first_tag][first_word]+=1
        except:
            emis[first_tag][first_word]=1"""
    try:
        temp=trans[pre_tag]
    except:
        trans[pre_tag]={}
    try_catch(trans,pre_tag,first_tag)
    """try:
        trans[pre_tag][first_tag]+=1
    except:
        trans[pre_tag][first_tag]=1"""
    return first_tag
def calc_trans_prob(my_dict,my_dict_prob,file_write):#Calculates the transition probabilites of a sentence 
    for fir_tag,sec_tag in my_dict.items():
        count=0
        for tag,val in sec_tag.items():
            count+=val
        for tag,val in sec_tag.items():
            try:
                temp=my_dict_prob[fir_tag]
            except:
                my_dict_prob[fir_tag]={}
            my_dict_prob[fir_tag][tag]=float(val)/count
            file_write.write('P('+fir_tag+'/'+tag+')= '+str(my_dict_prob[fir_tag][tag])+' '+fir_tag+' '+tag+'\n')
    file_write.write('\n')
def calc_emis_prob(my_dict,my_dict_prob,file_write):#Calculates the emission probabilites of a sentence 
    for fir_tag,sec_tag in my_dict.items():
        count=0
        for tag,val in sec_tag.items():
            count+=val
        for tag,val in sec_tag.items():
            try:
                temp=my_dict_prob[tag]
            except:
                my_dict_prob[tag]={}
            my_dict_prob[tag][fir_tag]=float(val)/count
            file_write.write('P('+tag+'/'+fir_tag+')= '+str(my_dict_prob[tag][fir_tag])+' '+tag+' '+fir_tag+'\n')
    file_write.write('\n')
def try_catch(my_dic,fir_tag,las_tag):
    try:
        my_dic[fir_tag][las_tag]+=1
    except:
        my_dic[fir_tag][las_tag]=1
def smoothing_transitions(trans,tag_set): #This functional smoothens the transitions using Laplace smoothing
      for i in tag_set:
          try_catch(trans,'start',i) #The start of sentance is taken as 'start'
          try_catch(trans,i,'END') #The end of sentance is taken as 'END'
          for j in tag_set:
              try_catch(trans,i,j)
def Train(inp_file_name):
    file_content=open(inp_file_name,'r')
    trans=dict()
    emis=dict()
    tag_set=[]
    for line in file_content: #reading each line from the input file and processing it
        line_words=line.split()
        word_tag=add_transition_emission('start',line_words[0],trans,emis,tag_set)
        pre_tag=word_tag
        for word in line_words[1:]:
            pre_tag=add_transition_emission(pre_tag,word,trans,emis,tag_set)
        pre_tag=add_transition_emission(pre_tag,'',trans,emis,tag_set)
    tag_set=set(tag_set)
    smoothing_transitions(trans,tag_set)
    trans_prob=dict()
    emis_prob=dict()
    file_write=open('hmmmodel.txt','w')
    file_write.write('Transition probabilities'+'\n\n') #Writing the transition probabilities to an output file
    calc_trans_prob(trans,trans_prob,file_write)
    file_write.write('Emission probabilities'+'\n\n') #Writing the emission probabilities to an output file
    calc_emis_prob(emis,emis_prob,file_write) 
Train(sys.argv[1])
    
