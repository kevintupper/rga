##########################################################################################
# rga_console_chatbot.py
#
# This script creates a console chatbot using the SWARM framework and the regulations.gov
# API client that we previously built.
#
# The idea:
# - We load the RGA_KEY (Regulations.gov API Key) from a .env file using python_dotenv.
# - We instantiate our RegulationsGovAPI client with this key.
# - We create an Agent that has access to a set of functions that wrap around the
#   RegulationsGovAPI client methods, allowing the Agent to search documents, dockets,
#   comments, and even post comments via the console.
#
# The user can interact with the agent by typing queries in the console. The agent will use
# the provided functions (tools) to get data from the regulations.gov API and respond with
# relevant information.
#
# The code heavily leverages the SWARM example patterns, but is adapted to our use case.
#
# Usage:
#   1. Ensure you have a .env file with: RGA_KEY=YOUR_REGULATIONS_GOV_API_KEY
#   2. pip install -r requirements.txt (should include requests, openai, python-dotenv, swarm)
#   3. Run: python console_chatbot.py
#
##########################################################################################

import os
import json
from dotenv import load_dotenv
from regulations_gov_api import RegulationsGovAPI
import sys

# Add the parent directory of 'app' and 'swarm' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from swarm import Swarm, Agent
from swarm.repl import run_demo_loop

##########################################################################################
# Load environment variables from .env
##########################################################################################
load_dotenv()
api_key = os.getenv("RGA_KEY")
if not api_key:
    print("Error: RGA_KEY not found in .env. Please set it before running.")
    exit(1)

##########################################################################################
# Instantiate the Regulations.gov API client
##########################################################################################
reg_api = RegulationsGovAPI(api_key=api_key)

##########################################################################################
# Define agent functions wrapping the regulations.gov API
#
# These functions will be callable by the agent. They should:
# - Take parameters as needed (e.g. filter strings)
# - Call the corresponding method in regulations_gov_api
# - Return a user-friendly string that the Agent can show to the user
#
# NOTE: The agent can call these functions by name. The docstrings help the agent understand
# what the functions do. We also handle JSON results from the API and format them.
##########################################################################################


def search_documents(filter_searchTerm: str = None,
                     filter_agencyId: str = None,
                     filter_documentType: str = None,
                     page_size: int = 5) -> str:
    """
    Search documents on regulations.gov.
    
    Args:
        filter_searchTerm: Search term to look for in documents.
        filter_agencyId: Filter by agency acronym, e.g. 'EPA'.
        filter_documentType: Filter by document type (e.g. 'Proposed Rule').
        page_size: How many results to return.
    """
    response = reg_api.get_documents(
        filter_searchTerm=filter_searchTerm,
        filter_agencyId=filter_agencyId,
        filter_documentType=filter_documentType,
        page_size=page_size
    )

    docs = response.get("data", [])
    if not docs:
        return "No documents found."
    # Format a brief summary of documents
    results = []
    for d in docs:
        title = d["attributes"]["title"]
        doc_id = d["id"]
        doc_type = d["attributes"]["documentType"]
        posted_date = d["attributes"]["postedDate"]
        results.append(f"- {title} (ID: {doc_id}, Type: {doc_type}, Posted: {posted_date})")

    return "Documents:\n" + "\n".join(results)


def get_document_detail(document_id: str, include_attachments: bool = False) -> str:
    """
    Get detailed information for a specified document by documentId.
    
    Args:
        document_id: The Document ID to retrieve.
        include_attachments: If True, also fetch attachments.
    """
    response = reg_api.get_document_by_id(document_id, include_attachments=include_attachments)
    
    # Check if the response contains the expected data
    data = response.get("data", {})
    if not data:
        return f"Document with ID {document_id} not found."

    attr = data.get("attributes", {})
    title = attr.get("title", "No title")
    docket_id = attr.get("docketId", "N/A")
    doc_type = attr.get("documentType", "N/A")
    posted_date = attr.get("postedDate", "N/A")
    comment = attr.get("comment", "N/A")
    subject = attr.get("subject", "N/A")
    topics = ", ".join(attr.get("topics", []))
    page_count = attr.get("pageCount", "N/A")
    file_formats = attr.get("fileFormats", [])

    # Format file formats information
    files_info = "\n".join(
        [f"Format: {f['format']}, URL: {f['fileUrl']}, Size: {f['size']} bytes" for f in file_formats]
    )

    info = [
        f"Title: {title}",
        f"Docket ID: {docket_id}",
        f"Type: {doc_type}",
        f"Posted Date: {posted_date}",
        f"Comment Text: {comment}",
        f"Subject: {subject}",
        f"Topics: {topics}",
        f"Page Count: {page_count}",
        f"Files:\n{files_info}"
    ]
    return "\n".join(info)


