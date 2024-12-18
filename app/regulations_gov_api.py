##########################################################################################
# regulations_gov_api.py
#
# This module provides a Python implementation for interacting with the Regulations.gov
# Public API v4 as specified in the given OpenAPI specification and documentation.
#
# The goal is to provide a simple, extensible, and well-documented client that can be
# integrated into a generative AI agent or chatbot, allowing the agent to call this API
# with minimal friction.
#
# ----------------------------------------
# Key Features:
# ----------------------------------------
# 1. Provides methods to:
#    - Search and retrieve documents
#    - Retrieve details for a single document
#    - Search and retrieve comments
#    - Create a new comment
#    - Retrieve details for a single comment
#    - Search and retrieve dockets
#    - Retrieve details for a single docket
#    - Fetch categories for a specific agency
#    - Generate submission keys for comment submissions with attachments
#    - Generate pre-signed file-upload URLs for attachments
#
# 2. Uses requests library to make HTTP calls.
#
# 3. Allows passing of an API key for authorized requests via header.
#
# 4. Methods provide parameters matching the API spec for filtering, sorting, paging, etc.
#
# 5. Follows best practices:
#    - Clear docstrings for each method.
#    - Checks for required parameters.
#    - Returns JSON responses directly.
#
# 6. Includes graceful error handling for non-200 responses:
#    - Raises exceptions with meaningful messages if the API returns a non-success status code.
#
# ----------------------------------------
# Usage Example:
# ----------------------------------------
# from regulations_gov_api import RegulationsGovAPI
#
# api = RegulationsGovAPI(api_key="YOUR_API_KEY")
#
# # Search documents by search term:
# docs = api.get_documents(filter_searchTerm="water")
#
# # Get a single document by ID:
# doc_detail = api.get_document_by_id("FDA-2009-N-0501-0012")
#
# # Post a comment (e.g. anonymous comment without attachment):
# response = api.post_comment(attributes={
#     "commentOnDocumentId": "FDA-2009-N-0501-0012",
#     "comment": "test comment",
#     "submissionType": "API",
#     "submitterType": "ANONYMOUS"
# })
#
# print(response)
#
##########################################################################################

import requests
from urllib.parse import urlencode

class RegulationsGovAPIError(Exception):
    """Custom exception for Regulations.gov API errors."""
    pass


