import re


class ScrapRegex:

    def __init__(self, tweets_amount, query_timeline_search, query_to_search):
        self.tweets_amount = tweets_amount
        self.query_timeline_search = query_timeline_search
        self.query_to_search = query_to_search
        self.data = []

    def scrap_filter(self, tweets_list):
        regex_list = []
        for tweets in tweets_list:
            regex = re.findall(fr'{self.query_timeline_search}', tweets)
            regex_list.append(regex)
        index_list = [regex_list.index(link) for link in regex_list if link != []]
        tweets_links = [tweets_list[i] for i in index_list]
        regex_list = [elements for elements in regex_list if elements != []]
        print(f'The number of occurencies of "{self.query_timeline_search}" in '
              f'{self.tweets_amount} tweets was: {len(regex_list)}\n')
        correct_tweets_links = list(set(tweets_links))
        return correct_tweets_links

    def organize_scrap_infos(self, scrap_info):
        for tweets in scrap_info:
            tweets_splited = tweets.split('\n')
            tweets_number_info = {'Comments': tweets_splited[-4] if len(tweets_splited[-4]) < 10 else 0,
                                  'Replys': tweets_splited[-3] if len(tweets_splited[-3]) < 10 else 0,
                                  'Likes': tweets_splited[-2] if len(tweets_splited[-2]) < 10 else 0,
                                  'Views': tweets_splited[-1] if len(tweets_splited[-1]) < 12 else 0}
            tweets_user_info = {'Username': tweets_splited[:2]}
            for remove in range(3):
                del tweets_splited[0]
            for deletion in range(3):
                try:
                    del tweets_splited[-1]
                except:
                    pass
            tweets_text_info = " ".join(tweets_splited)
            tweets_user_joined = " ".join(tweets_user_info['Username'])
            print(f'User: {tweets_user_joined} \n Tweet_Info: {tweets_number_info} \n Tweet: {tweets_text_info}')
            self.data.append({'Username': tweets_user_info['Username'],
                              'Comments': tweets_number_info['Comments'],
                              'Replys': tweets_number_info['Replys'],
                              'Likes': tweets_number_info['Likes'],
                              'Views': tweets_number_info['Views'],
                              'Text': tweets_text_info})
