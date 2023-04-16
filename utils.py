from nltk.corpus import stopwords
from stemming.porter2 import stem
import networkx
import nltk
import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objects as go
import streamlit as st
import io

nltk.download('stopwords')

class Recommender:

    def __init__(self) -> None:
        pass

    def get_book_metadata(self,purchasedAsin, amazonBooks):
        """
        Get metadata associated with a given ApurchasedAsin        """
        metadata = {}
        metadata['ASIN'] = purchasedAsin
        metadata['Title'] = amazonBooks[purchasedAsin]['Title']
        metadata['SalesRank'] = amazonBooks[purchasedAsin]['SalesRank']
        metadata['TotalReviews'] = amazonBooks[purchasedAsin]['TotalReviews']
        metadata['AvgRating'] = amazonBooks[purchasedAsin]['AvgRating']
        metadata['DegreeCentrality'] = amazonBooks[purchasedAsin]['DegreeCentrality']
        metadata['ClusteringCoeff'] = amazonBooks[purchasedAsin]['ClusteringCoeff']
        return metadata


    def get_ego_network(self,purchasedAsin, copurchaseGraph):
        """
        Get the depth-1 ego network of a given ASIN from copurchaseGraph
        """
        n = purchasedAsin
        ego = networkx.ego_graph(copurchaseGraph, n, radius=1)
        purchasedAsinEgoGraph = networkx.Graph(ego)
        pos = networkx.layout.spring_layout(purchasedAsinEgoGraph)
        M = purchasedAsinEgoGraph.number_of_edges()
        nodes = networkx.draw_networkx_nodes(purchasedAsinEgoGraph, pos, node_size=50, node_color='blue')
        edges = networkx.draw_networkx_edges(purchasedAsinEgoGraph, pos, node_size=50, edge_cmap=plt.cm.Blues, width=2, alpha=0.1)
        return purchasedAsinEgoGraph
        

# Create a scatter plot
        #fig = go.Figure(go.Scatter(x=[1, 2, 3, 4], y=[10, 11, 12, 13], mode='markers'))

    def plot_ego_network(self):
        """
        Plot the ego network using matplotlib   
        """
        threshold = 0.5
        purchasedAsinEgoTrimGraph = networkx.Graph()
        for f,t,e in purchasedAsinEgoTrimGraph.edges(data=True):
            if e['weight'] >= threshold:
                purchasedAsinEgoTrimGraph.add_edge(f,t, weight=e['weight'])
        pos = networkx.layout.spring_layout(purchasedAsinEgoTrimGraph)
        M = purchasedAsinEgoTrimGraph.number_of_edges()
        nodes = networkx.draw_networkx_nodes(purchasedAsinEgoTrimGraph, pos, node_size=50, node_color='blue')
        edges = networkx.draw_networkx_edges(purchasedAsinEgoTrimGraph, pos, node_size=50, edge_cmap=plt.cm.Blues, width=2, alpha=0.1)
        ax = plt.gca()
        ax.set_axis_off()
        plt.title('Degree-1 Ego Network')
        #plt.figure(0)
        plt.show()
        return purchasedAsinEgoTrimGraph


    def get_nodes(self,purchasedAsinEgoTrimGraph,purchasedAsin,amazonBooks):
        # Get the list of nodes connected to the purchasedAsin
        purchasedAsinNeighbours = purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)
        #return purchasedAsinNeighbours
        AsMeta = []
        for asin in purchasedAsinNeighbours:
            ASIN = asin
            Title = amazonBooks[asin]['Title']
            SalesRank = amazonBooks[asin]['SalesRank']
            TotalReviews = amazonBooks[asin]['TotalReviews']
            AvgRating = amazonBooks[asin]['AvgRating']
            DegreeCentrality = amazonBooks[asin]['DegreeCentrality']
            ClusteringCoeff = amazonBooks[asin]['ClusteringCoeff']
            AsMeta.append((ASIN, Title, SalesRank, TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff))
        return AsMeta
    
    def get_metadata(self,purchasedAsinNeighbours,amazonBooks):
        AsMeta = []
        for asin in purchasedAsinNeighbours:
            ASIN = asin
            Title = amazonBooks[asin]['Title']
            SalesRank = amazonBooks[asin]['SalesRank']
            TotalReviews = amazonBooks[asin]['TotalReviews']
            AvgRating = amazonBooks[asin]['AvgRating']
            DegreeCentrality = amazonBooks[asin]['DegreeCentrality']
            ClusteringCoeff = amazonBooks[asin]['ClusteringCoeff']
            AsMeta.append((ASIN, Title, SalesRank, TotalReviews, AvgRating, DegreeCentrality, ClusteringCoeff))
        return AsMeta
    
    def get_recommended(self,AsMeta):
    # Sorting the top five nodes in purchasedAsinNeighbour by Average Rating then by TotalReviews
        T5_byAvgRating_then_byTotalReviews = sorted(AsMeta, key=lambda x: (x[4], x[3]), reverse=True)[:5]
        return T5_byAvgRating_then_byTotalReviews

    def print_recommend(self,T5_byAvgRating_then_byTotalReviews):
    # Print Top 5 Recommendations
        print('\nTop 5 Recommendations by AvgRating then by TotalReviews for Users Purchased the book:')
        print('\n------------------------------------------------------------------------------------')
        print('ASIN\t', 'Title\t', 'SalesRank\t', 'TotalReviews\t', 'AvgRating\t', 'DegreeCentrality\t', 'ClusteringCoeff')
        for asin in T5_byAvgRating_then_byTotalReviews:
            print(asin)