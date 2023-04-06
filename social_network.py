# Name: Erin Morales

import networkx as nx
import matplotlib.pyplot as plt
from operator import itemgetter

def get_practice_graph():
    """Builds and returns the practice graph
    """
    practice_graph = nx.Graph()

    practice_graph.add_edge("A", "B")
    practice_graph.add_edge("A", "C")
    practice_graph.add_edge("B", "C")
    practice_graph.add_edge("B", "D")
    practice_graph.add_edge("D", "C")
    practice_graph.add_edge("D", "F")
    practice_graph.add_edge("D", "E")
    practice_graph.add_edge("F", "C")
    return practice_graph


def draw_practice_graph(graph):
    """Draw practice_graph to the screen.
    """
    nx.draw_networkx(graph)
    plt.show()

def get_romeo_and_juliet_graph():
    """Builds and returns the romeo and juliet graph
    """
    rj = nx.Graph()
    rj.add_edge("Nurse", "Juliet")
    rj.add_edge("Juliet", "Tybalt")
    rj.add_edge("Juliet", "Friar Laurence")
    rj.add_edge("Juliet", "Capulet")
    rj.add_edge("Tybalt", "Capulet")
    rj.add_edge("Capulet", "Escalus")
    rj.add_edge("Capulet", "Paris")
    rj.add_edge("Escalus", "Paris")
    rj.add_edge("Escalus", "Mercutio")
    rj.add_edge("Mercutio", "Romeo")
    rj.add_edge("Romeo", "Montague")
    rj.add_edge("Romeo", "Benvolio")
    rj.add_edge("Romeo", "Friar Laurence")
    rj.add_edge("Romeo", "Juliet")
    rj.add_edge("Montague", "Escalus")
    rj.add_edge("Paris", "Mercutio")
    rj.add_edge("Montague", "Benvolio")

    return rj


def draw_rj(graph):
    """Draw the rj graph to the screen and to a file.
    """
    nx.draw_networkx(graph)
    plt.savefig("romeo-and-juliet.pdf")
    plt.show()

def friends(graph, user):
    """Returns a set of the friends of the given user, in the given graph.
    """
    return set(graph.neighbors(user))


def friends_of_friends(graph, user):
    """Find and return the friends of friends of the given user.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a set containing the names of all of the friends of
    friends of the user. The set should not contain the user itself
    or their immediate friends.
    """
    result = set()
    mutual_friends = friends(graph, user)
    for next_friend in mutual_friends:
        next_next_friends = friends(graph, next_friend)
        result = result | next_next_friends
    result.remove(user)
    result = result - mutual_friends
    return result


def common_friends(graph, user1, user2):
    """
    Finds and returns the set of friends that user1 and user2 have in common.

    Arguments:
        graph:  the graph object that contains the users
        user1: a string representing one user
        user2: a string representing another user

    Returns: a set containing the friends user1 and user2 have in common
    """
    return friends(graph, user1) & friends(graph, user2)


def number_of_common_friends_map(graph, user):
    """Returns a map (a dictionary), mapping a person to the number of friends
    that person has in common with the given user. The map keys are the
    people who have at least one friend in common with the given user,
    and are neither the given user nor one of the given user's friends.
    Example: a graph called my_graph and user "X"
    Here is what is relevant about my_graph:
        - "X" and "Y" have two friends in common
        - "X" and "Z" have one friend in common
        - "X" and "W" have one friend in common
        - "X" and "V" have no friends in common
        - "X" is friends with "W" (but not with "Y" or "Z")
    Here is what should be returned:
      number_of_common_friends_map(my_graph, "X")  =>   { 'Y':2, 'Z':1 }

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: a dictionary mapping each person to the number of (non-zero)
    friends they have in common with the user
    """
    com_friend_dict = dict()
    user_friend = friends_of_friends(graph, user)
    for x in user_friend:
        com_friend_dict[x] = len((common_friends(graph, x, user)))
    return com_friend_dict


