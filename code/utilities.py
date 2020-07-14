import re
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# this list of stopwords is a merge of multiple lists found in the web
stops = set(['[closed]', '[duplicate]', 'i', 'me', 'sometime', 'been',
             'mostly', 'don\'t', 'don', 'hasnt', 'couldn\'t', 'couldn', '\'t',
             't', 'don', 'your', 'without', 'via', 'these', 'appreciate',
             'would', 'n\'t', 'n', 'because', 'near', 'doesn\'t', 'doesn',
             'ten', 'yo', 'unlikely', 'afterwards', 'sure', 'thus', 'going',
             'meanwhile', 'viz', 'bill', 'am', 'yourselves', 'an', 'whose',
             'former', 'mill', 'as', 'contains', 'at', 'trying', 'looking',
             'eleven', 'you', 'detail', 'i\'ve', 'much', 'appropriate', 'be',
             'anybody', 'comes', 'least', 'consequently', 'example', 'how',
             'see', 'inward', 'same', 'dont', 'by', 'whom', 'indicate',
             'after', 'shouldn\'t', 'shouldn', 'you\'ve', '\'ve', 'we\'d',
             '\'d', 'dear', 'mine', 'wouldn\'t', 'wouldn', 'a', 'sixty',
             'contain', 'thanx', 'namely', 'i', 'possible', 'right', 'co',
             'the', 'fifth', 'thank', 'somewhat', 'under', 'yours', 'did',
             'novel', 'nine', 'de', 'sometimes', 'do', 'down', 'got', 'empty',
             'wish', 'later', 'besides', 'serious', 'others', 'tis', 'needs',
             'which', 'ignored', 't\'s', '\'s', 'eg', 'e.g.', 'need', 'its',
             'thereafter', 'often', 'onto', 'regarding', 'et', 'gone', 'never',
             'she', 'take', 'ex', 'aside', 'immediate', 'relatively',
             'therefore', 'aren\'t', 'aren', 'hardly', 'useful', 'little',
             'however', 'some', 'rather', 'downwards', 'for', 'back',
             'greetings', 'c\'s', 'getting', 'nowhere', 'perhaps', 'sorry',
             'provides', 'you\'re', '\'re', 'myse\"', 'just', 'forty', 'over',
             'we\'ll', 'six', 'thence', 'go', 'obviously', 'kept', 'better',
             'with', 'although', 'selves', 'there', 'well', 'fify', 'happens',
             'he', 'hi', 'tries', 'very', 'placed', 'therein', 'soon', 'thick',
             'thanks', 'tried', 'else', 'four', 'beside', 'usually', 'whereas',
             'ie', 'i.e.', 'per', 'if', 'there\'s', 'likely', 'went', 'in',
             'considering', 'made', 'nothing', 'anyhow', 'specify', 'is',
             'being', 'it', 'forth', 'somebody', 'weren\'t', 'weren', 'ever',
             'we\'ve', '\'ve', 'system', 'even', 'hello', 'whereby',
             'secondly', 'become', 'thats', 'other', 'hundred', 'indicated',
             'against', 'respectively', 'a\'s', 'isn\'t', 'isn', 'whereupon',
             'hadn\'t', 'hadn', 'eight', 'howbeit', 'known', 'theres', 'top',
             'indicates', 'too', 'have', 'hopefully', 'everything', 'can\'t',
             'together', 'knows', 'twenty', 'accordingly', 'side',
             'particularly', 'thoroughly', 'may', 'seemed', 'within', 'could',
             'off', 'awfully', 'able', 'ain\'t', 'ain', 'com', 'theirs', 'con',
             'presumably', 'almost', 'use', 'several', 'amoungst', 'upon',
             'while', 'liked', 'second', 'latterly', 'amongst', 'that', 'etc',
             'whether', 'find', 'than', 'me', 'quite', 'different', 'insofar',
             'regardless', 'all', 'always', 'new', 'took', 'already', 'below',
             'everyone', 'didn\'t', 'didn', 'follows', 'lest', 'shall', 'less',
             'seriously', 'my', 'fill', 'plus', 'becomes', 'nd', 'were',
             'we\'re', 'try', 'since', 'became', 'behind', 'no', 'twas',
             'cause', 'best', 'around', 'and', 'hither', 'of', 'oh', 'somehow',
             'saying', 'ok', 'says', 'on', 'allows', 'brief', 'certainly',
             'fifteen', 'or', 'whence', 'cry', 'exactly', 'any', 'despite',
             'followed', 'c\'mon', 'concerning', 'due', 'until', 'formerly',
             'gotten', 'about', 'what\'s', 'anywhere', 'somewhere', 'wherein',
             'haven\'t', 'haven', 'wasn\'t', 'wasn', 'where\'s', 'above',
             'fire', 'let', 'welcome', 'they', 'here\'s', 'using', 'qv',
             'containing', 'old', 'myself', 'want', 'herein', 'them', 'then',
             'each', 'something', 'specifying', 'himself', 'rd', 're',
             'thereby', 'twelve', 'except', 'must', 'sincere', 'sub',
             'nevertheless', 'hasn\'t', 'hasn', 'maybe', 'probably', 'another',
             'believe', 'two', 'seen', 'anyway', 'seem', 'sup', 'into',
             'found', 'are', 'unless', 'does', 'taken', 'came', 'where', 'so',
             'gives', 'apart', 'ought', 'think', 'necessary', 'though', 'one',
             'thorough', 'many', 'entirely', 'actually', 'call', 'appear',
             'such', 'definitely', 'th', 'himse\"', 'associated', 'ask', 'to',
             'describe', 'they\'ve', 'but', 'through', 'anyways', 'won\'t',
             'won', 'becoming', 'willing', 'available', 'seven', 'cant', 'had',
             'mainly', 'zero', 'either', 'ours', 'whenever', 'un', 'yourself',
             'has', 'up', 'five', 'they\'d', 'those', 'us', 'beforehand',
             'seeming', 'given', 'last', 'let\'s', 'might', 'this', 'please',
             'reasonably', 'look', 'whatever', 'thin', 'especially', 'once',
             'everywhere', 'name', 'know', 'overall', 'vs', 'full', 'allow',
             'next', 'que', 'doing', 'away', 'asking', 'nearly', 'changes',
             'show', 'that\'s', 'non', 'we', 'anything', 'nor', 'not',
             'interest', 'now', 'themselves', 'throughout', 'he\'s', 'wants',
             'hence', 'wonder', 'every', 'unto', 'they\'re', '\'re', 'yes',
             'again', 'was', 'yet', 'indeed', 'i\'ll', 'way', 'inasmuch',
             'what', 'furthermore', 'ones', 'itse\"', 'whole', 'during',
             'none', 'beyond', 'three', 'when', 'put', 'her', 'whoever', 'far',
             'nobody', 'truly', 'between', 'it\'ll', 'okay', 'give', 'still',
             'having', 'come', 'they\'ll', '\'ll', 'itself', 'toward',
             'hereupon', 'among', 'anyone', 'following', 'i\'d', 'noone',
             'our', 'ourselves', 'i\'m', '\'m', 'specified', 'out', 'across',
             'couldnt', 'computer', 'seeing', 'moreover', 'causes', 'get',
             'course', 'merely', 'sensible', 'wherever', 'more',
             'unfortunately', 'lately', 'help', 'cannot', 'self', 'hereby',
             'whereafter', 'certain', 'first', 'thr', 'before', 'own', 'tell',
             'clearly', 'used', 'him', 'looks', 'his', 'only', 'should', 'few',
             'from', 'consider', 'keeps', 'described', 'otherwise', 'you\'d',
             'whither', 'you\'ll', 'like', 'goes', 'it\'s', 'bottom',
             'particular', 'towards', 'done', 'inner', 'regards', 'sent',
             'both', 'most', 'twice', 'outside', 'ed', 'keep', 'it\'d',
             'herself', 'seems', 'thereupon', 'who', 'here', 'everybody',
             'part', 'according', 'their', 'why', 'elsewhere', 'hers', 'can',
             'alone', 'along', 'who\'s', 'said', 'ltd', 'value', 'inc',
             'amount', 'move', 'will', 'hereafter', 'herse\"', 'saw', 'also',
             'say', 'enough', 'instead', 'gets', 'really', 'currently',
             'someone', 'third', 'corresponding', 'mean', 'various', 'neither',
             'latter', 'uses', 'further', 'front', 'tends', 'normally', 'dont',
             'couldnt', 't', 'nt', 'doesnt', 'ive', 'shouldnt', 'youve', 've',
             'wed', 'd', 'wouldnt', 'ts', 's', 'arent', 'cs', 'youre', 're',
             'well', 'theres', 'werent', 'weve', 've', 'as', 'isnt', 'hadnt',
             'cant', 'aint', 'didnt', 'were', 'cmon', 'whats', 'havent',
             'wasnt', 'wheres', 'heres', 'hasnt', 'theyve', 'lets', 'let',
             'thats', 'hes', 'theyre', 're', 'ill', 'itll', 'theyll', 'll',
             'id', 'im', 'youd', 'youll', 'its', 'itd', 'whos', 'amp'])


