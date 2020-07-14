import os

import gensim as gs
import networkx as nx
from sklearn.metrics import precision_recall_fscore_support

from create_graph import twitter_graph
from detect_events import event_detection_delineation
from prune_noisy import prune_noisy_CCs
from reveal_links import (reveal_hidden_links_simhash,
                          reveal_hidden_links_tfidf, reveal_hidden_links_w2v)
from utilities import ground_truth


def run_main(filename, G_cache, w2v_model, k, sim_thres, theta=10, avg=0,
             std=0, reveal_method='tfidf', ):
    """
    Function to run all the steps to detect events for each file (time window).

    Args:
        filename (str): The full filename (+ filepath) to a stream of tweets
            from a time window.

        G_cache (networkx.Graph()): The connected components that were cached
            as event candidates from the previous time window.

        w2v_model (gensim.models.KeyedVectors()): The Google's pre-trained
            Word2Vec model.

        k (int): The number of similar words to add.

        sim_thres (float): The cosine similarity threshold. If the similarity
            of a pair exceed this threshold, an edge is added in the graph
            between these nodes.

        theta (float): The number of similar words to add. Default value: 10.

        avg (float): The average size of the connected components from the
            previous time window. Default value: 0.

        std (float): The standard deviation of the sizes of the connected
            components from the previous time window. Default value: 0.

        reveal_method (str): The method to reveal the hidden text similarity
            edges. Default value: tfidf. Other options: 'simhash' and 'w2v'.

    Returns:
        A tuple that contains:
            - (float) the average size of the CCs from the current time window.
            - (float) the standard deviation of the size of the CCs from the
                current time window.
            - (integer) the event flag on the number of events that were detected
                in the current time window.
            - (networkx.Graph()) the updated graph with the connected
                components that were cache in the current time window.
            - (list) the list of subevents for the surrent time window.

    """
    # Step 1: Create Snapshot Graph
    (G, content_dict) = twitter_graph(filename)

    # Step 2: Reveal Hidden Links
    if reveal_method == 'simhash':
        G = reveal_hidden_links_simhash(G, content_dict, sim_thres)
    elif reveal_method == 'w2v':
        if w2v_model == '':
            print "Please, load Google's Word2Vec pre-trained model and rerun"
        G = reveal_hidden_links_w2v(G, content_dict, sim_thres, w2v_model, k)
    # In case nor simhash neither w2v methods were selected, run tfidf method
    else:
        G = reveal_hidden_links_tfidf(G, content_dict, sim_thres)

    # Step 3: Prune Noisy CCs
    (G, cc_lengths) = prune_noisy_CCs(G)

    # Step 4: Detect and delineate events
    result = event_detection_delineation(G, G_cache, theta, avg, std, cc_lengths)

    return result


def deli(datapath, w2v_model, k, sim_thres, theta, avg, std, reveal_method):
    """
    Function to run all the steps to detect events for each file (time window).

    Args:
        datapath (str): The full path to the folder containing all the .tsv
            files.

        w2v_model (gensim.models.KeyedVectors()): The Google's pre-trained
            Word2Vec model.

        k (int): The number of similar words to add.

        sim_thres (float): The cosine similarity threshold. If the similarity
            of a pair exceed this threshold, an edge is added in the graph
            between these nodes.

        theta (float): The number of similar words to add. Default value: 10.

        avg (float): The average size of the connected components from the
            previous time window. Default value: 0.

        std (float): The standard deviation of the sizes of the connected
            components from the previous time window. Default value: 0.

        reveal_method (str): The method to reveal the hidden text similarity
            edges. Default value: tfidf. Other options: 'simhash' and 'w2v'.

    Returns:
        A tuple, that contains:
            - A list of integers. DeLi's results in a list of integers, where each
                position is the time window id and '0' indicates no existence 
                of events and the number of the detected events otherwise.
            - A list of lists. Each element of the list is a list of the subevents 
                that correspond to the corresponding time window. 

    """
    event_list_per_tw = []
    subevents_list_per_tw = []
    G_cache = nx.Graph()
    number_files = len(os.listdir(datapath))
    for i in range(number_files-1):
        filename = datapath + str(i) + '.tsv'

        (avg, std, res, G_cache, subevents) = run_main(filename, G_cache, w2v_model, k,
                                                sim_thres, theta, avg, std,
                                                reveal_method)
        event_list_per_tw.append(res)
        subevents_list_per_tw.append(subevents)

    return (event_list_per_tw, subevents_list_per_tw)


if __name__ == "__main__":
    # the path to the directory with the Twitter data organized in .tsv files
    # per time window
    # the file format is the following:
    # each line has:
    #   - a tweet id,
    #   - a user id,
    #   - a tweet description,
    #   - a timestamp in epoch formatting,
    #   - a tweet id to which it replies (if the current tweet is a reply),
    #   - a user id to whom it replies (if the current tweet is a reply)
    datapath = '.././data/'

    # binary list with the ground truth, if the value of a cell is '1' it
    # indicates the existence of an event for the time window with id the index
    # of the cell. This was used for the Twitter dataset
    # gt_list = ground_truth()

    # available options: 'tfidf', 'simhash', 'w2v'
    reveal_method = 'tfidf'

    # initialization of the avg and std
    avg = 0
    std = 0

    # the number of similar words to be used to extend the text from the
    # word2vec vectors
    k = 3

    # the cosine similarity threshold
    sim_thres = 0.5

    # the event detection threshold
    theta = 17

    if reveal_method == 'w2v':
        modelpath = '../models/GoogleNews-vectors-negative300.bin.gz'
        # loading of the Google's pre-trained Word2Vec model
        w2v_model = gs.models.KeyedVectors.load_word2vec_format(modelpath,
                                                                binary=True)
    else:
        w2v_model = ''

    (events_binary, subevents) = deli(datapath, w2v_model, k, sim_thres, theta, avg, std,
                                    reveal_method)

    # TODO initiate a list with the ground truth in binary format. Each element of the 
    # list should be '1' if an event occured in that time window and '0' otherwise
    #print 'track in time, theta =', theta, ', performance =', \
    #    precision_recall_fscore_support(gt_list, events_binary, pos_label=1, average='binary')

    for tw, subevents in enumerate(subevents):
        print("For time window: " + str(tw))
        event_flag = events_binary[tw]
        if event_flag == 0:
            print("  There are no events detected !!!\n")
        else:
            print("  There are " + str(event_flag) + " events with the following subevents:")
            for s in subevents:
                print("    ", s, "\n")

