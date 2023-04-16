from utils import Recommender
import string
import re
from nltk.corpus import stopwords
from stemming.porter2 import stem
import networkx
import nltk
nltk.download('stopwords')
import networkx
from operator import itemgetter
import matplotlib.pyplot as plt
import matplotlib as mpl
import streamlit as st 
import pandas as pd
from PIL import Image
import io

def main():
    st.title("Graph based Recommendation System")
    html_temp = """
    <div style="background-color:blue;padding:10px">
    <h2 style="color:white;text-align:center;">amazon-books-graph-based-recommendation</h2>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)
    purchasedAsin = st.text_input("purchasedAsin")#0842328327
    if st.button("recommend"):
        recommender=Recommender()
        amazonBooks = {}
        fhr = open('amazon-books.txt', 'r', encoding='utf-8', errors='ignore')
        fhr.readline()
        for line in fhr:
                cell = line.split('\t')
                MetaData = {}
                MetaData['Id'] = cell[0].strip()
                ASIN = cell[1].strip()
                MetaData['Title'] = cell[2].strip()
                MetaData['Categories'] = cell[3].strip()
                MetaData['Group'] = cell[4].strip()
                MetaData['Copurchased'] = cell[5].strip()
                MetaData['SalesRank'] = int(cell[6].strip())
                MetaData['TotalReviews'] = int(cell[7].strip())
                MetaData['AvgRating'] = float(cell[8].strip())
                MetaData['DegreeCentrality'] = int(cell[9].strip())
                MetaData['ClusteringCoeff'] = float(cell[10].strip())
                amazonBooks[ASIN] = MetaData
        fhr.close()
        fhr = open("amazon-books-copurchase.edgelist", "rb")
        copurchaseGraph = networkx.read_weighted_edgelist(fhr)
        fhr.close()
        metadata=recommender.get_book_metadata(purchasedAsin, amazonBooks)
        purchasedAsinEgoTrimGraph=recommender.get_ego_network(purchasedAsin, copurchaseGraph)
        AsMeta=recommender.get_nodes(purchasedAsinEgoTrimGraph,purchasedAsin,amazonBooks)
        T5_byAvgRating_then_byTotalReviews=recommender.get_recommended(AsMeta)
        l=[]
        st.text('\nTop 5 Recommendations by AvgRating then by TotalReviews for Users Purchased the book:')
        columns_names=['ASIN','Title','SalesRank','TotalReviews','AvgRating','DegreeCentrality','ClusteringCoeff']
        for asin in T5_byAvgRating_then_byTotalReviews:
            l.append(asin)
        df=pd.DataFrame(l,columns=columns_names)
        st.table(df)

if __name__ == '__main__':
    main()