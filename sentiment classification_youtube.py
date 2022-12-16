from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd   
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from csv import writer
from matplotlib import pyplot as plt
import numpy as np
def scrapper():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.youtube.com/watch?v=gOf2SQVMUL0")
    driver.execute_script('window.scrollTo(1, 500);')
    #now wait let load the comments
    time.sleep(20)
    #scroll window from x-cordinaate 0 to y-cordinate-3000
    driver.execute_script('window.scrollTo(1, 3000);')
    # comment_div=driver.find_element(By.XPATH,value='//*[@id="contents"]')
    #this is a list
    comments=driver.find_elements(By.XPATH,'//*[@id="content-text"]')
    #create list of comments
    comments_list = []
    #create list to store score of comments
    comment_score = []
    print("Comments : ")
    for comment in comments:
        print("\n",comment.text)
        comments_list.append(comment.text)
         #calculate score of that comment
        comment_score.append(analyze(comment.text))
        #create a dictionary with all the values
    data = {'Comment':comments_list,'Sentiment':comment_score}
    df = pd.DataFrame(data, columns=['Comment','Sentiment']) 
    #viết vào file txt
    data1=comments_list
    with open('comment.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(data1))
        f.close()
    totalSentiment(df)
    
def analyze(comment):

    #analyzing the data
    score = SentimentIntensityAnalyzer().polarity_scores(comment)
    
    if score['compound'] >= 0.05 :
        sentiment = "Positive"
    elif score['compound'] <= - 0.05 :
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment
def totalSentiment(df):
    #calculate the percentage of sentiments
    sentiment_list = df.loc[:,'Sentiment']
    count_Positive = 0
    count_Neutral = 0
    count_Negative = 0
    count = 0
    for sentiment in sentiment_list:
        if(sentiment == 'Positive'):
            count_Positive +=1
        elif(sentiment == 'Negative'):
            count_Negative +=1
        else:
            count_Neutral +=1
            count+=1
    
    if(count != 0):
        a= (count_Positive/count)*100
        b= (count_Negative/count)*100
        c= (count_Neutral/count)*100
        fig = plt.figure()
        ax = fig.add_axes([0,0,1,1])
        ax.axis('equal')
        langs = ['Tích cực','Tiêu cực','Trung lập']
        comment = [a,b,c]
        ax.pie(comment, labels = langs,autopct='%1.2f%%')
        plt.show()
    else:
        print("Issue with scrapping. Please try again!")
scrapper()

