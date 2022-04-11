from betamax.matchers.uri import URIMatcher
from betamax.matchers.query import QueryMatcher

from urllib.parse import urlparse


class CustomQueryMatcher(QueryMatcher):
    name = "custom_query"

    def match(self, request, recorded_request):
        # don't match api key query param
        request_query_dict = self.to_dict(urlparse(request.url).query)
        del request_query_dict["apikey"]
        recorded_query = urlparse(recorded_request["uri"]).query
        recorded_query_dict = self.to_dict(recorded_query)
        del recorded_query_dict["apikey"]
        # debug:
        # raise Exception(
        #     request_query_dict,
        #     recorded_query_dict,
        #     request_query_dict == recorded_query_dict,
        # )
        return request_query_dict == recorded_query_dict


class CustomURIMatcher(URIMatcher):
    name = "custom_uri"

    def on_init(self):
        self.query_matcher = CustomQueryMatcher().match
