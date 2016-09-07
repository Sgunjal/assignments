# coding: utf-8

"""
CS579: Assignment 0
Collecting a political social network

In this assignment, I've given you a list of Twitter accounts of 4
U.S. presedential candidates.

The goal is to use the Twitter API to construct a social network of these
accounts. We will then use the [networkx](http://networkx.github.io/) library
to plot these links, as well as print some statistics of the resulting graph.

1. Create an account on [twitter.com](http://twitter.com).
2. Generate authentication tokens by following the instructions [here](https://dev.twitter.com/docs/auth/tokens-devtwittercom).
3. Add your tokens to the key/token variables below. (API Key == Consumer Key)
4. Be sure you've installed the Python modules
[networkx](http://networkx.github.io/) and
[TwitterAPI](https://github.com/geduldig/TwitterAPI). Assuming you've already
installed [pip](http://pip.readthedocs.org/en/latest/installing.html), you can
do this with `pip install networkx TwitterAPI`.

OK, now you're ready to start collecting some data!

I've provided a partial implementation below. Your job is to complete the
code where indicated.  You need to modify the 10 methods indicated by
#TODO.

Your output should match the sample provided in Log.txt.
"""

# Imports you'll need.
from collections import Counter
import matplotlib.pyplot as plt
import networkx as nx
import sys
import time
import configparser
import json
import re
from TwitterAPI import TwitterAPI
from nltk.test.unit.test_seekable_unicode_stream_reader import STRINGS
from xlwt.antlr import ifelse

consumer_key = 'EMBcTZDeaiQ6NoVTv51a3CEZm'
consumer_secret = '8lM7Vz7kIq0XtniLU715T14GsBx6411I5xeNbzdwDqFPylhPgE'
access_token = '64342841-f3LAynjrVCwtWWpF7jpsrhgwa8U2BYBNb9SZg7s4P'
access_token_secret = 'uFYVdx0pHXO96D4vz2Qs2CpNM1bwXiZdUkws2pmZKKqTl'

# This method is done for you. Make sure to put your credentials in the file twitter.cfg.
def get_twitter():
    """ Construct an instance of TwitterAPI using the tokens you entered above.
    Returns:
      An instance of TwitterAPI.
    """        
    return TwitterAPI(consumer_key, consumer_secret, access_token, access_token_secret)

def read_screen_names(filename):
    """
    Read a text file containing Twitter screen_names, one per line.

    Params:
        filename....Name of the file to read.
    Returns:
        A list of strings, one per screen_name, in the order they are listed
        in the file.

    Here's a doctest to confirm your implementation is correct.
    >>> read_screen_names('candidates.txt')
    ['DrJillStein', 'GovGaryJohnson', 'HillaryClinton', 'realDonaldTrump']
    """
    ###TODO
    file_obj = open("candidates.txt","r")  
    screen_strings=re.findall(r"\S+",file_obj.read())      
    return screen_strings
    pass

# I've provided the method below to handle Twitter's rate limiting.
# You should call this method whenever you need to access the Twitter API.
def robust_request(twitter, resource, params, max_tries=5):
    """ If a Twitter request fails, sleep for 15 minutes.
    Do this at most max_tries times before quitting.
    Args:
      twitter .... A TwitterAPI object.
      resource ... A resource string to request; e.g., "friends/ids"
      params ..... A parameter dict for the request, e.g., to specify
                   parameters like screen_name or count.
      max_tries .. The maximum number of tries to attempt.
    Returns:
      A TwitterResponse object, or None if failed.
    """
    for i in range(max_tries):
        request = twitter.request(resource, params)
        if request.status_code == 200:
            return request
        else:
            print('Got error %s \nsleeping for 15 minutes.' % request.text)
            sys.stderr.flush()
            time.sleep(61 * 15)


def get_users(twitter, screen_names):
    """Retrieve the Twitter user objects for each screen_name.
    Params:
        twitter........The TwitterAPI object.
        screen_names...A list of strings, one per screen_name
    Returns:
        A list of dicts, one per user, containing all the user information
        (e.g., screen_name, id, location, etc)

    See the API documentation here: https://dev.twitter.com/rest/reference/get/users/lookup

    In this example, I test retrieving two users: twitterapi and twitter.

    >>> twitter = get_twitter()
    >>> users = get_users(twitter, ['twitterapi', 'twitter'])
    >>> [u['id'] for u in users]
    [6253282, 783214]
    """
    ###TODO
    responseofRequest=[]    
    resource='users/lookup'
    params={'screen_name':screen_names}
    responseofRequest = robust_request(twitter, resource, params, max_tries=5)    
    return responseofRequest
    pass


