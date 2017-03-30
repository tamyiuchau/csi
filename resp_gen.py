from google.cloud import language
import re
client = language.Client()
from random import choice

def analyze(text):
    doc=client.document_from_text(text)
    anno=doc.annotate_text()
    return anno
    


def tkprint(an):
    for token in an.tokens:
        print(token.part_of_speech,token.text_content,token.edge_index,token.edge_label,token.lemma)

def conflit():
    if neg(a) in obj.describtion(b):
        question((a,b),different)
def obj():
    if not know(a):
        if a is human:
            question(a,human)
        elif b is place:
            question(b,love)
        
def pron_ref(sub):
    if sub is 1:
        return I
    elif sub is 2:
        if sub == we:
            sub
    trancking_obj[type(sub)]
    
#obj={"PERSON":[],"LOCATION":[],"EVENT":[],"WORK_OF_ART":[],"CONSUMER_GOOD":[],"OTHER":[]}
state={"question","learn"}
obj=[]
data_feel={}
data_good={}
data_bad={}
p_ent={}
self_ref_f=False
subject=""
def resolve(tks):
    c={}
    d={}
    for i in tks:
        if i.edge_label not in c:
            c[i.edge_label]=[i]
        else:
            c[i.edge_label].append(i)
    for i in tks:
        prev=""
        if "NEG" in c:
            prev=" not "
        if i.part_of_speech not in d:
            d[i.part_of_speech]=[prev+i.text_content]
        else:
            d[i.part_of_speech].append(prev+i.text_content)
    if "NSUBJ" in c:
        for i in c["NSUBJ"]:
            if i.part_of_speech=="PRON":
                name=i.text_content.lower()
                if name == "you":
                    global self_ref_f
                    self_ref_f=True
            else:
                global subject
                subject=i.text_content
            
    return c,d
    
cum_senti=0.0

def query(text):
    #print(data_feel)
    #print(data_good)
    for i in ["morning","afternoon"]:
        if "good "+i in text.lower():
            return "Good morning."+"I am Alice. Can you tell me about someone you know?"
    for i in ["goodnight","good night"]:
        if i in text.lower():
            return "Good night. Wish you a good sleep."
    for i in text.split("."):
        for j in i.split("?"):
            reply=""
            global self_ref_flag
            self_ref_flag=False
            anno=analyze(j)
            tks=anno.tokens
            senti=anno.sentiment.score*anno.sentiment.magnitude
            global cum_senti
            
            cum_senti+=senti
            global p_ent
            p_ent={i.entity_type:i for i in anno.entities if i.name.lower() not in {'i','we','you','they','he','she','it'}}
            
            td,pos=resolve(tks)
            if "X" in pos:
                return pos["X"][0]+" "+"I am Alice. Can you tell me about someone you know?"
            if senti<0:
                if subject in data_good:
                    reply="But "+subject+" is "+choice(data_good[subject]+"!")
                if "ADJ" in pos:
                    for i in pos["ADJ"]:
                        if subject not in data_bad:
                            data_bad[subject]=i
                        else:
                            data_bad[subject].append(i)
            elif senti>0.05:
                if "ADJ" in pos:
                    for i in pos["ADJ"]:
                        if subject not in data_good:
                            data_good[subject]=[i]
                        else:
                            data_good[subject].append(i)
            if not reply:
                if cum_senti<0:
                    reply="You don't seem happy. What's up?"
            if self_ref_flag:
                return "Recursion is too difficult and I still don't understand my self. I am interested in you, please don't refer to me."
            else:
                return reply
    
