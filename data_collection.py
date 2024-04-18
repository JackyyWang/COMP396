import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from youtube_transcript_api import YouTubeTranscriptApi
import json

# Setup YouTube API
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"
client_secrets_file = ""

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
    client_secrets_file, scopes)
credentials = flow.run_console()
youtube = googleapiclient.discovery.build(
    api_service_name, api_version, credentials=credentials)

def get_video_ids(youtube, playlist_id):
    video_ids = []
    request = youtube.playlistItems().list(part="snippet", playlistId=playlist_id, maxResults=50)
    while request:
        response = request.execute()
        for item in response.get('items', []):
            video_ids.append(item['snippet']['resourceId']['videoId'])
        request = youtube.playlistItems().list_next(request, response)
    return video_ids

def get_video_comments(youtube, video_id):
    comments = []
    request = youtube.commentThreads().list(part="snippet", videoId=video_id, textFormat="plainText", maxResults=100)
    while request:
        response = request.execute()
        for item in response.get('items', []):
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        request = youtube.commentThreads().list_next(request, response)
    return comments

def get_video_details(youtube, video_id):
    request = youtube.videos().list(part="snippet,contentDetails,statistics", id=video_id)
    response = request.execute()

    details = response.get("items", [])[0]
    snippet = details["snippet"]
    statistics = details["statistics"]
    contentDetails = details["contentDetails"]

    return {
        "channelTitle": snippet.get("channelTitle"),
        "viewCount": statistics.get("viewCount"),
        "likeCount": statistics.get("likeCount"),
        "commentCount": statistics.get("commentCount"),
        "duration": contentDetails.get("duration")
    }

playlist_id_list = ["PL6XRrncXkMaU55GiCvv416NR2qBD_xbmf"]

#playlist_id = "PL0tDb4jw6kPwbfkRqaiNFdr0d_rl9vAXP"



data = {}

for playlist_id in playlist_id_list:
    video_ids = get_video_ids(youtube, playlist_id)
    for video_id in video_ids:
        video_data = {}
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = ' '.join([x['text'] for x in transcript_list])
            video_data['transcript'] = transcript_text
        except Exception as e:
            video_data['transcript'] = f"Transcript not found: {e}"

        try:
            video_details = get_video_details(youtube, video_id)
            video_data.update(video_details)
        except Exception as e:
            video_data['details'] = f"Video details not found: {e}"

        try:
            comments = get_video_comments(youtube, video_id)
            video_data['comments'] = comments
        except Exception as e:
            video_data['comments'] = f"Comments not found: {e}"

        data[video_id] = video_data

with open('CNN_playlist_data.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)