def get_friends(twitter, screen_name):
    """ Return a list of Twitter IDs for users that this person follows, up to 5000.
    See https://dev.twitter.com/rest/reference/get/friends/ids

    Note, because of rate limits, it's best to test this method for one candidate before trying
    on all candidates.

    Args:
        twitter.......The TwitterAPI object
        screen_name... a string of a Twitter screen name
    Returns:
        A list of ints, one per friend ID, sorted in ascending order.

    Note: If a user follows more than 5000 accounts, we will limit ourselves to
    the first 5000 accounts returned.

    In this test case, I return the first 5 accounts that I follow.
    >>> twitter = get_twitter()
    >>> get_friends(twitter, 'aronwc')[:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    resource='friends/ids'
    params={'screen_name':screen_name ,'count':5000}
    responseofRequest=robust_request(twitter, resource, params, max_tries=5)
    friend_ids=[r for r in responseofRequest]
    return friend_ids  
    pass


def add_all_friends(twitter, users):
    """ Get the list of accounts each user follows.
    I.e., call the get_friends method for all 4 candidates.

    Store the result in each user's dict using a new key called 'friends'.

    Args:
        twitter...The TwitterAPI object.
        users.....The list of user dicts.
    Returns:
        Nothing

    >>> twitter = get_twitter()
    >>> users = [{'screen_name': 'aronwc'}]
    >>> add_all_friends(twitter, users)
    >>> users[0]['friends'][:5]
    [695023, 1697081, 8381682, 10204352, 11669522]
    """
    ###TODO
    for user in users:
        friendlist = get_friends(twitter,user['screen_name'])
        user.update({'friends':friendlist})
    pass


def print_num_friends(users):
    """Print the number of friends per candidate, sorted by candidate name.
    See Log.txt for an example.
    Args:
        users....The list of user dicts.
    Returns:
        Nothing
    """
    ###TODO
    for user in sorted(users, key=lambda x: x['screen_name']):
        print(user['screen_name']+" "+str(len(user['friends'])))
    pass


def count_friends(users):
    """ Count how often each friend is followed.
    Args:
        users: a list of user dicts
    Returns:
        a Counter object mapping each friend to the number of candidates who follow them.
        Counter documentation: https://docs.python.org/dev/library/collections.html#collections.Counter

    In this example, friend '2' is followed by three different users.
    >>> c = count_friends([{'friends': [1,2]}, {'friends': [2,3]}, {'friends': [2,3]}])
    >>> c.most_common()
    [(2, 3), (3, 2), (1, 1)]
    """
    ###TODO
    friendlist=[]
    for user in users:
        friendlist+=user['friends']        
    return Counter(friendlist)
    pass


def friend_overlap(users):
    """
    Compute the number of shared accounts followed by each pair of users.

    Args:
        users...The list of user dicts.

    Return: A list of tuples containing (user1, user2, N), where N is the
        number of accounts that both user1 and user2 follow.  This list should
        be sorted in descending order of N. Ties are broken first by user1's
        screen_name, then by user2's screen_name (sorted in ascending
        alphabetical order). See Python's builtin sorted method.

    In this example, users 'a' and 'c' follow the same 3 accounts:
    >>> friend_overlap([
    ...     {'screen_name': 'a', 'friends': ['1', '2', '3']},
    ...     {'screen_name': 'b', 'friends': ['2', '3', '4']},
    ...     {'screen_name': 'c', 'friends': ['1', '2', '3']},
    ...     ])
    [('a', 'c', 3), ('a', 'b', 2), ('b', 'c', 2)]
    """
    ###TODO
    list2=[]
    candidates_count=0
    user_list=({})   
    for user in users:
        candidates_count=candidates_count+1    
    x=1;
    min_counter=0;
    y=0
    while y<(candidates_count-1):
        x=y+1
        while x<candidates_count:
            min_counter=0
            len_user1=len(users[y]['friends'])
            len_user2=len(users[x]['friends'])
            if len_user1>=len_user2:
                max_val=len_user1
                min_val=len_user2
            else:
                max_val=len_user2
                min_val=len_user1
            counter1=0;
            while counter1<max_val:
                counter2=0;
                while counter2<min_val:
                    if users[y]['friends'][counter1] == users[x]['friends'][counter2]:
                        min_counter=min_counter+1
                    counter2=counter2+1
                counter1=counter1+1                              
            
            list1= [users[y]['screen_name'],users[x]['screen_name'],min_counter]        
            list2.append(list1)            
            x=x+1
        y=y+1   
    
    return sorted(list2, key=lambda x:(x[2], x[0]),reverse=True)  
    pass


def followed_by_hillary_and_donald(users, twitter):
    """
    Find and return the screen_name of the one Twitter user followed by both Hillary
    Clinton and Donald Trump. You will need to use the TwitterAPI to convert
    the Twitter ID to a screen_name. See:
    https://dev.twitter.com/rest/reference/get/users/lookup

    Params:
        users.....The list of user dicts
        twitter...The Twitter API object
    Returns:
        A string containing the single Twitter screen_name of the user
        that is followed by both Hillary Clinton and Donald Trump.
    """
    ###TODO
    friendlist=[]
    for user in users:
        if user['screen_name']=='HillaryClinton':
            x=len(user['friends'])
            friendlist=friendlist+user['friends']
        elif user['screen_name']=='realDonaldTrump':
            y=len(user['friends'])
            friendlist=friendlist+user['friends']
    
    for value,count in Counter(friendlist).most_common(1):
            val=value
    resource='users/lookup'
    params={'user_id':str(val)}
    request_response=twitter.request(resource, params)  
    xyz=request_response.json()    
    return xyz[0]['screen_name']
    pass


def create_graph(users, friend_counts):
    """ Create a networkx undirected Graph, adding each candidate and friend
        as a node.  Note: while all candidates should be added to the graph,
        only add friends to the graph if they are followed by more than one
        candidate. (This is to reduce clutter.)

        Each candidate in the Graph will be represented by their screen_name,
        while each friend will be represented by their user id.

    Args:
      users...........The list of user dicts.
      friend_counts...The Counter dict mapping each friend to the number of candidates that follow them.
    Returns:
      A networkx Graph
    """
    ###TODO
    list1=[]
    x=0
    graph = nx.Graph()
    for user in users:        
        graph.add_node(user['screen_name']) 
        list1=user['friends']
        len1=len(list1)        
        for x in range(len1):                      
            if friend_counts[list1[x]] > 1:
                graph.add_node(list1[x])
                graph.add_edge(list1[x], user['screen_name'])            
    return graph   
    pass


def draw_network(graph, users, filename):
    """
    Draw the network to a file. Only label the candidate nodes; the friend
    nodes should have no labels (to reduce clutter).

    Methods you'll need include networkx.draw_networkx, plt.figure, and plt.savefig.

    Your figure does not have to look exactly the same as mine, but try to
    make it look presentable.
    """
    ###TODO
    user_list=({})
    for user in users:
        user_list.update({user['screen_name']:user['screen_name']})            
    plt.figure(figsize=(12,12))    
    nx.draw_networkx(graph,labels=user_list,with_labels=True,alpha=.5, width=.2)    
    plt.savefig(filename)
    plt.show()
    pass


def main():
    """ Main method. You should not modify this. """
    twitter = get_twitter()
    screen_names = read_screen_names('candidates.txt')
    print('Established Twitter connection.')
    print('Read screen names: %s' % screen_names)
    users = sorted(get_users(twitter, screen_names), key=lambda x: x['screen_name'])
    print('found %d users with screen_names %s' %
          (len(users), str([u['screen_name'] for u in users])))
    add_all_friends(twitter, users)
    print('Friends per candidate:')
    print_num_friends(users)
    friend_counts = count_friends(users)
    print('Most common friends:\n%s' % str(friend_counts.most_common(5)))
    print('Friend Overlap:\n%s' % str(friend_overlap(users)))
    print('User followed by Hillary and Donald: %s' % followed_by_hillary_and_donald(users, twitter))

    graph = create_graph(users, friend_counts)
    print('graph has %s nodes and %s edges' % (len(graph.nodes()), len(graph.edges())))
    draw_network(graph, users, 'network.png')
    print('network drawn to network.png')


if __name__ == '__main__':
    main()

# That's it for now! This should give you an introduction to some of the data we'll study in this course.
