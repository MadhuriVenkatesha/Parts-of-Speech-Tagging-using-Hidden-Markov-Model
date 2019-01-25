import operator
import sys
def extract_prob(my_dict,fir_tag,sec_tag,prob):#extracting the transition and emission probabilities from the model file
    try:
        temp=my_dict[fir_tag]
    except:
        my_dict[fir_tag]={}
    my_dict[fir_tag][sec_tag[:-1]]=prob
    
def tag_file(file_name):
    trans=dict()
    emis=dict()
    val=None
    tag_types=[]
    model_file=open('hmmmodel.txt','r')
    for line in model_file:
        words=line.split(' ')
        if words[0]=='\n':
            continue
        if words[0]=="Transition":
            my_dict=trans
            val=1
            continue
        elif words[0]=="Emission":
            my_dict=emis
            val=2
            continue
        extract_prob(my_dict,words[-2],words[-1],float(words[-3]))
    for key,val in trans.items():
        """print key,":",val"""
        if key !='start':
            tag_types.append(key)
    """for key,val in emis.items():
        print key,":",val"""
    Viterbi_tagging(emis,trans,file_name,tag_types)
    
def path_calc(curr_tags,Vit,ind,trans,back_ptr): #This function calculates the tag of every word and keeps track of it 
    poss_like_hood={}
    print "word "+str(ind)
    Vit[ind+1]={}
    back_ptr[ind+1]={}
    for curr_tag,emis_prob in curr_tags.items():
        poss_like_hood[curr_tag]={}
        for pre_Vit_tag,pre_Vit_prob in Vit[ind].items():
            poss_like_hood[curr_tag][pre_Vit_tag] = float(pre_Vit_prob)*emis_prob*trans[pre_Vit_tag][curr_tag]
            print "Curr tag "+curr_tag+" : "+"Previous tag "+pre_Vit_tag+" transition "+str(trans[pre_Vit_tag][curr_tag])
        max_tag=max(poss_like_hood[curr_tag].iteritems(), key=operator.itemgetter(1))[0]
        print "Max tag "+max_tag+" Max Val "+str(poss_like_hood[curr_tag][max_tag])
        Vit[ind+1][curr_tag]=poss_like_hood[curr_tag][max_tag]
        back_ptr[ind+1][curr_tag]=max_tag
    print Vit[ind+1]
    print "-------------------------------------------------------------------------------------------------------"
def Viterbi_tagging(emis,trans,file_name,tag_types): #This function performs Viterbi tagging of the test data
    file_content=open(file_name,'r')
    val=1
    rare_words={}
    file_write=open('hmmoutput.txt','w')
    for i in tag_types:
        rare_words[i]=0
    for line in file_content:
        line_words=line.split()
        if val<=2:
            val+=1
            continue
        Vit={0:{'start':1}}
        back_ptr={0:{'start':None}}
        ind=0
        for word in line_words:
            try:
                curr_tags=emis[word]
            except:
                curr_tags=rare_words
            path_calc(curr_tags,Vit,ind,trans,back_ptr)
            ind+=1
        path_calc({'END':1},Vit,ind,trans,back_ptr)
        fin_tag='END'
        final_tagged_line=['' for j in range(len(line_words))]
        for word_ind in range(ind+1,0,-1):
            if fin_tag!='END':
                final_tagged_line[word_ind-1]=fin_tag
            fin_tag=back_ptr[word_ind][fin_tag]
        w_ind=-1
        break
        for w_ind in range(len(line_words)-1):
            file_write.write(line_words[w_ind]+'/'+final_tagged_line[w_ind]+' ') #Writing the final tagged sentence to an output file
        file_write.write(line_words[w_ind+1]+'/'+final_tagged_line[w_ind+1]+'\n')
tag_file(sys.argv[1])
