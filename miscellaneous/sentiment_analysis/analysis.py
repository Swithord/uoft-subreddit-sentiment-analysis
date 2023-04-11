from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import pandas as pd
# from textblob import TextBlob
import csv

new = ['new college', 'nc', 'wilson', 'wetmore', '45 willcocks']
uc = ['uc', 'university college', 'whitney', 'sir dan', 'sir daniel', 'morrison']
trinity = ['trinity', 'trin', 'hilda']
vic = ['victoria', 'vic', 'annesley', 'margaret addison', 'roweel jackman', 'burwash']
woodsworth = ['woodsworth', 'ww']
smc = ['smc', 'st michael', 'st mike', 'st. michael', 'st. mike', 'st michaels', 'st mikes', 'st. michaels',
       'st. mikes', 'brennan', 'elmsley', 'sorbara', 'loretto']
innis = ['innis']
new = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in new]
uc = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in uc]
trinity = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in trinity]
vic = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in vic]
woodsworth = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in woodsworth]
smc = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in smc]
innis = [prefix + name + suffix for prefix in [' ', ' [', '{', '(']
             for suffix in ['!', '?', ',', '.', ':', ';', '}', ']', ')', "'", ' '] for name in innis]
all_names = new + uc + trinity + vic + woodsworth + smc + innis
analyzer = SentimentIntensityAnalyzer()
rejected = []


def get_list(csv_file: str) -> list[str]:
    """Splits a csv file into a list of strings containing the title and text."""
    with open(csv_file) as file:
        reader = csv.reader(file)
        _ = next(reader)

        lst = []
        for row in reader:
            lst.append((' ' + str(row[1]) + ' ' + str(row[2])).replace('\n', ' '))

        return lst


def analyse_polarity(text: str) -> float:
    """Analyses the polarity of a given string."""
    # blob = TextBlob(text)
    # return blob.sentiment.polarity
    return analyzer.polarity_scores(text)['neg']


def analyse_subreddit(csv_file: str) -> dict:
    posts = get_list(csv_file)
    sentiments = {'new': [], 'uc': [], 'trinity': [], 'vic': [], 'woodsworth': [], 'smc': [], 'innis': []}

    with open('rejected.txt', 'w') as rejected_file, open('new.txt', 'w') as new_file,\
        open('uc.txt', 'w') as uc_file, open('trinity.txt', 'w') as trinity_file,\
        open('vic.txt', 'w') as vic_file, open('woodsworth.txt', 'w') as woodsworth_file,\
            open('smc.txt', 'w') as smc_file, open('innis.txt', 'w') as innis_file:
        for post in posts:
            post_lower = post.lower()
            if any(name in post_lower for name in all_names):
                polarity = analyse_polarity(post)
                print(f'got post with polarity {polarity}: {post}')
                if any(name in post_lower for name in new):
                    sentiments['new'].append(polarity)
                    new_file.write(f'{polarity} | {post}\n')
                if any(name in post_lower for name in uc):
                    sentiments['uc'].append(polarity)
                    uc_file.write(f'{polarity} | {post}\n')
                if any(name in post_lower for name in trinity):
                    sentiments['trinity'].append(polarity)
                    trinity_file.write(f'{polarity} | {post}\n')
                if any(name in post_lower for name in vic):
                    sentiments['vic'].append(polarity)
                    vic_file.write(f'{polarity} | {post}\n')
                if any(name in post_lower for name in woodsworth):
                    sentiments['woodsworth'].append(polarity)
                    woodsworth_file.write(f'{polarity} | {post}\n')
                if any(name in post_lower for name in smc):
                    sentiments['smc'].append(polarity)
                    smc_file.write(f'{polarity} | {post}\n')
                if any(name in post_lower for name in innis):
                    sentiments['innis'].append(polarity)
                    innis_file.write(f'{polarity} | {post}\n')
            else:
                rejected_file.write(post + '\n')

    return sentiments


if __name__ == '__main__':
    print(all_names)
    result = analyse_subreddit('uoft.csv')
    colleges_dict = {'college': [], 'score': [], 'n': []}
    for college in result:
        colleges_dict['college'].append(college)
        colleges_dict['score'].append(sum(result[college]) / len(result[college]))
        colleges_dict['n'].append(len(result[college]))

    colleges = pd.DataFrame(colleges_dict)
    colleges.to_csv('results2.csv')
