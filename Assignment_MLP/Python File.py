def csv(file):
    dataset = [] 
    data = open(file,'r').readlines() 
    for i in data: 
        row=i.split(',') 
        t=list(map(float,row[:-1])) 
        if row[-1]=='M\n': 
            t.append(1) 
        else:
            t.append(0) 
        dataset.append(t) 
    return dataset[:len(dataset)-100] 
file = 'mydata.csv' 
dataset = csv(file)
from random import randrange 
def split(dataset, n): 
    t = list() 
    dataset_copy = list(dataset) 
    fold_size = len(dataset) // n 
    for i in range(n): 
        fold = list() 
        while len(fold) < fold_size: 
            index = randrange(0, len(dataset_copy)) 
            fold.append(dataset_copy.pop(index))    
        t.append(fold) 
    return t 
def findmetrics(act, pred):
    tn,tp,fn,fp,= 0,0,0,0 
    for i in range(len(act)): 
        if act[i] == 1 and pred[i]==1: 
            tp+=1
        elif act[i]==1 and pred[i]==0:
            fn+=1
        elif act[i]==0 and pred[i]==1:
            fp+=1
        else: 
            tn+=1
    return [(tn+tp)/(tn+tp+fn+fp),str(tp)+'  '+str(fn)+'\n'+str(fp)+'  '+str(tn),tp/(tp+fp),tp/(tp+fn)]
def algorithm(dataset, algo, n, *args):
    folds =split(dataset, n) 
    scores = list() 
    for i in range(len(folds)): 
        train_set = list(folds) 
        train_set.remove(folds[i]) 
        train_set = sum(train_set, []) 
        test_set = list() 
        actual=list()
        for row in folds[i]:
            row_c = list(row) 
            actual.append(row_c[-1]) 
            row_c[-1] = None 
            test_set.append(row_c) 
        
        predicted = algo(train_set, test_set, *args) 
        metrics = findmetrics(actual, predicted) 
        print(' Fold',i+1,':')
        print(' the Hyperparameters')
        print('Completed Cumulative Epochs : ',4000*(i+1))
        print('Learning rate : ',0.02,'\n')
        print('Metrics -')
        print('Accuracy : ',metrics[0]) 
        print('Confusion Matrix:\n'+metrics[1])
        print('Precision : ',metrics[2])
        print('Recall : ',metrics[3],'\n')
        scores.append(metrics[0])
    return scores
def predict(row, weights):
    activation = weights[0]
    for i in range(len(row)-1):
        activation += weights[i + 1] * row[i] 
    return 1.0 if activation>= 0.0 else 0.0 
def train_it(train, lerate, noepoch):
    weights = [0.0 for i in range(len(train[0]))] 
    for epoch in range(noepoch): 
        sum_error = 0.0  
        for row in train: 
            prediction = predict(row, weights) 
            error = row[-1] - prediction 
            sum_error += error**2 
            weights[0] = weights[0] + lerate * error
            for i in range(len(row)-1): 
                weights[i + 1] = weights[i + 1] + lerate * error * row[i] 
        error_data.append((epoch, sum_error)) 
    return weights
import seaborn as sns 
import matplotlib.pyplot as plt
%matplotlib inline 
def plot(error_data,a): 
    x=[error_data[i+4000*a][0] for i in range(0,4000)] 
    y=[error_data[i+4000*a][1] for i in range(0,4000)] 
    ax=sns.lineplot(x,y,color="coral") 
    
    ax.set_title('Fold '+str(a+1)+' loss function/Squared sum plot') 
    ax.set(xlabel='Epochs',ylabel='Squared Error') 
    plt.show() 

def perceptron(train, test, lerate, noepoch):
    predictions = list() 
    weights = train_it(train, lerate, noepoch) 
    stor_weights.append(weights)
    for row in test: 
        prediction = predict(row, weights) 
        predictions.append(prediction) 
    return predictions
nofolds = 3 
lerate = 0.02 
noepoch = 4000 

error_data = list() 
stor_weights = list() 
print('Training phase ')
scores = algorithm(dataset, perceptron, nofolds, lerate, noepoch)

print('Results obtained in every run:\n')


for i in range(3):
    plot(error_data,i)
print(' All Accuracy Scores: ',scores)
print(' Average Accuracy: ',sum(scores)/len(scores))
print('\n Initial start weights: ')
print(stor_weights[0])
w_test = stor_weights[-1]
print('\n Updated Final Weights: ')
print(w_test,'\n')

print("test results for an new dataset ")
act,pred=[],[]
for i in range(100):
    act.append(dataset[len(dataset)-i-1][30])
    pred.append(predict(dataset[len(dataset)-i-1], w_test))

metrics=findmetrics(act,pred)
print('\n Accuracy: ',metrics[0])
print('Confusion Matrix:\n'+metrics[1])
print(' Recall: ',metrics[3])
print(' Precision: ',metrics[2])



