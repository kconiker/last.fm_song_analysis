import codecs
from operator import itemgetter
import pandas as pd
from pandas import Series, DataFrame
import numpy as np

aid2name = {}
aid2numplays = {}
uid2numplays = {}
sorted_aidnumplays = []
sorted_uidnumplays = []
users_artists = {}
uid2fid = {}
usertagart_df = None

# read in files and process to get data for above variables

# read in artists
fp = codecs.open("artists.dat", encoding="utf-8")
fp.readline() #skip first line of headers
for line in fp:
    line = line.strip()
    fields = line.split('\t')
    aid = int(fields[0])
    name = fields[1]

    if aid == int(aid) and name != "":
        aid2name[aid] = name

fp.close()

# read in users, artist listened to, and number of times played
fp = codecs.open("user_artists.dat", encoding="utf-8")
fp.readline() #skip first line of headers
for line in fp:
    line = line.strip()
    fields2 = line.split('\t')
    user_id = int(fields2[0])
    artist_id = int(fields2[1])
    weight = int(fields2[2])

    # build a dictionary to store number of plays for each artist
    # read in only artist that are in aid2name
    if artist_id in aid2name:
        # create a total number of plays by summing up the weight for each artist
        if artist_id in aid2numplays:
            aid2numplays[artist_id] += weight
        else:
            aid2numplays[artist_id] = weight

    # build a dictionary to store number of plays for each user
    # create a total number of plays by summing up the weight for each user
    if user_id in uid2numplays:
        uid2numplays[user_id] += weight
    else:
        uid2numplays[user_id] = weight

    # build a dictionary of users and the artists they listened to
    users_artists.setdefault(user_id,[]).append(artist_id)

fp.close()

# create sorted list with highest counts at the beginning of the list
# for both artist and user lists
for artist in aid2numplays:
    pair = (artist, aid2numplays[artist])
    sorted_aidnumplays.append(pair)

sorted_aidnumplays = sorted(sorted_aidnumplays, key=itemgetter(1), reverse=True)

for user in uid2numplays:
    pair = (user, uid2numplays[user])
    sorted_uidnumplays.append(pair)

sorted_uidnumplays = sorted(sorted_uidnumplays, key=itemgetter(1), reverse=True)

# read users and who they are friends with
fp = codecs.open("user_friends.dat", encoding="utf-8")
fp.readline() #skip first line of headers
for line in fp:
    line = line.strip()
    fields = line.split('\t')
    uid = int(fields[0])
    fid = int(fields[1])

    uid2fid.setdefault(uid, []).append(fid)

fp.close()


usertagart_df = pd.read_table('user_taggedartists.dat', sep='\t', index_col=[5, 4])
usertagart_df2 = pd.read_table('user_taggedartists.dat', sep='\t', index_col=[5, 4, 1])


# print out each question then call the function that produces the answer
def main():
    print("\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n")
    print("1. Who are the top artists?")
    question_one()
    print()
    print("2. What artists have the most listeners?")
    num_artist_listeners = question_two()
    print()
    print("3. Who are the top users?")
    question_three()
    print()
    print("4. What artists have the highest average number of plays per listener?")
    artist_avg_plays = question_four(num_artist_listeners)
    print()
    print("5. What artists with at least 50 listeners have the highest average number of plays per listener?")
    question_five(artist_avg_plays)
    print()
    print("6. Do users with five or more friends listen to more songs?")
    question_six()
    print()
    print("7. How similar are two artists?")
    artist_sim(735, 562)
    artist_sim(735, 89)
    artist_sim(735, 289)
    artist_sim(89, 289)
    artist_sim(89, 67)
    artist_sim(67, 735)
    print()
    print("8. 10 artists with the highest overall number of tags, first month in top 10 and months in top ten")
    question_eight()



# question 1
# description: Take the first 10 artist from our sorted list "sorted_aidnumplays"
#              to get most played artists cross all users. Then look up the names
#              of the artists from "aid2name"
def question_one():
    for aid, song_plays in sorted_aidnumplays[:10]:
        print("\t" + str(aid2name[aid]) + "(" + str(aid) + ")", song_plays)

