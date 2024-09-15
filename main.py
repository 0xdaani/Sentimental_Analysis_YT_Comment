from ElasticIndex import ElasticIndex
from YoutubeScraper import YoutubeScraper


if __name__ == '__main__':

	# ElasticSearch infos
	password = "XXXXXXXX"
	index_name = "XXXXXXXX"

	# Youtube infos
	# https://www.youtube.com/watch?v=nLRL_NcnK-4
	videoId = "nLRL_NcnK-4"
	# Get api key: https://support.google.com/googleapi/answer/6158862?hl=en
	api_key = "XXXXXXXX"
	
	ei = ElasticIndex(
	 	password=password,
		path_ca="../elasticsearch-8.15.1/config/certs/http_ca.crt",
		index_name=index_name
	)

	ys = YoutubeScraper(
		api_key=api_key, 
		videoId=videoId
	)

	# Scrape comments from the specified YouTube video
	ys.get_comments()
	# Add sentiment analysis on the retrieved comments
	ys.add_sentiment_analysis()


	# Delete all existing data in the Elasticsearch index
	ei.delete_all()
	# Send the processed comments (including sentiment analysis) to Elasticsearch index
	ei.send_data(ys.comments)

	# # Define a simple match-all query
	# query = {
	#     "query": {
	#         "match_all": {}
	#     }
	# }

	# ei.query(query)
