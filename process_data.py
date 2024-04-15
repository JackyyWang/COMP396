import json
from collections import Counter


# set of stop words
stop_words = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 
'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 
'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 
'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are',
 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing',
 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 
'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 
'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 
'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 
'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn',
 "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 
'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

def process_transcript(transcript):
    if transcript.startswith("Transcript not found"):
        return []
    words = transcript.lower().split()
    words = [word.strip('.,!;()[]') for word in words]
    words = [word for word in words if word and word not in stop_words]
    word_counts = Counter(words)
    return [word for word, _ in word_counts.most_common(10)]


input_file_path = 'fox_playlist_data.json'

output_file_path = 'updated_fox_playlist_data.json'

try:
    with open(input_file_path, 'r') as file:
        json_data = json.load(file)

    for video_id, video_data in json_data.items():
        transcript = video_data.get('transcript', '')
        most_common_words = process_transcript(transcript)
        json_data[video_id]['mostCommonWords'] = most_common_words

    with open(output_file_path, 'w') as file:
        json.dump(json_data, file, indent=4)

except FileNotFoundError:
    print("The original JSON file was not found.")
except Exception as e:
    print(f"An error occurred: {e}")