def number_map_to_sorted_list(map_with_number_vals):
    """Given a dictionary, return a list of the keys in the dictionary.
    The keys are sorted by the number value they map to, from greatest
    number down to smallest number.
    When two keys map to the same number value, the keys are sorted by their
    natural sort order for whatever type the key is, from least to greatest.

    Arguments:
        map_with_number_vals: a dictionary whose values are numbers

    Returns: a list of keys, sorted by the values in map_with_number_vals
    """
    map_list = []
    sort_map = sorted(map_with_number_vals.items())
    list_sort = sorted(sort_map, key=itemgetter(1), reverse=True)
    for x in list_sort:
        map_list.append(x[0])
    return map_list


def recommend_by_number_of_common_friends(graph, user):
    """
    Returns a list of friend recommendations for the user, sorted
    by number of friends in common.

    Arguments:
        graph: the graph object that contains the user and others
        user: a string

    Returns: A list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the number of common friends (people
    with the most common friends are listed first).  In the
    case of a tie in number of common friends, the names/IDs are
    sorted by their natural sort order, from least to greatest.
    """
    num_com_fren = number_of_common_friends_map(graph, user)
    fren_sort_lst = number_map_to_sorted_list(num_com_fren)
    return fren_sort_lst


def influence_map(graph, user):
    """
    Returns a map (a dictionary) mapping from each person to their
    influence score, with respect to the given user. The map only
    contains people who have at least one friend in common with the given
    user and are neither the user nor one of the users's friends.
    See the assignment writeup for the definition of influence scores.
    """
    fren_map = {}
    com_fren = friends_of_friends(graph, user)
    for person in com_fren:
        fren_set = common_friends(graph, user, person)
        influence_score = 0
        num_frens = 0
        for x in fren_set:
            num_frens = len(list(graph.neighbors(x)))
            influence_score = influence_score + (1/num_frens)
        fren_map[person] = influence_score
    return fren_map


def recommend_by_influence(graph, user):
    """Return a list of friend recommendations for the given user.
    The friend recommendation list consists of names/IDs of people in
    the graph who are not yet a friend of the given user.  The order
    of the list is determined by the influence score (people
    with the biggest influence score are listed first).  In the
    case of a tie in influence score, the names/IDs are sorted
    by their natural sort order, from least to greatest.
    """
    influ_map = influence_map(graph, user)
    return number_map_to_sorted_list(influ_map)

def get_facebook_graph():
    """
    Builds and returns the facebook graph
    """
    my_file = open('facebook-links-small.txt')
    facebook = nx.Graph()
    for txt in my_file:
        line = txt.split()
        person = line[0]
        fren = line[1]
        facebook.add_edge(int(fren), int(person))
    my_file.close()
    return facebook


def main():

    rj = get_romeo_and_juliet_graph()

    print("Problem 4:")
    print()

    names = rj.nodes
    different_list = []
    same_list = []
    for user in names:
        com_rec = (recommend_by_number_of_common_friends(rj, user))
        influ_rec = (recommend_by_influence(rj, user))
        if com_rec == influ_rec:
            same_list.append(user)
        else:
            different_list.append(user)

    print('Unchanged Recommendations:', sorted(same_list))
    print('Changed Recommendations:', sorted(different_list))

    facebook = get_facebook_graph()
    # assert len(facebook.nodes()) == 63731
    # assert len(facebook.edges()) == 817090

    print()
    print("Problem 6:")
    print()
    fb_profile = facebook.nodes()
    sorted_fb_profile = sorted(fb_profile)
    for user in sorted_fb_profile:
        if user % 1000 == 0:
            fren_rec_list = recommend_by_number_of_common_friends(facebook,
                                                                  user)[0:10]
            print(user, '(by num_common_friends): ', fren_rec_list)

    print()
    print("Problem 7:")
    print()

    for user in sorted_fb_profile:
        if user % 1000 == 0:
            list_influ = recommend_by_influence(facebook, user)[0:10]
            print(user, '(by influence): ', list_influ)

    print()
    print("Problem 8:")
    print()

    same_num = 0
    different_num = 0
    for user in sorted_fb_profile:
        if user % 1000 == 0:
            fren_rec = recommend_by_number_of_common_friends(facebook, user)
            influ_rec = recommend_by_influence(facebook, user)
            if influ_rec != fren_rec:
                different_num += 1
            elif influ_rec == fren_rec:
                same_num += 1

    print('Same:', same_num)
    print('Different:', different_num)


if __name__ == "__main__":
    main()
