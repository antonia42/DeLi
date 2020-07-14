import sys

import networkx as nx
#from simhash import Simhash, SimhashIndex
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# if there is a problem with gensim and Word2Vec, check the python version
# to be 2.7
# print('Hello from {}'.format(sys.version))


# TF-IDF helper function
def reveal_similar_links(G, cids, contents, threshold=0.5):
    """
    Function to calculate the TF-IDF vectors for all tweet/contents and then it
    calculates the cosine similarity for all pairs. It returns the graph with
    edges between the similar tweet-nodes, when the cosine similarity for a
    pair of tweet-nodes is above a threshold.

    Args:
        G (networkx.Graph()): The initialized instance of the networkx Graph()
            class.

        cids (list): The list with the tweet ids from the tweet-nodes of the
            graph.

        contents (list): The list with the preprocessed content from the tweet-
            nodes. Indexing is the same as in the 'cids' list.

        threshold (float): The cosine similarity threshold. If the similarity
            of a pair exceed this threshold, an edge is added in the graph
            between these nodes.

    Returns:
        The enriched graph instance (networkx.Graph()), after revealing the
        hidden edges between similar tweet-nodes.

    """
    try:
        tfidf = TfidfVectorizer(norm='l2', max_features=1000)
        tf_idf_matrix = tfidf.fit_transform(contents)
        tf_idf_matrix.todense()
        pairwise_similarity = tf_idf_matrix * tf_idf_matrix.T
        cos_matrix = (pairwise_similarity).A

        tsize = len(contents)
        for i in range(0, tsize):
            for j in range(i+1, tsize):
                # similarity score is in [-1, 1]
                sim_score = cos_matrix[i][j]
                if sim_score > threshold:
                    # reveal hidden edge (between similar tweet-nodes)
                    G.add_edge(cids[i], cids[j], edgetype='similarTo')

    except:
        pass

    return G


# Add edges between all pairs of similar content nodes based on TFIDF
def reveal_hidden_links_tfidf(G, content_dict, threshold):
    """
    Function to reveal hidden similarity edges between tweet-nodes based only
    on TF-IDF vectors and a cosine similarity threshold.

    Args:
        G (networkx.Graph()): The initialized instance of the networkx Graph()
            class.

        content_dict (dict): The dict with the tweet ids from the tweet-nodes
            of the graph and the corresponding preprocessed tweet/content text.

        threshold (float): The cosine similarity threshold. If the similarity
            of a pair exceed this threshold, an edge is added in the graph
            between these nodes.

    Returns:
        The returning element of the function 'reveal_similar_links', a.k.a. an
        enriched graph instance, after revealing the hidden edges between
        similar tweet-nodes.

    """
    cids = content_dict.keys()
    contents = content_dict.values()

    return reveal_similar_links(G, cids, contents, threshold)


# Creates w-shingles for SimHash
def get_shingles(sentence, n):
    """
    Function to reveal hidden similarity edges between tweet-nodes based on
    SimHash, an LSH approximation on TF-IDF vectors and a cosine similarity
    threshold.

    Args:
        sentence (str): The sentence (preprocessed text from a tweet-node),
            from which the shingles will be created.

        n (int): The size of the shingle. In this case, the size is always set
            to be three, and it means that all possible tuples with three
            consecutive words will be created.

    Returns:
        A list with all triples made by consecutive words in a sentence.

    """
    s = sentence.lower()
    return [s[i:i + n] for i in range(max(len(s) - n + 1, 1))]


# Add edges between all pairs of similar content nodes based on SimHash
def reveal_hidden_links_simhash(G, content_dict, threshold):
    """
    Function to reveal hidden similarity edges between tweet-nodes based on
    SimHash, an LSH approximation on TF-IDF vectors and a cosine similarity
    threshold.

    Args:
        G (networkx.Graph()): The initialized instance of the networkx Graph()
            class.

        content_dict (dict): The dict with the tweet ids from the tweet-nodes
            of the graph and the corresponding preprocessed tweet/content text.

        threshold (float): The cosine similarity threshold. If the similarity
            of a pair exceed this threshold, an edge is added in the graph
            between these nodes.

    Returns:
        The returning element of the function 'reveal_similar_links', a.k.a. an
        enriched graph instance, after revealing the hidden edges between
        similar tweet-nodes.

    """
    objs = []
    for cid, content in content_dict.items():
        objs.append((cid, Simhash(get_shingles(content, 3), f=1)))

    index = SimhashIndex(objs, f=1, k=2)

    for key in index.bucket:
        bucket_item = index.bucket[key]

        contents = []
        cids = []
        for item in bucket_item:
            newid = str(item.split(',')[-1])

            contents.append(content_dict[newid])
            cids.append(newid)

            G = reveal_similar_links(G, cids, contents, threshold)

    return G


# Add edges between all pairs of similar content nodes based on word2vec
def reveal_hidden_links_w2v(G, content_dict, threshold, model, k=3):
    """
    Function to reveal hidden similarity edges between tweet-nodes based on
    Word2Vec enriched TF-IDF vectors and a cosine similarity threshold. More
    specifically, for each word in a tweet, we add the 'k' most similar words
    according to the pre-trained Word2Vec model.
    Note: If you need to speed up the code during experimentation, it is better
        to calculate the Word2Vec enriched text and cache it.

    Args:
        G (networkx.Graph()): The initialized instance of the networkx Graph()
            class.

        content_dict (dict): The dict with the tweet ids from the tweet-nodes
            of the graph and the corresponding preprocessed tweet/content text.

        threshold (float): The cosine similarity threshold. If the similarity
            of a pair exceed this threshold, an edge is added in the graph
            between these nodes.

        model (gensim.models.KeyedVectors()): The Google's pre-trained
            Word2Vec model.

        k (int): The number of similar words to add.

    Returns:
        The returning element of the function 'reveal_similar_links', a.k.a. an
        enriched graph instance, after revealing the hidden edges between
        similar tweet-nodes.

    """
    contents = content_dict.values()
    cids = content_dict.keys()

    enriched_contents = []
    for c in contents:
        words = c.split(' ')
        enriched_list = []
        for w in words:
            try:
                w2v_sim_list = model.most_similar(w, topn=k)
                sim_words = [str(t[0]) for t in w2v_sim_list]
                enriched_list.append(' '.join(sim_words) + ' ' + w)
            except:
                enriched_list.append(w)
                pass

        if len(enriched_list) > 0:
            enriched_contents.append(' '.join(enriched_list))

    return reveal_similar_links(G, cids, enriched_contents, threshold)
