import codecs
import sys

import networkx as nx

from utilities import preprocess_text

reload(sys)
sys.setdefaultencoding('utf-8')


def twitter_graph(filename):
    """
    Function to create the heterogeneous Twitter graph. The resulting graph,
    contains user-nodes and tweet-nodes from the stream of Twitter written in
    the filename.

    Args:
        filename (str): The full filename (+ filepath) to a stream of tweets
            from a time window.

    Returns:
        A tuple that contains an instance of the networkx Graph() class and a
        dictionary with the tweet ids as keys and the preprocessed tweet
        content as values.

    """
    G = nx.Graph()
    with codecs.open(filename, 'rb', encoding='utf-8', errors='ignore') as f:
        content_dict = {}
        for line in f:
            line = line.rstrip('\n')
            line_v = line.split('\t')
            cid = str(line_v[0])
            pid = str(line_v[1])
            content = str(line_v[2])
            epoch_timestamp = int(line_v[3])
            reply_to_cid = str(line_v[4])
            reply_to_pid = str(line_v[5])

            # preprocess tweet
            preprocessed_content = preprocess_text(content)

            if len(preprocessed_content) > 0:
                # add user node
                G.add_node(pid, size=1, nodetype='publisher')

                # add tweet node
                G.add_node(cid, content=content, pre=preprocessed_content,
                           timestamp=epoch_timestamp, size=1,
                           nodetype='content')

                content_dict[cid] = preprocessed_content

                # add user-tweets-text edges
                G.add_edge(cid, pid, edgetype='publish')

                # add user1-repliesTo-user2 edge between the two publisher
                # nodes; if the user to whom there is a reply exists in the
                # snapshot graph
                if reply_to_pid:
                    if reply_to_pid in G:
                        G.add_edge(pid, reply_to_pid, edgetype='replyTo')

    f.close()

    return (G, content_dict)