# question 2
# description: Grab the dictionary of users and the artists they have listened to
#              loop through the users then loop through the artists
#              if a user listened to an artist add the artist to the artist_listeners
#              dictionary. Next put the artist ID and count into a tuple. Then sort the
#              tuple and print out the top 10 artists
def question_two():
    artist_listeners = {}
    pair_artist_listeners = []

    for userID in users_artists:
        for artistID in users_artists[userID]:
            if artistID not in artist_listeners:
                artist_listeners[artistID] = 1
            else:
                artist_listeners[artistID] += 1

    for artistID in artist_listeners:
        pair = (artistID, artist_listeners[artistID])
        pair_artist_listeners.append(pair)

    sorted_artist_listeners = sorted(pair_artist_listeners, key=itemgetter(1), reverse=True)

    for artistID, listeners in sorted_artist_listeners[:10]:
        print("\t" + str(aid2name[artistID]) + "(" + str(artistID) + ")", listeners)

    return artist_listeners

# question 3
# description: loop through sorted_uidnumplays and print out the top ten
def question_three():
    for uid, playCount in sorted_uidnumplays[:10]:
        print("\t" + str(uid), playCount)

# question 4
# description: for each artist computed the average number of plays by taking
#              the total number of plays for each artist and dividing it by number
#              listeners put the values in a tuple, sort it then printing out the 10 highest artists name, id,
#              total plays, total number of listeners, and computed average
def question_four(num_artist_listeners):
    artist_avg_plays = {}
    pair_artist_avg = []

    for aid, plays in sorted_aidnumplays:
        listeners = num_artist_listeners[aid]
        artist_avg = plays / listeners
        artist_avg_plays[aid] = (artist_avg, plays, listeners)

    for artistID in artist_avg_plays:
        pair = (artistID, artist_avg_plays[artistID][0], artist_avg_plays[artistID][1], artist_avg_plays[artistID][2])
        pair_artist_avg.append(pair)

    sorted_artist_avg = sorted(pair_artist_avg, key=itemgetter(1), reverse=True)

    for artistID, avg, plays, listeners in sorted_artist_avg[:10]:
        print("\t" + str(aid2name[artistID]) + "(" + str(artistID) + ")", "total number of plays: " + str(plays), "total number of listeners: " + str(listeners), "average number of plays: " + str(avg))

    return artist_avg_plays

# question 5
# description: loop through the artist_avg_plays dictionary in question 4, check to see if it has more than 50 listeners
#              if so put the aid, avg, plays, and listeners in a tuple, sort the tuple and print the artist name, artist id,
#              total number of plays, total number of listeners, and the computed average number of plays per listener
def question_five(artist_avg_plays):
    pair_artist_filter_avg = []

    for aid in artist_avg_plays:
        if artist_avg_plays[aid][2] > 50:
            pair = (aid, artist_avg_plays[aid][0], artist_avg_plays[aid][1], artist_avg_plays[aid][2])
            pair_artist_filter_avg.append(pair)

    sorted_artist_filter_avg = sorted(pair_artist_filter_avg, key=itemgetter(1), reverse=True)

    for artistID, avg, plays, listeners in sorted_artist_filter_avg[:10]:
        print("\t" + str(aid2name[artistID]) + "(" + str(artistID) + ")", "total number of plays: " + str(plays), "total number of listeners: " + str(listeners), "average number of plays: " + str(avg))

# question 6
# description: find out who has 5 or more friends and compute the total, compute the total for who  has less than 5
#              friends, add up each of their total song plays using uid2numplays dictionary, divide total number of song
#              plays by total number of users print the print the two numbers with labels
def question_six():
    uid_total_friends_gtr = 0
    uid_total_friends_lss = 0
    total_gtr_plays = 0
    total_lss_plays = 0

    for uid in uid2fid:
        if uid in uid2numplays:
            if len(uid2fid[uid]) >= 5:
                uid_total_friends_gtr += 1
                total_gtr_plays += uid2numplays[uid]
            else:
                uid_total_friends_lss += 1
                total_lss_plays += uid2numplays[uid]

    avg_gtr = total_gtr_plays / uid_total_friends_gtr
    avg_lss = total_lss_plays / uid_total_friends_lss

    print("\tAverage number of songs for users with 5 or more friends", avg_gtr)
    print("\tAverage number of songs for users with less than 5 friends", avg_lss)