def preprocess_text(s):
    """
    Function to preprocess the raw tweet text. Basic text processing is being
    used:
        - clean the tweet from stopwords,
        - remove links and mentions, etc.

    Args:
        s (str): The raw tweet-node content.

    Returns:
       The preprocessed string.

    """
    delete_char_set = set(['\"', '\'', '-', '+', '=', ':', '(', ')', '&', '^',
                           ';'])
    new_s = ''
    for char in s:
        if char in delete_char_set:
            continue
        new_s += char

    exclude = set(['.', ',', '?', '!'])
    words_list = new_s.split(' ')
    new_words_list = []
    if len(words_list) > 1:
        for word in words_list:
            if len(word) > 1:
                word = word.lower()

                # Delete punctuation marks only if they appear at the start or
                # the end of the word
                if word[0] in exclude:
                    word = word[1:]
                if word[-1] in exclude:
                    word = word[:-1]

                if (word.startswith('@') or word.startswith('http') or
                        word in stops):
                    continue
                new_words_list.append(word)

    return ' '.join(new_words_list)


def ground_truth():
    """
    Function to get a the ground truth for the Twitter dataset.

    Returns:
       A list of integers. The ground truth in a binary list, where each
       position is the time window id and '0' indicates no existence of events
       and '1' existence of at least one event.

    """
    gt_binary = []
    gt_windows_set = set([50, 51, 52, 53, 54, 55, 56, 57, 58, 60, 78, 79, 80,
                         81, 82, 83, 84, 120, 121, 122, 123, 124, 125, 126,
                         127, 130, 131, 132, 133, 134, 135, 136, 137, 140, 141,
                         142, 143, 144, 145, 146, 147, 150, 151, 152, 153, 158,
                         204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214,
                         215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225,
                         226, 227, 237, 238, 239, 240, 241, 242, 243, 246, 247,
                         248, 249, 335, 336, 337, 338, 341, 342, 343, 344, 427,
                         428, 429, 430, 431, 432, 433, 434, 435, 437, 438, 439,
                         440, 521, 522, 523, 524, 525, 526, 527, 528, 529, 532,
                         533, 534, 535, 622, 623, 624, 625, 628, 629, 630, 631,
                         702, 703, 704, 705, 706, 707, 708, 709, 718, 719, 720,
                         721, 724, 725, 726, 727, 780, 781, 782, 783, 784, 785,
                         786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796,
                         797, 799, 800, 801, 802, 803, 804, 805, 806, 807, 810,
                         811, 812, 813, 814, 815, 816, 817, 820, 821, 822, 823,
                         879, 880, 881, 882, 883, 884, 885, 886, 890, 891, 892,
                         893, 894, 895, 896, 897, 889, 907, 908, 909, 910, 911,
                         912, 915, 916, 917, 918])

    for i in range(0, 940):
        if i in gt_windows_set:
            gt_binary.append(1)
        else:
            gt_binary.append(0)

    return gt_binary