class RegulationsGovAPI:
    """
    A client for the Regulations.gov public API v4.
    
    This class provides methods to interact with the Regulations.gov API endpoints
    as specified in the OpenAPI specification and documentation.
    """

    BASE_URL = "https://api.regulations.gov/v4"

    def __init__(self, api_key: str):
        """
        Initialize the API client with a provided API key.
        
        :param api_key: Your Regulations.gov API key as a string.
        """
        self.api_key = api_key
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/vnd.api+json"
        }

    def _get(self, endpoint: str, params: dict = None):
        """
        Internal method for handling GET requests.
        
        :param endpoint: API endpoint (e.g. "/documents")
        :param params: Dictionary of query parameters
        :return: JSON response from the API
        :raises RegulationsGovAPIError: if response status is not successful
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        if not response.ok:
            raise RegulationsGovAPIError(f"GET {url} failed with status {response.status_code}: {response.text}")
        return response.json()

    def _post(self, endpoint: str, data: dict):
        """
        Internal method for handling POST requests.
        
        :param endpoint: API endpoint (e.g. "/comments")
        :param data: JSON body as a dictionary
        :return: JSON response from the API
        :raises RegulationsGovAPIError: if response status is not successful
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.post(url, headers=self.headers, json={"data": data})
        if response.status_code not in (200, 201):
            raise RegulationsGovAPIError(f"POST {url} failed with status {response.status_code}: {response.text}")
        return response.json()

    # ----------------------------
    # DOCUMENTS ENDPOINTS
    # ----------------------------

    def get_documents(self,
                      filter_agencyId: str = None,
                      filter_commentEndDate: str = None,
                      filter_docketId: str = None,
                      filter_documentType: str = None,
                      filter_frDocNum: str = None,
                      filter_searchTerm: str = None,
                      filter_postedDate: str = None,
                      filter_lastModifiedDate: str = None,
                      filter_subtype: str = None,
                      filter_withinCommentPeriod: bool = None,
                      sort: str = None,
                      page_number: int = None,
                      page_size: int = None):
        """
        Retrieve a list of documents matching the provided filters.
        
        :param filter_agencyId: e.g. "EPA"
        :param filter_commentEndDate: Date filter (format: yyyy-MM-dd, can use ge/le)
        :param filter_docketId: Filter by a specific docket ID
        :param filter_documentType: One of [Notice, Rule, Proposed Rule, Supporting & Related Material, Other]
        :param filter_frDocNum: Filter by FR document number
        :param filter_searchTerm: Full-text search term
        :param filter_postedDate: Date filter (format: yyyy-MM-dd, can use ge/le)
        :param filter_lastModifiedDate: DateTime filter (yyyy-MM-dd HH:mm:ss, can use ge/le)
        :param filter_subtype: Filter by document subtype
        :param filter_withinCommentPeriod: If True, filter documents currently open for comment
        :param sort: Sort by a field. e.g. "postedDate", "-postedDate"
        :param page_number: Page number (1 to 20)
        :param page_size: Page size (5 to 250)
        
        :return: JSON response with documents list and metadata.
        """
        params = {}
        if filter_agencyId:
            params['filter[agencyId]'] = filter_agencyId
        if filter_commentEndDate:
            params['filter[commentEndDate]'] = filter_commentEndDate
        if filter_docketId:
            params['filter[docketId]'] = filter_docketId
        if filter_documentType:
            params['filter[documentType]'] = filter_documentType
        if filter_frDocNum:
            params['filter[frDocNum]'] = filter_frDocNum
        if filter_searchTerm:
            params['filter[searchTerm]'] = filter_searchTerm
        if filter_postedDate:
            params['filter[postedDate]'] = filter_postedDate
        if filter_lastModifiedDate:
            params['filter[lastModifiedDate]'] = filter_lastModifiedDate
        if filter_subtype:
            params['filter[subtype]'] = filter_subtype
        if filter_withinCommentPeriod is True:
            params['filter[withinCommentPeriod]'] = 'true'
        if sort:
            params['sort'] = sort
        if page_number:
            params['page[number]'] = page_number
        if page_size:
            params['page[size]'] = page_size

        return self._get("/documents", params)

    def get_document_by_id(self, document_id: str, include_attachments: bool = False):
        """
        Retrieve detailed information for a specified document by ID.
        
        :param document_id: The documentId to fetch details for.
        :param include_attachments: If True, include attachments in the response.
        
        :return: JSON response with document details.
        """
        params = {}
        if include_attachments:
            params['include'] = 'attachments'
        return self._get(f"/documents/{document_id}", params)

    # ----------------------------
    # COMMENTS ENDPOINTS
    # ----------------------------

    def get_comments(self,
                     filter_agencyId: str = None,
                     filter_searchTerm: str = None,
                     filter_postedDate: str = None,
                     filter_lastModifiedDate: str = None,
                     filter_commentOnId: str = None,
                     sort: str = None,
                     page_number: int = None,
                     page_size: int = None):
        """
        Retrieve a list of comments based on given filters.
        
        :param filter_agencyId: e.g. "EPA"
        :param filter_searchTerm: Full-text search term
        :param filter_postedDate: Date filter (yyyy-MM-dd, can use ge/le)
        :param filter_lastModifiedDate: DateTime filter (yyyy-MM-dd HH:mm:ss, can use ge/le)
        :param filter_commentOnId: Filters results on supplied commentOnId (objectId of a document)
        :param sort: Sort field (e.g. postedDate, -postedDate)
        :param page_number: Page number (1 to 20)
        :param page_size: Page size (5 to 250)
        
        :return: JSON response with comments list and metadata.
        """
        params = {}
        if filter_agencyId:
            params['filter[agencyId]'] = filter_agencyId
        if filter_searchTerm:
            params['filter[searchTerm]'] = filter_searchTerm
        if filter_postedDate:
            params['filter[postedDate]'] = filter_postedDate
        if filter_lastModifiedDate:
            params['filter[lastModifiedDate]'] = filter_lastModifiedDate
        if filter_commentOnId:
            params['filter[commentOnId]'] = filter_commentOnId
        if sort:
            params['sort'] = sort
        if page_number:
            params['page[number]'] = page_number
        if page_size:
            params['page[size]'] = page_size

        return self._get("/comments", params)

    def post_comment(self, attributes: dict):
        """
        Create a new comment.
        
        According to the spec, the request body should be:
        {
          "data": {
            "type": "comments",
            "attributes": { ... }
          }
        }
        
        attributes must at least contain:
          - commentOnDocumentId
          - comment
          - submissionType (always "API")
          - submitterType (one of "ANONYMOUS","INDIVIDUAL","ORGANIZATION")
          
        For anonymous:
          attributes={
            "commentOnDocumentId":"DOCUMENT_ID",
            "comment":"Your comment text",
            "submissionType":"API",
            "submitterType":"ANONYMOUS"
          }
        
        :param attributes: Dict containing the comment attributes.
        :return: JSON response with the created comment details.
        """
        data = {
            "type": "comments",
            "attributes": attributes
        }
        return self._post("/comments", data)

    def get_comment_by_id(self, comment_id: str, include_attachments: bool = False):
        """
        Retrieve detailed information for a specified comment by commentId.
        
        :param comment_id: The ID of the comment to retrieve.
        :param include_attachments: If True, include attachments.
        
        :return: JSON response with the comment details.
        """
        params = {}
        if include_attachments:
            params['include'] = 'attachments'
        return self._get(f"/comments/{comment_id}", params)

    # ----------------------------
    # DOCKETS ENDPOINTS
    # ----------------------------

    def get_dockets(self,
                    filter_agencyId: str = None,
                    filter_searchTerm: str = None,
                    filter_lastModifiedDate: str = None,
                    filter_docketType: str = None,
                    sort: str = None,
                    page_number: int = None,
                    page_size: int = None):
        """
        Retrieve a list of dockets based on given filters.
        
        :param filter_agencyId: e.g. "EPA"
        :param filter_searchTerm: Full-text search term
        :param filter_lastModifiedDate: Date filter (yyyy-MM-dd HH:mm:ss, can use ge/le)
        :param filter_docketType: One of [Rulemaking, Nonrulemaking]
        :param sort: e.g. "title", "-title"
        :param page_number: Page number (1 to 20)
        :param page_size: Page size (5 to 250)
        
        :return: JSON response with dockets list and metadata.
        """
        params = {}
        if filter_agencyId:
            params['filter[agencyId]'] = filter_agencyId
        if filter_searchTerm:
            params['filter[searchTerm]'] = filter_searchTerm
        if filter_lastModifiedDate:
            params['filter[lastModifiedDate]'] = filter_lastModifiedDate
        if filter_docketType:
            params['filter[docketType]'] = filter_docketType
        if sort:
            params['sort'] = sort
        if page_number:
            params['page[number]'] = page_number
        if page_size:
            params['page[size]'] = page_size

        return self._get("/dockets", params)

    def get_docket_by_id(self, docket_id: str):
        """
        Retrieve detailed information for a specified docket by docketId.
        
        :param docket_id: The docketId to fetch details for.
        :return: JSON response with docket details.
        """
        return self._get(f"/dockets/{docket_id}")

    # ----------------------------
    # AGENCY CATEGORIES ENDPOINT
    # ----------------------------

    def get_agency_categories(self, acronym: str):
        """
        Returns a list of categories for a specific agency acronym.
        
        :param acronym: Agency acronym (e.g. "EPA")
        :return: JSON response with list of categories
        """
        params = {'filter[acronym]': acronym}
        return self._get("/agency-categories", params)

    # ----------------------------
    # SUBMISSION KEYS ENDPOINT
    # ----------------------------

    def create_submission_key(self):
        """
        Creates a unique submission key for posting comments with attachments.
        
        :return: JSON response with the newly created submission key.
        """
        data = {"type": "submission-keys"}
        return self._post("/submission-keys", data)

    # ----------------------------
    # FILE UPLOAD URLS ENDPOINT
    # ----------------------------

    def create_file_upload_url(self, submissionKey: str, fileName: str, contentType: str):
        """
        Creates a presigned URL to upload a file to the S3 bucket.
        
        Steps to attach a file to a comment:
          1) Create submission key
          2) Create upload URL for each file
          3) Upload binaries to the returned presigned URL
          4) Post comment using the submissionKey and fileName
        
        :param submissionKey: The unique submission key obtained from create_submission_key.
        :param fileName: The name of the file to upload.
        :param contentType: The MIME type of the file (e.g. "image/jpeg").
        :return: JSON response containing the presigned URL and file metadata.
        """
        data = {
            "type": "file-upload-urls",
            "attributes": {
                "submissionKey": submissionKey,
                "fileName": fileName,
                "contentType": contentType
            }
        }
        return self._post("/file-upload-urls", data)