# question 7
# description: first compute the set of users who listened to aid1 and compute another set of users that listened
#              to aid2, do an intersection on the two sets and count how many values there are, do a union one the two
#              sets and count the values, then compute the Jaccard index by dividing the intersection by the union total
#              look up and print out both artist names using aid2name dictionary and then print the Jaccard index
def artist_sim(aid1,aid2):
    set_aid1 = set()
    set_aid2 = set()
    intersect = 0
    union = 0
    jaccard_index = 0

    for uid in users_artists:
        if aid1 in users_artists[uid]:
            set_aid1 = set_aid1.union({uid})
        if aid2 in users_artists[uid]:
            set_aid2 = set_aid2.union({uid})

    intersect = float(len(set_aid1.intersection(set_aid2)))
    union = float(len(set_aid1.union(set_aid2)))
    jaccard_index = intersect / union

    print("\t" + str(aid2name[aid1]) + ", " + str(aid2name[aid2]), str(jaccard_index))

# question 8
# description: compute the number of tags for each artist, group dataframe by artist id and count the number of tad IDs
#              10 artists with the highest overall number of tags, first month in top 10 and months in top 10
def question_eight():
    g = usertagart_df['tagID'].groupby(usertagart_df['artistID'])
    gcount = g.count()
    gcount.columns = ['artistID', 'tagCount']

    # pick top 10 tagged artists
    # artistIDs: 289, 89, 292, 67, 72, 227, 190, 154, 288, 157
    # number of tags: 931, 767, 762, 730, 701, 598, 595, 563, 528, 467
    gcountsort10 = gcount.sort_values(ascending=False).head(10)

    ten_popular_art = gcountsort10.index
    num_tags_top_ten = gcountsort10.values

    top_art_counts = zip(ten_popular_art, num_tags_top_ten)

    # create a nested dictionary to keep track of the total number of tags for the top ten artist, how many times an
    #  artist was in the top ten and the first month they were in the top ten

    art_count_dict = {}

    for artist, tag_count in top_art_counts:
         art_count_dict[artist] = {
             'first_month': None,
             'num_top_ten_months': 0,
             'num_tags': tag_count
         }

    # count tagIDs in dataframe by artistID, Month, and Year
    g_by_month = usertagart_df2['tagID'].groupby(['year','month','artistID']).count()

    # for a year in the dataframe starting at 2005
    year = 2005

    while year <= 2011:

        # get the current year from the dataframe
        current_year = g_by_month.loc[year:year].sort_index(level='month', ascending=True)
        # grab the list of months from the index
        list_of_months = current_year.index.get_level_values(1).values
        # create a unique list of months
        unique_months = np.unique(list_of_months)

        # for a month in current year
        # sort the monthly dataframe
        # see if on of the top artists is in the top ten for that month
        #   if so add a one to that artist in the art_count_dict

        for month in unique_months:
            current_month = current_year.loc[year:year, month:month].sort_values(ascending=False).head(10)
            for artist in art_count_dict:
                for artistID in current_month.index.get_level_values(2).values:
                    if artist == artistID:
                        if art_count_dict[artist]['first_month'] == None:
                            # convert month number into name
                            month_name = ''
                            if month == 1:
                                month_name = 'January'
                            if month == 2:
                                month_name = 'February'
                            if month == 3:
                                month_name = 'March'
                            if month == 4:
                                month_name = 'April'
                            if month == 5:
                                month_name = 'May'
                            if month == 6:
                                month_name = 'June'
                            if month == 7:
                                month_name = 'July'
                            if month == 8:
                                month_name = 'August'
                            if month == 9:
                                month_name = 'September'
                            if month == 10:
                                month_name = 'October'
                            if month == 11:
                                month_name = 'November'
                            if month == 12:
                                month_name = 'December'
                            art_count_dict[artist]['first_month'] = month_name + ' ' + str(year)
                        art_count_dict[artist]['num_top_ten_months'] = art_count_dict[artist]['num_top_ten_months'] + 1



        year = year + 1

    # print top ten artists with the most tags, when they first got into the top ten, and how many times they were in
    # the top ten
    for artist in art_count_dict:
        print("\t" + str(aid2name[artist]) + "(" + str(artist) + "):  num tags = ", end="")
        print(str(art_count_dict[artist]['num_tags']), ", first time in the top ten: ", end="")
        print(art_count_dict[artist]['first_month'] + ", number times in top ten ", end="")
        print(str(art_count_dict[artist]['num_top_ten_months']))

main()