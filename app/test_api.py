##########################################################################################
# test_api.py
#
# A simple test script to verify that our RegulationsGovAPI client is working as expected.
#
# This script:
# 1. Loads the API key from a .env file using python_dotenv.
# 2. Instantiates the RegulationsGovAPI client.
# 3. Makes a few sample API calls to test different endpoints.
# 4. Prints out results in a formatted and readable manner.
#
# Before running this script, ensure:
# - You have a .env file in the same directory containing the line: RGA_KEY=YOUR_API_KEY
# - You have installed python-dotenv and requests:
#     pip install python-dotenv requests
#
# Usage:
#     python test_api.py
#
##########################################################################################

import os
from dotenv import load_dotenv
from regulations_gov_api import RegulationsGovAPI
import json

def pretty_print(json_data):
    """
    Utility function to pretty-print JSON data.
    """
    print(json.dumps(json_data, indent=4))

def main():
    # Load environment variables from .env
    load_dotenv()
    api_key = os.getenv("RGA_KEY")
    if not api_key:
        print("Error: RGA_KEY not found in .env file. Please ensure it's set.")
        return

    # Instantiate our API client
    api = RegulationsGovAPI(api_key=api_key)

    # ---------------------------------
    # Test: Get documents (simple query)
    # ---------------------------------
    print("Testing: GET /documents with a simple searchTerm='water'")
    try:
        docs_response = api.get_documents(filter_searchTerm="water", page_size=5)
        pretty_print(docs_response)
    except Exception as e:
        print(f"Error fetching documents: {e}")

    # ---------------------------------
    # Test: Get a specific document by ID
    # Note: Use a known example document ID from the docs: "FDA-2009-N-0501-0012"
    # ---------------------------------
    print("\nTesting: GET /documents/{documentId}")
    try:
        doc_detail = api.get_document_by_id("FDA-2009-N-0501-0012")
        pretty_print(doc_detail)
    except Exception as e:
        print(f"Error fetching document by ID: {e}")

    # ---------------------------------
    # Test: Get comments (simple query)
    # ---------------------------------
    print("\nTesting: GET /comments with filter searchTerm='water'")
    try:
        comments_response = api.get_comments(filter_searchTerm="water", page_size=5)
        pretty_print(comments_response)
    except Exception as e:
        print(f"Error fetching comments: {e}")

    # ---------------------------------
    # Test: Get a single docket by ID
    # Example docket from docs: "EPA-HQ-OAR-2003-0129"
    # ---------------------------------
    print("\nTesting: GET /dockets/{docketId}")
    try:
        docket_detail = api.get_docket_by_id("EPA-HQ-OAR-2003-0129")
        pretty_print(docket_detail)
    except Exception as e:
        print(f"Error fetching docket by ID: {e}")

    # ---------------------------------
    # Test: Get agency categories
    # Using EPA as example acronym
    # ---------------------------------
    print("\nTesting: GET /agency-categories with filter[acronym]='EPA'")
    try:
        categories = api.get_agency_categories("EPA")
        pretty_print(categories)
    except Exception as e:
        print(f"Error fetching agency categories: {e}")

    # ---------------------------------
    # Test: Create submission key (for posting comments with attachments)
    # ---------------------------------
#    print("\nTesting: POST /submission-keys")
#    try:
#        submission_key_resp = api.create_submission_key()
#        pretty_print(submission_key_resp)
#    except Exception as e:
#        print(f"Error creating submission key: {e}")

    # ---------------------------------
    # Test: Create file upload url
    # Note: This requires a valid submissionKey from the previous call.
    # If successful, we can try to create a file upload url.
    # ---------------------------------
#    print("\nTesting: POST /file-upload-urls (requires submissionKey)")
#    try:
#        sub_key = submission_key_resp.get("data", {}).get("id")
#        if sub_key:
#            upload_url_resp = api.create_file_upload_url(submissionKey=sub_key,
#                                                         fileName="test.jpg",
#                                                         contentType="image/jpeg")
#            pretty_print(upload_url_resp)
#        else:
#            print("No submissionKey available to test file-upload-urls endpoint.")
#    except Exception as e:
#        print(f"Error creating file upload url: {e}")

    # ---------------------------------
    # Test: Post a comment (ANONYMOUS without attachment)
    # IMPORTANT: This requires a valid documentId that is open for comments.
    #            The provided documentId in examples may or may not be open.
    #            In a real test, you would pick a document you know is open for comments.
    #
    # For demonstration purposes, if this fails due to the document not being open for
    # comments or other validation errors, that is expected.
    # ---------------------------------
#    print("\nTesting: POST /comments (ANONYMOUS)")
#    try:
        # Attempt to post a test comment on a known document.
        # Adjust the documentId if needed for a real test.
#        post_comment_attributes = {
#            "commentOnDocumentId": "FDA-2009-N-0501-0012",
#            "comment": "This is a test comment via API.",
#            "submissionType": "API",
#            "submitterType": "ANONYMOUS"
#          }

#        post_comment_resp = api.post_comment(post_comment_attributes)
#        pretty_print(post_comment_resp)
#    except Exception as e:
#        print(f"Error posting comment: {e}")

if __name__ == "__main__":
    main()
