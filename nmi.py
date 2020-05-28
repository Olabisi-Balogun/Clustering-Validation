import itertools
import math
import sys
#function to compute the jaccard similarity
def jaccard(label1, label2):
    n = len(label1)
    n11 = n10 = n01 = 0
    
    for i, j in itertools.combinations(range(n),2):
        comembership1 = label1[i] == label1[j]
        comembership2 = label2[i] == label2[j]
        
        if comembership1 and comembership2:
            n11+=1
        elif comembership1 and not comembership2:
            n10+=1
        elif not comembership1 and comembership2:
            n01+=1
    
    return float(n11)/ (n11+n10+n01)
#Steps to compute NMI

def get_cluster_dict(label1, label2):
    #label1.sort()
    #label2.sort()
    n_ground = len(set(label1))
    n_pred = len(set(label2))
    cluster_dict = {}
    merged_label = tuple(zip(label2, label1))

   
    for i in range(n_pred):
        count_label=0
        for j in range(n_ground):
            if (str(i),str(j)) in(merged_label):
                count = merged_label.count((str(i),str(j)))
                count_label +=count
        
        cluster_dict[str(i)] = count_label
            
                
                
    return cluster_dict
            
def get_ground_dict(label1, label2):
    #label1.sort()
    #label2.sort()
    n_ground = len(set(label1))
    n_pred = len(set(label2))
    ground_dict = {}
    merged_label = tuple(zip(label1, label2))
    
    for i in range(n_ground):
        count_label = 0
        for j in range(n_pred):
            if(str(i),str(j)) in merged_label:
                count = merged_label.count((str(i),str(j)))
                count_label+=count
        ground_dict[str(i)] = count_label
        
    return ground_dict
    

def cal_numerator(data, g_dict, c_dict):
    n = len(data)
    numerator1 = 0.0
    numerator2 = 0.0
    
    for key in g_dict:
        temp = (g_dict[key]/n)*math.log(float(g_dict[key]/n), 2)
        numerator1 = numerator1 + temp
    
    for key in c_dict:
        temp2 = (c_dict[key]/n)* math.log(float(c_dict[key]/n), 2)
        numerator2 = numerator2 + temp2
        
    return -(numerator1), -(numerator2)

def cal_denominator(data, label1,label2,g_dict, c_dict):
    #label1.sort()
    #label2.sort()
    n = len(data)
    denominator = 0.0
    merged_label = tuple(zip(label2, label1))
    sum_d = 0.0
    
    for i in range(len(c_dict)):
        sum_d = 0.0
        for j in range(len(g_dict)):
            if (str(i), str(j)) in merged_label:
                count = merged_label.count((str(i),str(j)))
                temp_d = (count/ n)* math.log((count*n/(c_dict[str(i)]*g_dict[str(j)])), 2)
                sum_d = sum_d + temp_d
        denominator = sum_d + denominator
        
    return denominator

def cal_nmi(denom, numerator):
    
    num1, num2 = numerator
    
    nmi = denom/math.sqrt(num1*num2)
    
    return format(nmi,'.3f')

def print_ans(nmi, jac):
    return nmi, format(jac,'.3f')
    
def calculate_similarity():
    
    file = open("input_jaccard.txt","r")
    
    data = []
    ground_truth = []
    predicted = []
    
    for line in file:
        line=list(line.strip("\n").strip(" ").split(" "))
        data.append(line)
        #data.append(list(line.strip("\n").split(" ")))
        
    for i in range(len(data)):
        ground_truth.append(data[i][0])
        predicted.append(data[i][1])
        
    dict_cluster = get_cluster_dict(ground_truth, predicted)
    dict_ground = get_ground_dict(ground_truth, predicted)
    get_numerator = cal_numerator(data, dict_ground, dict_cluster)
    get_denominator = cal_denominator(data,ground_truth, predicted,dict_ground,dict_cluster)
    get_nmi = cal_nmi(get_denominator, get_numerator)
    jaccard_sim = jaccard(ground_truth, predicted)
    print_answer = print_ans(get_nmi, jaccard_sim)
    
    return print_answer

answer1, answer2 = calculate_similarity()
print(answer1, answer2)
