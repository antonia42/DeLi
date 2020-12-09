## Detection and Delineation of Events and Sub-Events in Social Networks (IEEE ICDE 2018)
#### Authors: [Antonia Saravanou](http://cgi.di.uoa.gr/~antoniasar/), [Ioannis Katakis](http://www.katakis.eu/), [George Valkanas](http://cgi.di.uoa.gr/~gvalk/), [Dimitrios Gunopulos](http://kddlab.di.uoa.gr/dg.html)
#### [Link to the paper](http://cgi.di.uoa.gr/~antoniasar/papers/Saravanou_Delineating_ICDE2018.pdf)
#### [Link to the poster](http://cgi.di.uoa.gr/~antoniasar/papers/Saravanou_Delineating_ICDE2018_poster.pdf)

### Introduction
Event detection techniques in social networks have been proposed as a way to sense and understand what is happening in the offline and online world. A fundamental problem is that event detection techniques capture and treat events as singletons, as if they are all disconnected and irrelevant to each other. Clearly, this is not the case in real life, where we abstract a series of highlights or turning points - a sub-event - into groups, which collectively constitute the event. Sub-event delineation offers a better understanding through a more detailed breakdown of the main event. For example, a football match is better described as a sequence of highlights, e.g., goals, penalties, red and yellow cards, that occur during the 90 minutes of the game. 


**DeLi** (**De**tecting and De**Li**neating Events) is an efficient algorithm for event detection in social media with automated timeline construction. DeLi addresses the event delineation problem at its core: it identifies the main event and simultaneously captures highlights (subevents) that describe it over time, without any prior knowledge of the main event. The technique is unsupervised and is able to distinguish between distinct main events that take place concurrently. It achieves that by modeling the social network as a dynamic, heterogeneous graph with both user nodes (with links representing interactions) and content nodes (with links representing similarity. Such a representation contains information about the structure and the content of the network, thereby bringing together the two method categories. Within this graph, (sub-)events are large connected components that DeLi uses in order to provide effective event detection and
delineation.


The contributions of this work can be summarized as follows:
1. **Network Representation**: We introduce a novel representation of a network as a dynamic heterogeneous graph, the Content Network. 
2. **Revealing Hidden Links**: We provide an algorithm that identifies hidden links in Content Networks by connecting similar content nodes utilizing neural word embeddings.
3. **Event Detection**: We present an algorithm for detecting events by tracking large connected components of Content Networks over time. Our results demonstrate, that we are able to effectively identify events compared to widely used event detection techniques.
4. **Sub-Event Detection (or Delineation)**: We present an algorithm that builts on top of our event detection algorithm and is detecting sub-events by tracking dense subgraphs in the large connected components of Content Networks over time and summarizing them using the text similarity and the graph structure. Our results demonstrate, that we are able to effectively identify sub-events compared to the state-of-the-art.


If you make use of this code, the DeLi algorithm, or the datasets in your work, please cite the following paper:
```
@inproceedings{saravanou2018detection,
  title={Detection and Delineation of Events and Sub-Events in Social Networks},
  author={Saravanou, Antonia and Katakis, Ioannis and Valkanas, George and Gunopulos, Dimitrios},
  booktitle={2018 IEEE 34th International Conference on Data Engineering (ICDE)},
  pages={1348--1351},
  year={2018},
  organization={IEEE}
}
```


### Dataset format

The network should be stored under the `data/` folder, one file per time window. The filename should be `<time window id>.tsv`, where `<time window id>` starts from `0` to `number of time windows - 1`.

The file should be in the following format:
- One line per tweet.
- Each line should have the following *tab*-separated information: 
*tweet_id, user_id, tweet_text, timestamp, is_reply_to_tweet_id, is_reply_to_user_id*.

For example, the first few lines of a dataset can be:
```
tweet_id    user_id tweet_text  timestamp   is_reply_to_tweet_id    is_reply_to_user_id
t0	u0	the brown fox jumped over the lazy dog	1594426186		
t1	u0	brown fox cat dog	1594426189	t0	u0
t2	u1	icecream summer vacations	1594426199		
t3	u2	sea beach iced coffee	1594426206	t2	u1
```


### References 
Saravanou, A., Katakis, I., Valkanas, G. and Gunopulos, D., 2018, April. Detection and Delineation of Events and Sub-Events in Social Networks. In 2018 IEEE 34th International Conference on Data Engineering (ICDE) (pp. 1348-1351). IEEE. 

If you make use of this code, the DeLi algorithm, or the dataset in your work, please cite the following paper:
```
@inproceedings{saravanou2018detection,
  title={Detection and Delineation of Events and Sub-Events in Social Networks},
  author={Saravanou, Antonia and Katakis, Ioannis and Valkanas, George and Gunopulos, Dimitrios},
  booktitle={2018 IEEE 34th International Conference on Data Engineering (ICDE)},
  pages={1348--1351},
  year={2018},
  organization={IEEE}
}
```