def search_comments(filter_searchTerm: str = None, page_size: int = 5) -> str:
    """
    Search comments on regulations.gov.
    
    Args:
        filter_searchTerm: Search term for comments.
        page_size: Number of results.
    """
    response = reg_api.get_comments(filter_searchTerm=filter_searchTerm, page_size=page_size)
    comments = response.get("data", [])
    if not comments:
        return "No comments found."

    results = []
    for c in comments:
        title = c["attributes"]["title"]
        cid = c["id"]
        posted = c["attributes"]["postedDate"]
        results.append(f"- {title} (Comment ID: {cid}, Posted: {posted})")

    return "Comments:\n" + "\n".join(results)


def search_dockets(filter_searchTerm: str = None, page_size: int = 5) -> str:
    """
    Search dockets on regulations.gov.
    
    Args:
        filter_searchTerm: Search term for dockets.
        page_size: How many results to return.
    """
    response = reg_api.get_dockets(filter_searchTerm=filter_searchTerm, page_size=page_size)
    dockets = response.get("data", [])
    if not dockets:
        return "No dockets found."

    results = []
    for d in dockets:
        title = d["attributes"]["title"]
        did = d["id"]
        modified = d["attributes"]["lastModifiedDate"]
        results.append(f"- {title} (Docket ID: {did}, Last Modified: {modified})")

    return "Dockets:\n" + "\n".join(results)


def get_docket_detail(docket_id: str) -> str:
    """
    Get detailed information for a specified docket by docketId.
    
    Args:
        docket_id: The Docket ID to retrieve.
    """
    response = reg_api.get_docket_by_id(docket_id)
    if "title" not in response.get("attributes", {}):
        return f"Docket with ID {docket_id} not found."

    attr = response["attributes"]
    title = attr.get("title", "No title")
    docket_type = attr.get("docketType", "N/A")
    modify_date = attr.get("modifyDate", "N/A")
    rin = attr.get("rin", "N/A")

    info = [
        f"Title: {title}",
        f"Docket Type: {docket_type}",
        f"Last Modified: {modify_date}",
        f"RIN: {rin}"
    ]
    return "\n".join(info)


def post_anonymous_comment(document_id: str, comment_text: str) -> str:
    """
    Post an anonymous comment on a given documentId.
    
    Args:
        document_id: ID of the document to comment on.
        comment_text: The comment to post.
    """
    attrs = {
        "commentOnDocumentId": document_id,
        "comment": comment_text,
        "submissionType": "API",
        "submitterType": "ANONYMOUS"
    }

    try:
        resp = reg_api.post_comment(attributes=attrs)
        # The response should have an id and attributes for the posted comment
        c_id = resp.get("id", "N/A")
        return f"Comment posted successfully! Comment ID: {c_id}"
    except Exception as e:
        return f"Failed to post comment: {str(e)}"


##########################################################################################
# Create our SWARM Agent
#
# The instructions tell the agent what it is and what it can do. We tell it that it can
# help the user interact with the regulations.gov API. The agent can call the functions
# we defined above to fulfill user requests.
##########################################################################################

agent = Agent(
    name="RegulationsGovAgent",
    instructions=(
        "You are a helpful agent that can search and retrieve information from the "
        "Regulations.gov API. The user may ask you to find documents, comments, dockets, "
        "or post a comment. Use the provided functions to answer their questions.\n\n"
        "For example:\n"
        "- To find documents about 'water', call search_documents with filter_searchTerm='water'.\n"
        "- To get details of a specific document, call get_document_detail(document_id='...').\n"
        "- To find comments about a term, call search_comments.\n"
        "- To search for dockets, call search_dockets.\n"
        "- To get details of a docket, call get_docket_detail(docket_id='...').\n"
        "- To post a comment anonymously, call post_anonymous_comment(document_id='...', comment_text='...').\n\n"
        "Always return a clear, user-friendly answer. If you're unsure what the user is asking, "
        "ask for clarification."
    ),
    model="gpt-4o",
    functions=[
        search_documents,
        get_document_detail,
        search_comments,
        search_dockets,
        get_docket_detail,
        post_anonymous_comment
    ]
)

##########################################################################################
# Run the interactive console loop using run_demo_loop provided by SWARM
#
# The user can type queries, and the agent will respond.
##########################################################################################

if __name__ == "__main__":
    # We run the demo loop. The user can now type queries in the console.
    # The agent can call the functions as needed and respond accordingly.
    run_demo_loop(agent, stream=True)
