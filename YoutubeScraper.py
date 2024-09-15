# Source: https://www.geeksforgeeks.org/how-to-extract-youtube-comments-using-youtube-api-python/
# Get api key: https://support.google.com/googleapi/answer/6158862?hl=en

from googleapiclient.discovery import build
from transformers import pipeline

MAX_CARACTERE=500

class YoutubeScraper:
    """docstring for YoutubeScraper"""
    def __init__(self, api_key, videoId):
        print("[*] Init youtube scraper")
        self.api_key = api_key
        self.videoId = videoId

        # creating youtube resource object
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

        # retrieve youtube video results
        self.video_response = self.youtube.commentThreads().list(
            part='snippet,replies',
            videoId=self.videoId
        ).execute()

        self.comments = []

        print("[**] Youtube scraper ready for: https://www.youtube.com/watch?v={}".format(videoId))

    def get_comments(self, verbose=False):
        print("[*] Starting scraping")

        print("[**] Getting comments from: https://www.youtube.com/watch?v={}".format(self.videoId))
        # iterate video response
        while self.video_response:

            # extracting required info
            # from each result object 
            for item in self.video_response['items']:
                self.comments.append(item)

                if verbose:
                    print(item)

            # Again repeat
            if 'nextPageToken' in self.video_response:
                self.video_response = self.youtube.commentThreads().list(
                        part = 'snippet,replies',
                        videoId = self.videoId,
                        pageToken = self.video_response['nextPageToken']
                    ).execute()
            else:
                break


        print("[**] Ending scraping")

    def add_sentiment_analysis(self, verbose=False):
        print("[*] Start sentiment analysis")

        print("[**] Importing the pre-trained model for sentiment analysis")

        # Load a pre-trained pipeline for sentiment analysis
        sentiment_analyzer = pipeline("sentiment-analysis")

        print("[**] Performing sentiment analysis")
        for item in self.comments:
            # Analyze the sentiment of the texts
            item['snippet']['topLevelComment']['snippet']['analysisSentimental'] = sentiment_analyzer(item['snippet']['topLevelComment']['snippet']['textDisplay'][:MAX_CARACTERE])

        if verbose:
            # Display the results
            for item in self.comments:
                print("Text : {}\nSentiment analysis score: {}\n".format(item['snippet']['topLevelComment']['snippet']['textDisplay'], item['snippet']['topLevelComment']['snippet']['analysisSentimental']))

        print("[**] Adding sentiment analysis score")

if __name__ == '__main__':    
    # faire un simple url
    videoId = 'nLRL_NcnK-4'

    ys = YoutubeScraper('XXXXXXXX', videoId)
    ys.get_comments(verbose=True)

    print("[End]")
