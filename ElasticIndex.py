# send data to elastic
# https://www.elastic.co/guide/en/cloud/current/ec-getting-started-python.html

from elasticsearch import Elasticsearch

class ElasticIndex:
	"""docstring for ElasticIndex"""

	def __init__(self, password, path_ca, index_name, server="https://localhost:9200/", user="elastic"):
		print("[*] Init elastic cluster")

		self.es = Elasticsearch(
		    server,
		    ca_certs=path_ca,
		    basic_auth=(user, password)
		)
		print("[**] Connected to the elastic cluster\n{}".format(self.es.info()))

		# Index variables
		self.index_name = index_name
		print("[**] Index name: {}".format(self.index_name))
		print("[**] Elastic Connected")

	def query(self, query):
		# Perform the search
		result = self.es.search(index=self.index_name, body=query)

		print("[*] Result query on {}".format(self.index_name))
		# Print the search results
		for hit in result['hits']['hits']:
		    print(hit['_source'])

	def send_data(self, data, verbose=False):
		for item in data:
			# print(item)
		
			# Index the document in Elasticsearch
			response = self.es.index(index=self.index_name, body=item)

			if verbose:
				# Print the response from Elasticsearch (including information about the indexing operation)
				print(response)

		print("[*] Data added in index {}".format(self.index_name))

	def delete_all(self, verbose=False):
		# Define a query that matches all documents
		query = {
		    "query": {
		        "match_all": {}
		    }
		}

		# Use the delete_by_query API to delete all documents
		response = self.es.delete_by_query(index=self.index_name, body=query)

		if verbose:
			# Print the response from Elasticsearch (including information about the delete operation)
			print(response)



if __name__ == '__main__':	
	ei = ElasticIndex(
	 	password="XXXXXXXX",
		path_ca="../elasticsearch-8.15.1/config/certs/http_ca.crt",
		index_name="XXXXXXXX"
	)

	# Define a simple match-all query
	query = {
	    "query": {
	        "match_all": {}
	    }
	}

	# ei.query(query)