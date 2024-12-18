<instructions>
Below is the API specification and documentation for the regulations.gov api.

I am going to build a generative AI agent that is art of a chatbot. The agent will have the ability call 
the api as part of its capabilities. Your job here is to fully implement the API so that the agent can
call it.

Your code should be very well documented and have commments preceding code blocks. Be generous in your 
comments so junior developers who are not familiar with code base or API can follow along easily.

Also, employ best practices and make sure the specification and documentation are followed and fully implemented.
The code returned should be complete. Our plan is to copy and paste what you return into prod and run it.
</instructions>

<regulations_gov_open_api_specification>
# open.yml
# ------------------
# Disclaimer:
# ------------------
# This Open API specification document is work in progress. This document will continue 
# to be updated until our Public API v4 is finalized.
#--------------------
openapi: 3.0.0
info:
  title: Regulations.gov API
  description: >-
    Public API for Regulations.gov
  version: "4.0"
servers:
  - url: 'https://api.regulations.gov/v4'
    description: Production endpoint for Regulations.gov API
security: 
  - ApiKeyAuth: []
paths:
  /documents:
    get:
      summary: List of documents
      description: This endpoint returns list of documents
      tags:
        - documents
      parameters: 
        - name: filter[agencyId]
          in: query
          description: >-
            'Filters results for the agency acronym specified in the value. Example: ''EPA'''
          required: false
          schema:
            type: string
        - name: filter[commentEndDate]
          in: query
          description: >-  
            Filters results relative to the comment end date.  The value must be formatted as `yyyy-MM-dd`.<br/><br/> Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used. <br/> `ge` - greater than or equal <br/> `le` - less than or equal
          required: false
          schema:
            type: string
            format: date
        - name: filter[docketId]
          in: query
          description: >-
            Filters results on the specified docket ID.
          required: false
          schema:
            type: string
        - name: filter[documentType]
          in: query
          description: >-
            Filters results on the specified document type.
          required: false
          schema:
            $ref: '#/components/schemas/DocumentType'
        - name: filter[frDocNum]
          in: query
          description: >-
            Filters results on the specified frDocNum.
          required: false
          schema:
            type: string
        - name: filter[searchTerm]
          in: query
          description: >-
            Filters results on the given term.
          required: false
          schema:
            type: string
        - name: filter[postedDate]
          in: query
          description: >-  
            Filters results relative to the posted date.  The value must be formatted as `yyyy-MM-dd`.<br/><br/> Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used. <br/> `ge` - greater than or equal <br/> `le` - less than or equal
          required: false
          schema:
            type: string
            format: date
        - name: filter[lastModifiedDate]
          in: query
          description: >-  
            Filters results relative to the last modified date.  The value must be formatted as `yyyy-MM-dd HH:mm:ss`.<br/><br/> Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used. <br/> `ge` - greater than or equal <br/> `le` - less than or equal
          required: false
          schema:
            type: string
            format: date            
        - name: filter[subtype]
          in: query
          description: >-
            Filters results on the supplied document subtype
          required: false
          schema:
            type: string
        - name: filter[withinCommentPeriod]
          in: query
          description: >-
            Filters results for documents that are open for comment by setting the value to `true`. <br/><br/> _`False` is not an acceptable value for this parameter, hence it should be removed when not being used._          
          required: false
          schema:
            type: boolean
        - name: sort
          in: query
          description: >-
            Sorts the results on the field specified in the value.  The default behavior will sort the results in ascending order; to sort in descending order, prepend a minus sign to the value. <br/><br/> Supported values are `commentEndDate`, `postedDate`, `lastModifiedDate`, `documentId` and `title`. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.         
          required: false
          schema:
            type: string
        - name: page[number]
          in: query
          description: >-
            Specifies the number for the page of results that will be returned from the query. <br/><br/> Acceptable values are numerical between, and including, 1 and 20.          
          required: false
          schema:
            type: integer
        - name: page[size]
          in: query
          description: >-
            Specifies the size per page of results that will be returned from the query. <br/><br/> Acceptable values are numerical between, and including, 5 and 250.           
          required: false
          schema:
            type: integer
      responses:
        '200':
          description: A JSON\:API document with the a list of documents
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/DocumentFindAllResponse'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError' 
  /documents/{documentId}:
    get:
      tags:
        - documents
      summary: Get detailed information for specified documentId
      description: Gets the detailed information of a specific document with the passed documentId.
      parameters:
        - name: documentId
          in: path
          description: ID of document to return
          required: true
          schema:
            type: string
        - name: include #Only supported value for include is attachments.
          in: query
          description: resources to include
          required: false
          schema:
            type: string
          example: attachments
      responses:
        '200':
          description: successful operation
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/DocumentFindOneResponse'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '404':
          description: Document not found
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
  /comments:
    get:
      summary: List of comments
      description: This endpoint returns list of comments 
      tags:
        - comments
      parameters: 
        - name: filter[agencyId]
          in: query
          description: >-
            'Filters results for the agency acronym specified in the value. Example: ''EPA'''
          required: false
          schema:
            type: string
        - name: filter[searchTerm]
          in: query
          description: >-
            Filters results on the given term.
          required: false
          schema:
            type: string
        - name: filter[postedDate]
          in: query
          description: >-
            Filters results relative to the posted date.  The value must be formatted as `yyyy-MM-dd`.<br/><br/> Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used. <br/> `ge` - greater than or equal <br/> `le` - less than or equal
          required: false
          schema:
            type: string
            format: date
        - name: filter[lastModifiedDate]
          in: query
          description: >-  
            Filters results relative to the last modified date.  The value must be formatted as `yyyy-MM-dd HH:mm:ss`.<br/><br/> Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used. <br/> `ge` - greater than or equal <br/> `le` - less than or equal
          required: false
          schema:
            type: string
            format: date
        - name: filter[commentOnId]
          in: query
          description: >-
            Filters results on the supplied commentOnId
          required: false
          schema:
            type: string
        - name: sort
          in: query
          description: >-
            Sorts the results on the field specified in the value.  The default behavior will sort the results in ascending order; to sort in descending order, prepend a minus sign to the value. <br/><br/> The only supported values are `postedDate`, `lastModifiedDate` and `documentId`. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.          
          required: false
          schema:
            type: string
        - name: page[number]
          in: query
          description: >-
            Specifies the number for the page of results that will be returned from the query. <br/><br/> Acceptable values are numerical between, and including, 1 and 20.          
          required: false
          schema:
            type: integer
        - name: page[size]
          in: query
          description: >-
            Specifies the size per page of results that will be returned from the query. <br/><br/> Acceptable values are numerical between, and including, 5 and 250.           
          required: false
          schema:
            type: integer
      responses:
        '200':
          description: A JSON\:API document with the a list of comments
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/CommentFindAllResponse'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
    post:
      summary: Creates a new comment.
      tags:
        - comments
      requestBody:
        description: A JSON object containing comment information
        required: true
        content:
          application/vnd.api+json:
            schema:
                $ref: '#/components/schemas/JSONResourcePostRequestObject'
      responses:
        '201':
          description: Created
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONResourcePostResponseObject'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '404':
          description: Document not found
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
  /comments/{commentId}:
    get:
      summary: Get detailed information for specified commentId
      description: Gets the detailed information of a specific comment with the passed commentId.
      tags:
        - comments
      parameters:
        - name: commentId
          in: path
          description: ID of comment to return
          required: true
          schema:
            type: string
        - name: include #Only supported value for include is attachments.
          in: query
          description: resources to include
          example: attachments
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/CommentFindOneResponse'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '404':
          description: Document not found
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
  /dockets:
    get:
      summary: List of dockets
      description: This endpoint returns list of dockets 
      tags:
        - dockets
      parameters:
        - name: filter[agencyId]
          in: query
          description: >-
            'Filters results for the agency acronym specified in the value. Example: ''EPA'''
          required: false
          schema:
            type: string
        - name: filter[searchTerm]
          in: query
          description: >-
            Filters results on the given term.
          required: false
          schema:
            type: string
        - name: filter[lastModifiedDate]
          in: query
          description: >-  
            Filters results relative to the last modified date.  The value must be formatted as `yyyy-MM-dd HH:mm:ss`.<br/><br/> Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used. <br/> `ge` - greater than or equal <br/> `le` - less than or equal
          required: false
          schema:
            type: string
            format: date
        - name: filter[docketType]
          in: query
          description: >-
            Filters results on the specified docket type.
          required: false
          schema:
            $ref: '#/components/schemas/DocketType'
        - name: sort
          in: query
          description: >-
            Sorts the results on the field specified in the value.  The default behavior will sort the results in ascending order; to sort in descending order, prepend a minus sign to the value. <br/><br/> The only supported values are `title`, `docketId` and `lastModifiedDate`. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.          
          required: false
          schema:
            type: string
        - name: page[number]
          in: query
          description: >-
            Specifies the number for the page of results that will be returned from the query. <br/><br/> Acceptable values are numerical between, and including, 1 and 20.          
          required: false
          schema:
            type: integer
        - name: page[size]
          in: query
          description: >-
            Specifies the size per page of results that will be returned from the query. <br/><br/> Acceptable values are numerical between, and including, 5 and 250.           
          required: false
          schema:
            type: integer
      responses:
        '200':
          description: A JSON\:API document with the a list of dockets
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/DocketFindAllResponse'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
  /dockets/{docketId}:
    get:
      tags:
        - dockets
      summary: Get detailed information for specified docketId
      description: Gets the detailed information of a specific docket with the passed docketId.
      parameters:
        - name: docketId
          in: path
          description: ID of docket to return
          required: true
          schema:
            type: string
      responses:
        '200':
          description: successful operation
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/DocketFindOneResponse'
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '404':
          description: Document not found
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
  /agency-categories:
    get:
      summary: Returns a list of categories
      description: This endpoint returns list of categories
      tags:
        - comment submission utilities
      parameters:
        - name: filter[acronym]
          in: query
          description: >-
            'Filters results for the agency acronym specified in the value. Example: ''EPA'''
          required: true
          schema:
            type: string
      responses:
        '200':
          description: List of agency categories
          content:
            application/vnd.api+json:
             schema: # TODO: Pull this object out into a component
                type: object 
                properties: 
                  data:
                    type: array
                    items:
                      type: object
                      properties:
                        default:
                          type: boolean
                          description: Defines if its the default category value
                        acronym:
                          type: string
                          description: Agency acronym
                        categories:
                          type: string
                          description: The name of the category
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
  /submission-keys:
    post:
      summary: Creates the unique submission key
      operationId: GetSubmitterKey
      tags:
        - comment submission utilities
      requestBody:
        content: 
          application/vnd.api+json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    type:
                      type: string
                      example: 'submissionKeys'
      responses:
        '201':
          description: Created
          content:
            application/vnd.api+json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                        id:
                          type: string
                          description: the newly created submission key
                        type:
                          type: string
                          example: 'submission-keys'
                        links:
                          $ref: '#/components/schemas/SelfLink'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'      
  /file-upload-urls:
    post:
      summary: Creates a presigned url to upload file
      tags:
        - comment submission utilities
      description: 'Returns a pre-signed URL to upload a file to the S3 bucket'
      requestBody:
        required: true
        content: 
          application/vnd.api+json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    type:
                      type: string
                      example: 'file-upload-urls'
                    attributes:
                      type: object
                      properties: 
                        submissionKey:
                          type: string
                          description: submission key for the submission
                        fileName:
                          type: string
                          description: name of the file to upload
                        contentType:
                          type: string
                          description: content type of the file
      responses:
        '201':
          description: Created
          content:
            application/vnd.api+json:
              schema:
                type: object
                properties:
                  data:
                    type: object
                    properties:
                      id:
                        type: string
                        format: uri
                        description: The pre-signed url to upload the file
                      type:
                        type: string
                        example: 'file-upload-urls'
                      attributes:
                        type: object
                        properties: 
                          submissionKey:
                            type: string
                            description: submission key for the submission
                          fileName:
                            type: string
                            description: name of the file to upload
                          contentType:
                            type: string
                            description: content type of the file
        '400':
          description: Validation error
          content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
        '403':
           description: API key is missing or invalid
           content:
            application/vnd.api+json:
              schema:
                $ref: '#/components/schemas/JSONError'
components:
  securitySchemes:
    ApiKeyAuth:          # arbitrary name for the security scheme
        type: apiKey
        in: header       # can be "header", "query" or "cookie"
        name: X-Api-Key  # name of the header, query parameter or cookie
  schemas:
    #JSON:API Specific documentation
    DocumentFindAllResponse:
      description: A JSON:API document with a list of resources
      properties:
        data:
          description: The list of documents where each document is a JSON:API document
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/DocumentFindAllItem'
        meta:
          $ref: '#/components/schemas/FindAllResponseMetadata'
    CommentFindAllResponse:
      description: A JSON:API document with a list of resources
      properties:
        data:
          description: The list of comments where each comment is a JSON:API document
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/CommentFindAllItem'
        meta:
          $ref: '#/components/schemas/FindAllResponseMetadata'
    DocketFindAllResponse:
      description: A JSON:API document with a list of resources
      properties:
        data:
          description: The list of dockets where each docket is a JSON:API document
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/DocketFindAllItem'
        meta:
          $ref: '#/components/schemas/FindAllResponseMetadata'
    DocumentFindAllItem:
      description: A JSON:API document which represents a single document in the list
      properties:
        id:
          description: The JSON:API resource ID `documentId`
          type: string
        type:
          description: The JSON:API resource type `documents`
          type: string
        attributes: 
          $ref: '#/components/schemas/Document'
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
    CommentFindAllItem:
      description: A JSON:API document which represents a single document in the list
      properties:
        id:
          description: The JSON:API resource ID `documentId`
          type: string
        type:
          description: The JSON:API resource type `comments`
          type: string
        attributes: 
          $ref: '#/components/schemas/Comment'
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
    DocketFindAllItem:
      description: A JSON:API document which represents a single document in the list
      properties:
        id:
          description: The JSON:API resource ID `docketId`
          type: string
        type:
          description: The JSON:API resource type `dockets`
          type: string
        attributes: 
          $ref: '#/components/schemas/Docket'
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
    AttachmentFindAllItem:
      description: A JSON:API document which represents a single document in the list
      properties:
        id:
          description: The JSON:API resource ID `attachmentId`
          type: string
        type:
          description: The JSON:API resource type `attachments`
          type: string
        attributes: 
          $ref: '#/components/schemas/Attachment'
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
    FindAllResponseMetadata:
      description: A JSON:API document
      properties:
        hasNextPage:
          type: boolean
        hasPreviousPage:
          type: boolean
        numberOfElements:
          type: integer
        pageNumber: 
          type: integer
        pageSize:
          type: integer
        totalElements:
          type: integer
        totalPages:
          type: integer
        firstPage:
          type: boolean
        lastPage:
          type: boolean
    DocumentFindOneResponse:
      description: A JSON:API document which represents a single document
      type: object
      properties:
        id:
          description: The JSON:API resource ID (documentId of the document)
          type: string
        type:
          description: The JSON:API resource type `documents`
          type: string
        attributes: 
          $ref: "#/components/schemas/DocumentDetail"
        relationships:
          $ref: "#/components/schemas/Relationship"
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
        included:
          description: The list of documents where each document is a JSON:API document
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/AttachmentFindAllItem'
    CommentFindOneResponse:
      description: A JSON:API document which represents a single document
      type: object
      properties:
        id:
          description: The JSON:API resource ID (documentId of the comment). DocumentId field is always returned in JSON response. This is an agency configurable field. Each agency has option to configure the format of the field. 
          type: string
        type:
          description: The JSON:API resource type `comments`
          type: string
        attributes: 
          $ref: "#/components/schemas/CommentDetail"
        relationships:
          type: array
          items:
            $ref: "#/components/schemas/Relationship"
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
        included:
          description: The list of documents where each document is a JSON:API document
          type: array
          uniqueItems: true
          items:
            $ref: '#/components/schemas/AttachmentFindAllItem'
    DocketFindOneResponse:
      description: A JSON:API document which represents a single document
      type: object
      properties:
        id:
          description: The JSON:API resource ID (docketId of the docket)
          type: string
        type:
          description: The JSON:API resource type `dockets`
          type: string
        attributes: 
          $ref: "#/components/schemas/DocketDetail"
        links: 
          type: array
          items:
            $ref: '#/components/schemas/SelfLink'
    Relationship:
      description: A single relationship object
      type: object
      properties:
        data:
          $ref: "#/components/schemas/RelationshipToAttachment"
        links:
          $ref: "#/components/schemas/RelationshipLinks"
      additionalProperties: false
    RelationshipToAttachment:
      description: >-
        An array of attachment objects as relationship resources.
      type: array
      items:
        type: object
        properties:
          type:
            type: string
          id:
            type: string
    RelationshipLinks:
      description: >-
        Relationship links to other related resources (`attachments`)
      type: object
      properties:
        self:
          $ref: "#/components/schemas/Link"
        related:
          $ref: "#/components/schemas/Link"
      additionalProperties: false
    SelfLink:
      description: Link to self
      type: object
      properties:
        self:
          $ref: "#/components/schemas/Link"
    Link:
      description: A string containing the link URL.
      type: string
      format: uri-reference
      uniqueItems: true
    JSONResourcePostRequestObject:
      description: A JSON:API document which represents a single document being posted
      type: object
      properties:
        type:
          description: The JSON:API resource type `comments`
          type: string
        attributes: 
          type: object
          oneOf:
            - $ref: "#/components/schemas/IndividualComment"
            - $ref: "#/components/schemas/OrganizationComment"
            - $ref: "#/components/schemas/AnonymousComment"
    JSONResourcePostResponseObject:
      description: A JSON:API document which represents the response from post
      type: object
      properties:
        id:
          description: The comment tracking number
          type: string
        type:
          description: The JSON:API resource type `comments`
          type: string
        attributes:
          $ref: "#/components/schemas/CommentPostResponse"
    JSONError:
      description: A JSON:API document
      type: object
      properties:
        errors:
          description: List of JSON:API Error
          type: array
          items:
            $ref: "#/components/schemas/Error" 
    #Regulations.gov documentation        
    DocumentType:
      type: string
      description: type of document. This field is always returned in JSON response
      enum:
        - Notice
        - Rule
        - Proposed Rule
        - Supporting & Related Material
        - Other
    DocketType:
      type: string
      description: the type of docket
      enum:
        - Rulemaking
        - Nonrulemaking 
    SubmitterType:
      type: string
      description: the submitter type
      enum:
        - Anonymous
        - Individual
        - Organization
    FileFormat:
      type: object
      properties: 
        fileUrl:
          type: string
          description: URL of the file on S3
        format:
          type: string
          description: The format of the file such as `pdf`
        size:
          type: integer
          description: The file size
    #Relationship model for attachments
    Attachment:
      type: object
      properties:
        agencyNote:
          type: string
          description: The note by agency
        authors:
          type: array
          items:
            type: string
          description: The individual, organization, or group of collaborators that contributed to the creation of the attachment.
        docAbstract:
          type: string
          description: The detailed description of the attachment.
        docOrder:
          type: integer
          description: The order of the attachment
        fileFormats:
          type: array
          description: list of file formats
          items:
              $ref: '#/components/schemas/FileFormat'
        modifyDate:
          type: string
          format: date-time
          description: The date when the attachment was last modified.
        publication:
          type: string
          description: The publication date
        restrictReason:
          type: string
          description: If the attachment is restricted, this field will state the reason.
        restrictReasonType:
          type: string
          description: If the attachment is restricted, this field will state the type of restriction.
        title:
          type: string
          description: The formal title of the attachment
    #Search components     
    Document:
      type: object
      properties: 
        agencyId:
          type: string
          description: The acronym used to abbreviate the name of the agency associated with the document.
        commentEndDate:
          type: string
          nullable: true
          format: date-time
          description: The date that closes the period when public comments may be submitted on the document.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        commentStartDate:
          type: string
          nullable: true
          format: date-time
          description: The date that begins the period when public comments may be submitted on the document.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        docketId:
          type: string
          description: The ID of the docket to which the document corresponds.
        documentType:
          $ref: '#/components/schemas/DocumentType'
        frDocNum:
          type: string
          description: The federal register document number of the document.
        highlightedContent:
          type: string
          nullable: true
          description: Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.
        lastModifiedDate:
          type: string
          format: date-time
          description: The date document was last modified in the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        objectId:
          type: string
          description: The internal ID of the document in our system.
        openForComment:
          type: boolean
          description: Conveys if the document is open for comment
        postedDate:
          type: string
          description: The date that the document was posted by the agency to the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        subtype:
          type: string
          nullable: true
          description: An agency-specific attribute to further categorize a document beyond the type (`documentType`).
        title:
          type: string
          description: The formal title of the document.
        withdrawn:
          type: boolean
          description: Conveys if the document is withdrawn
    Comment:
      type: object
      properties:
        agencyId:
          type: string
          description: The acronym used to abbreviate the name of the agency associated with the document.
        documentType:
          $ref: '#/components/schemas/DocumentType'
        highlightedContent:
          type: string
          nullable: true
          description: Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.
        lastModifiedDate:
          type: string
          format: date-time
          description: The date comment was last modified in the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        objectId:
          type: string
          description: The internal ID of the comment in our system.
        postedDate:
          type: string
          description: The date that the document was posted by the agency to the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        title:
          type: string
          description: The formal title of the document.
        withdrawn:
          type: boolean
          description: Conveys if the document is withdrawn
    Docket:
      type: object
      properties:
        agencyId:
          type: string
          description: The acronym used to abbreviate the name of the agency associated with the docket.
        docketType:
          $ref: '#/components/schemas/DocketType'
        highlightedContent:
          type: string
          nullable: true
          description: Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.
        lastModifiedDate:
          type: string
          format: date-time
          description: The date docket was last modified in the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        objectId:
          type: string
          description: The internal ID of the docket in our system.
        title:
          type: string
          description: The formal title of the docket.
    #Detail components
    BasicDetailModel:
      type: object
      properties:
        address1:
          type: string
          nullable: true
          description: The first line of the submitter's address. 
        address2:
          type: string
          nullable: true
          description: The second line of the submitter's address.
        agencyId:
          type: string
          description: The acronym used to abbreviate the name of the agency associated with the document. This field is always returned in JSON response.
        city:
          type: string
          nullable: true
          description: The city associated with the submitter's address. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        category:
          type: string
          nullable: true
          description: An agency-specific category allowing agencies to group comments according to their type.
        comment:
          type: string
          description: The comment text associated with the comment submission. This field is always returned in JSON response.
        country:
          type: string
          nullable: true
          description: The country associated with the submitter's address. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        docAbstract:
          type: string
          description: The detailed description of the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        docketId:
          type: string
          description: The ID of the docket to which the document corresponds. This field is always returned in JSON response. 
        documentType:
          $ref: '#/components/schemas/DocumentType'
        email:
          type: string
          nullable: true
          description: The submitter's e-mail address.
        fax:
          type: string
          nullable: true
          description: The submitter's fax number.
        field1:
          type: string
          nullable: true
          description: An agency-specific field used for storing additional data with the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        field2:
          type: string
          nullable: true
          description: An agency-specific field used for storing additional data with the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        fileFormats:
          type: array
          description: list of file formats
          items:
            $ref: '#/components/schemas/FileFormat'
        firstName:
          type: string
          nullable: true
          description: The submitter's first name. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        govAgency:
          type: string
          nullable: true
          description: The name of the government agency that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        govAgencyType:
          type: string
          nullable: true
          description: The type of government agency that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        lastName:
          type: string
          nullable: true
          description: The submitter's last name. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        legacyId:
          type: string
          nullable: true
          description: An agency-specific identifier that was given to the document in the legacy system. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        modifyDate:
          type: string
          format: date-time
          description: The date when the document was last modified.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        objectId:
          type: string
          description: The internal ID of the document in our system.
        openForComment:
          type: boolean
          description: Conveys if the document is open for commenting.
        organization:
          type: string
          nullable: true
          description: The organization that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        originalDocumentId:
          type: string
          description: The document ID that was assigned when first entered into the system should a change occur that requires a new document ID to be assigned.
        pageCount:
          type: string
          nullable: true
          description: Conveys the number of pages contained in the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        phone:
          type: string
          nullable: true
          description: The submitter's phone number.
        postedDate:
          type: string
          format: date-time
          description: The date that the document was posted by the agency to the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`. This field is always returned in JSON response.
        postmarkDate:
          type: string
          nullable: true
          format: date-time
          description: The postmark date of a document that was sent by mail.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        reasonWithdrawn:
          type: string
          nullable: true
          description: If the document is withdrawn, this field will state the reason. If data exists, it is always returned in JSON response.
        receiveDate:
          type: string
          format: date-time
          description: The date that the document was received by the agency to the system.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2018-06-29T04:00:00Z`. This field is always returned in JSON response.
        restrictReason:
          type: string
          description: If the document is restricted, this field will state the reason. If data exists, it is always returned in JSON response.
        restrictReasonType:
          type: string
          description: If the document is restricted, this field will state the type of restriction. If data exists, it is always returned in JSON response.
        stateProvinceRegion:
          type: string
          nullable: true
          description: The submitter's state,province or region. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        subtype:
          type: string
          nullable: true
          description: An agency-specific attribute to further categorize a document beyond the documentType. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
        title:
          type: string
          description: The formal title of the document. This field is always returned in JSON response.
        trackingNbr:
          type: string
          description: The tracking number of the submission. This field is always returned in JSON response.
        withdrawn:
          type: boolean
          description: Conveys if the document is withdrawn. This field is always returned in JSON response.
        zip:
          type: string
          description: The zip associated with the submitter's address. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.
    DocumentDetail:
      allOf:     # Combines the BasicDetailModel and the inline model
        - $ref: '#/components/schemas/BasicDetailModel'
        - type: object
          required:
            - documentId
          properties: 
            additionalRins:
              type: array
              nullable: true
              items:
                type: string
              description: One or more Regulatory Information Numbers (RINs) to which the document relates.
            allowLateComments:
              type: boolean
              description: Indicates whether the owning agency will accept comments on the document after the due date.
            authorDate:
              type: string
              nullable: true
              format: date-time
              description: The date that the authors wrote or published the document.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
            authors:
              type: array
              nullable: true
              items:
                type: string
              description: The individual, organization, or group of collaborators that contributed to the creation of the document.
            cfrPart:
              type: string
              nullable: true
              description: The Code of Federal Regulations (CFR) Citation applicable to the document.
            commentEndDate:
              type: string
              nullable: true
              format: date-time
              description: The date that closes the period when public comments may be submitted on the document.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
            commentStartDate:
              type: string
              nullable: true
              format: date-time
              description: The date that begins the period when public comments may be submitted on the document.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
            effectiveDate:
              type: string
              nullable: true
              format: date-time
              description: The date the document is put into effect.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
            exhibitLocation:
              type: string
              nullable: true
              description: The physical location of an exhibit to which a document refers.
            exhibitType:
              type: string
              nullable: true
              description: The type of exhibit to which a document refers.
            frDocNum:
              type: string
              nullable: true
              description: The unique identifier of a document originating in the [Federal Register](https://www.federalregister.gov/).
            frVolNum:
              type: string
              nullable: true
              description: The [Federal Register](https://www.federalregister.gov/) volume number where the document was published.
            implementationDate:
              type: string
              nullable: true
              format: date-time
              description: The date the document is to be implemented.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
            openForComment:
              type: boolean
              description: Conveys if a document is open for comment.
            media:
              type: string
              nullable: true
              description: The media in which the document is stored.
            ombApproval:
              type: string
              nullable: true
              description: The control number assigned when approval is given by the Office of Management and Budget (OMB) in accordance with the Paperwork Reduction Act (PRA).
            paperLength:
              type: integer
              description: When the document is in paper format, indicates the length of the paper.
            paperWidth:
              type: integer
              description: When the document is in paper format, indicates the width of the paper.
            regWriterInstruction:
              type: string
              nullable: true
              description: Additional instructions provided by the writer of the regulation.
            sourceCitation:
              type: string
              nullable: true
              description: The citation for the source that published the document.
            startEndPage:
              type: string
              nullable: true
              description: The starting and ending pages where the document was published.
            subject:
              type: string
              nullable: true
              description: The subject of the document.
            topics:
              type: array
              nullable: true
              items:
                type: string
              description: The principal topics to which the document pertains.
    CommentDetail: 
      allOf:     # Combines the BasicDetailModel and the inline model
        - $ref: '#/components/schemas/BasicDetailModel'
        - type: object
          required:
            - documentId
          properties: 
            commentOnDocumentId:
              type: string
              description: documentId of the parent document. This field is always returned in JSON response.
            duplicateComments:
              type: integer
              description: Number of duplicate comments
    DocketDetail:
      type: object
      properties:
        agencyId:
          type: string
          description: The acronym used to abbreviate the name of the agency associated with the docket.
        category:
          type: string
          nullable: true
          description: Agency specific docket category providing regulatory action details, status, and the agency program and or office.
        dkAbstract:
          type: string
          description: The detailed description of the docket.
        docketType:
          $ref: '#/components/schemas/DocketType'
        effectiveDate:
          type: string
          format: date-time
          description: The date the docket is put into effect.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        field1:
          type: string
          nullable: true
          description: An agency-specific field used for storing additional data with the docket.
        field2:
          type: string
          nullable: true
          description: An agency-specific field used for storing additional data with the docket.
        generic:
          type: string
          nullable: true
          description: An agency-specific field used for storing additional data with the docket.
        keywords:
          type: array
          nullable: true
          items:
            type: string
            description: Agency selected keywords associated with a docket to improve its searchability by the public.
        legacyId:
          type: string
          nullable: true
          description: An agency-specific identifier that was given to the docket in the legacy system.
        modifyDate:
          type: string
          format: date-time
          description: The date when the docket was last modified.<br/><br/>The date is formatted as ISO 8601 with an offset such as `2019-01-20T13:15:45Z`.
        objectId:
          type: string
          description: The internal ID of the document in our system.
        organization:
          type: string
          nullable: true
          description: Identifies docket's (a regulatory action) orginating agency and/or department.
        petitionNbr:
          type: string
          nullable: true
          description: Agency specific identifier associated with a docket.
        program:
          type: string
          nullable: true
          description: The agency specific program associated with the docket.
        rin:
          type: string
          nullable: true
          description: OMB issued Regulation Identifier Number (RIN) uniquely identifies a docket and its documents.
        shortTitle:
          type: string
          nullable: true
          description: A combination of letters and or numbers assigned to an agency's regulatory action for purposes of brevity.
        subType:
          type: string
          nullable: true
          description: This agency specific attribute characterizes a docket (regulatory action) beyond its assigned docket type, e.g., Rulemaking.
        subType2:
          type: string
          nullable: true
          description: This agency specific attribute characterizes a docket (regulatory action) beyond the designated docket subtype.
        title:
          type: string
          description: A name or descriptive heading given to an agency's docket.
    #Comment Submission Related components
    BaseCommentPayload:
      type: object
      required:
        - comment
        - commentOnDocumentId
        - submissionType #user should set submission Type to API
      properties:
        category:
          type: string
          description: An agency-specific category allowing agencies to group comments according to their type.
        comment:
          type: string
          maxLength: 5000
          description: The comment text
        commentOnDocumentId:
          type: string
          description: documentId of the parent document
        email:
          type: string
          maxLength: 100
          description: The email address to receive email receipt for the commenrt
        files:
          type: array
          items:
            type: string
            description: The names of the files submitted with the submission
        numItemsReceived:
          type: integer
          description: The number of items included in the submission          
        sendEmailReceipt:
          type: boolean
          description: Conveys if the user would like to receive an email receipt for the comment
        submissionKey:
          type: string
          description: The unique identifier associated with the submission
        submissionType:
          type: string
          description: The submitter type - Its always going to be `API` for comments submitted via API 
    IndividualComment:
      allOf:     # Combines the BasicCommentPayLoad and the inline model
        - $ref: '#/components/schemas/BaseCommentPayload'
        - type: object
          required:
            - submitterType
            - firstName
            - lastName
          properties:
            city:
              type: string
              maxLength: 50
              description: The city associated with the submitter's address.
            country:
              type: string
              maxLength: 50
              description: The country associated with the submitter's address.
            firstName:
              type: string
              maxLength: 25
              description: The submitter's first name.
            lastName:
              type: string
              maxLength: 25
              description: The submitter's last name.
            phone:
              type: string
              maxLength: 50
              description: The submitter's phone number.
            stateProvinceRegion:
              type: string
              maxLength: 50
              description: The email associated with the submitter's address.
            submitterType: #submitter type should be set to Individual
              $ref: '#/components/schemas/SubmitterType'
            zip:
              type: string
              maxLength: 10
              description: The zip associated with the submitter's address.
    OrganizationComment: 
      allOf:     # Combines the BasicCommentPayLoad and the inline model
        - $ref: '#/components/schemas/BaseCommentPayload'
        - type: object
          required:
            - submitterType
            - organization
            - organizationType
          properties:
            organization:
              type: string
              maxLength: 120
              description: The organization that the submitter represents.          
            organizationType:
              type: string
              description: The agency specific organization type that the submitter represents.          
            submitterType: #submitter type should be set to Organization
              $ref: '#/components/schemas/SubmitterType'
    AnonymousComment: 
      allOf:     # Combines the BasicCommentPayLoad and the inline model
        - $ref: '#/components/schemas/BaseCommentPayload'
        - type: object
          required:
            - submitterType
          properties: 
            submitterType: #submitter type should be set to Anonymous
              $ref: '#/components/schemas/SubmitterType'
    CommentPostResponse:
      allOf:
        - oneOf:     # Returns the created comment
          - $ref: '#/components/schemas/IndividualComment'
          - $ref: '#/components/schemas/OrganizationComment'
          - $ref: '#/components/schemas/AnonymousComment'
        - type: object
          properties:
            numItemsReceived:
              type: integer
              description: The number of items included in the submission          
            receiveDate: 
              type: string
              description: The date comment was received.
    Error:
      type: object
      properties:
        status:
          type: integer #http status code
        title:
          type: string
        detail:
          type: string

</regulations_gov_open_api_specification>

<regulations_gov_api_documentation>
## Overview
When Congress passes laws, federal agencies implement those laws through regulations. These regulations vary in subject, but include everything from ensuring water is safe to drink to setting health care standards. Regulations.gov is the place where users can find and comment on regulations. The APIs allow for users to find creative ways to present regulatory data. 

## API Description
Regulations.gov offers a GET API for documents, comments, and dockets and a POST API for comments. These endpoints can be used for searching document, comments and dockets, and posting a comment.

### Searching for documents
You can search for a list of documents based on the criteria passed by using the endpoint /v4/documents. The search operation supports full text keyword searches and filtering based on a number of available parameters.

### Detailed information for a single document
In order to obtain more details about a single document, you can use the endpoint /v4/documents/{documentId}. A document is defined by one of the following types: Proposed Rule, Rule, Supporting & Related, or Other. Each document type has its own set of attributes, which vary based on the Agency posting the document. Another defining characteristic is if the document is part of a Rulemaking or Nonrulemaking Docket.

You can choose to include attachments using include parameter. Attachments are not included by default.

### Searching for comments
You can search for a list of comments based on the criteria passed by using the endpoint /v4/comments. The search operation supports full text keyword searches and filtering based on a number of available parameters.

### Detailed information for a single comment
In order to obtain more details about a single comment, you can use the endpoint /v4/comments/{commentId}. Each comment has its own set of attributes, which vary based on the Agency posting the comment. Another defining characteristic is if the comment is part of a Rulemaking or Nonrulemaking Docket.

You can choose to include attachments using include parameter. Attachments are not included by default.

### Searching for dockets
A docket is an organizational folder containing multiple documents. Dockets can be searched using the endpoint: /v4/dockets.

### Detailed information for a single docket
In order to obtain more details about a single docket, you can use the endpoint /v4/dockets/{docketId}. Each docket has its own set of attributes, which vary based on the Agency posting the docket. Another defining characteristic is if the docket is a Rulemaking or a Nonrulemaking Docket

### Posting a comment
User can post a comment using the endpoint /v4/comments. User can post the comment using one of the following submitter types:

Individual
Organization
Anonymous
If user would like to attach files with their submission, user can get a presigned url for the amazon s3 bucket using the endpoint /v4/file-upload-urls

A submissionKey can be retrieved using /v4/submission-keys endpoint.

submissionType should be set to API.

## Data Limitations
A recent GAO report expressed concerns over whether comment data is fully described to the public, including any limitations. Various aspects of the commenting process can create limitations for certain external users of public comment data and some data fields are managed solely by agencies. For agency-specific commenting practices, contact eRulemaking@gsa.gov. The Open API Specification document has been updated with information on agency configurable fields. For convenience, the data is also provided below in a concise format:

### List of fields that are always publicly viewable on a comment
Here is the list of fields that is always available in the JSON response for a comment:

agencyId
comment
commentOnId
docketId
documentId - This field is returned as an Id of the document in the JSON response.
documentType
postedDate
receiveDate
restrictReason - if restrictReasonType is set to “Other”
restrictReasonType - if the document is restricted
reasonWithdrawn - if the comment has been withdrawn
title
trackingNbr
withdrawn

### List of agency configurable comment fields
Agency configured fields can be updated by an agency at any point in time and made accessible or inaccessible in the JSON response of a comment. Here is the list of these fields:

city
country
docAbstract
firstName
govAgency
govAgencyType
lastName
legacyId
organization
pageCount
postmarkDate
stateProvinceRegion
subtype
zip

### List of fields that are never publicly viewable on a comment
originalDocumentId
address1
address2
email
phone
fax

## Post Comment API Validation

### Common Validations for all comments
commentOnDocumentId, comment and submissionType are required fields.
If sendEmailReceipt is true, email field is required.
An emoji is not a valid character.
If a field has a maximum length requirement, the requirement is applied to both, the number of characters and the number of bytes.
submitterType field must be one of these allowed values: ANONYMOUS, INDIVIDUAL, ORGANIZATION.
submissionType field must be set to API.
Field value for comment must be less than or equals to 5000 characters/bytes.
Field value for email must be less than or equals to 100 characters/bytes.

### Individual Comment Validations
firstName and lastName are required fields.
Field value for firstName and lastName must be less than or equals to 25 characters/bytes.
Field value for city, stateProvinceRegion, phone and country must be less than or equals to 50 characters/bytes.
Field value for zip field must have less than or equals to 10 characters/bytes.

### Organization Comment Validations
organization and organizationType are required fields.
Field value for organization field must have less than or equals to 120 characters/bytes.

## Examples

### Searching for documents
Here are few example queries for searching documents:

Search for term water:
https://api.regulations.gov/v4/documents?filter[searchTerm]=water&api_key=DEMO_KEY
Filter documents by a specific date:
https://api.regulations.gov/v4/documents?filter[postedDate]=2020-09-01&api_key=DEMO_KEY
Filter documents by a date range:
https://api.regulations.gov/v4/documents?filter[postedDate][ge]=2020-09-01&filter[postedDate][le]=2020-09-01&api_key=DEMO_KEY
Search for a documentId:
https://api.regulations.gov/v4/documents?filter[searchTerm]=FDA-2009-N-0501-0012&api_key=DEMO_KEY
Sort documents by posted date in asc:
https://api.regulations.gov/v4/documents?sort=postedDate&api_key=DEMO_KEY
Sort documents by posted date in desc:
https://api.regulations.gov/v4/documents?sort=-postedDate&api_key=DEMO_KEY
Detailed information for a single document
There are few ways a user can query documents endpoint to retrieve detailed information for a document.

Get document details without attachments:
https://api.regulations.gov/v4/documents/FDA-2009-N-0501-0012?api_key=DEMO_KEY
Get document details with attachments:
https://api.regulations.gov/v4/documents/FDA-2009-N-0501-0012?include=attachments&api_key=DEMO_KEY
Searching for comments
Here are few example queries for searching comments:

Search for term water:
https://api.regulations.gov/v4/comments?filter[searchTerm]=water&api_key=DEMO_KEY
Filter comments by a specific date:
https://api.regulations.gov/v4/comments?filter[postedDate]=2020-09-01&api_key=DEMO_KEY
Filter comments by a date range:
https://api.regulations.gov/v4/comments?filter[postedDate][ge]=2020-09-01&filter[postedDate][le]=2020-09-01&api_key=DEMO_KEY
Search for a commentId:
https://api.regulations.gov/v4/comments?filter[searchTerm]=HHS-OCR-2018-0002-5313&api_key=DEMO_KEY
Sort comments by posted date in asc:
https://api.regulations.gov/v4/comments?sort=postedDate&api_key=DEMO_KEY
Sort comments by posted date in desc:
https://api.regulations.gov/v4/comments?sort=-postedDate&api_key=DEMO_KEY
Retrieve all comments for a docket where number of comments is less than 5000:

Step 1: Get all documents for the docketId FAA-2018-1084:
https://api.regulations.gov/v4/documents?filter[docketId]=FAA-2018-1084&api_key=DEMO_KEY
It returns two documents, FAA-2018-1084-0001 and FAA-2018-1084-0002. Each document metadata includes an objectId attribute.

Step 2: Get all comments for each document using objectId:
https://api.regulations.gov/v4/comments?filter[commentOnId]=0900006483a6cba3&api_key=DEMO_KEY
The above request returns a list of comments for document FAA-2018-1084-0001.

Note: Step 2 should be repeated for FAA-2018-1084-0002 in the above example.

Retrieve all comments for a docket where number of comments is greater than 5000:

Step 1: Get all documents for the docketId EOIR-2020-0003:
https://api.regulations.gov/v4/documents?filter[docketId]=EOIR-2020-0003&api_key=DEMO_KEY
The above query returns five documents where four documents are Supporting & Related Material documents and one document is a Proposed Rule. Response for the above request includes an attribute objectId for each document and its set to 09000064846eebaf for the Proposed Rule, EOIR-2020-0003-0001.

Step 2: Get all comments for each document using objectId:
https://api.regulations.gov/v4/comments?filter[commentOnId]=09000064846eebaf&api_key=DEMO_KEY
The above request returns a list of comments for document EOIR-2020-0003-0001, the only Proposed Rule in the docket. totalElements under meta attribute shows that this document has total 88,061 comments.

Note: Step 2 should be repeated for each document.

Step 3: Page through the first set of 5000 documents:
https://api.regulations.gov/v4/comments?filter[commentOnId]=09000064846eebaf&page[size]=250&page[number]=N&sort=lastModifiedDate,documentId&api_key=DEMO_KEY
The first 5000 documents can be retrieved using the query above and paging through the results where N is the page number between 1 and 20. Please note we are sorting the results by lastModifiedDate to ensure we can filter our data by lastModifiedDate later. On the last page of this set, please note the lastModifiedDate of the last document. In our case, EOIR-2020-0003-5548 is the last document on page 20 and the lastModifiedDate attribute of the document is 2020-08-10T15:58:52Z. We will be filtering the data in the next step using this date.

Step 4: Page through the next set of 5000 documents:
https://api.regulations.gov/v4/comments?filter[commentOnId]=09000064846eebaf&filter[lastModifiedDate][ge]=2020-08-10 11:58:52&page[size]=250&page[number]=N&sort=lastModifiedDate,documentId&api_key=DEMO_KEY
The next 5000 documents can be retrieved using the query above and paging through the results where N is the page number between 1 and 20.

The lastModifiedDate attribute of the last document in the first set (Step 3) was 2020-08-10T15:58:52Z. This date translates to 2020-08-10 11:58:52 in Eastern time. Running the above query should return all documents where lastModifiedDate is greater than or equal to 2020-08-10T15:58:52Z. Its important to note that we are running a “greater than or equal to” query to ensure we do not miss any documents where last modified date is 2020-08-10T15:58:52Z.

On the last page of this set, please note the lastModifiedDate of the last document and repeat.

Note: Step 4 should be repeated for as many times as needed to retrieve all 88,061 comments.

Detailed information for a single comment
There are few ways a user can query comments endpoint to retrieve detailed information for a comment:

Get comment details without attachments:
https://api.regulations.gov/v4/comments/HHS-OCR-2018-0002-5313?api_key=DEMO_KEY
Get comment details with attachments:
https://api.regulations.gov/v4/comments/HHS-OCR-2018-0002-5313?include=attachments&api_key=DEMO_KEY
Searching for dockets
Here are few example queries for searching dockets:

Search for term water:
https://api.regulations.gov/v4/dockets?filter[searchTerm]=water&api_key=DEMO_KEY
Search for a docketId:
https://api.regulations.gov/v4/dockets?filter[searchTerm]=EPA-HQ-OAR-2003-0129&api_key=DEMO_KEY
Filter dockets by multiple agencyIds:
https://api.regulations.gov/v4/dockets?filter[agencyId]=GSA,EPA&api_key=DEMO_KEY
Sort dockets by title in asc order:
https://api.regulations.gov/v4/dockets?sort=title&api_key=DEMO_KEY
Sort dockets by title in desc order:
https://api.regulations.gov/v4/dockets?sort=-title&api_key=DEMO_KEY
Detailed information for a single docket
To retrieve detailed information on a docket, the following query can be used:

https://api.regulations.gov/v4/dockets/EPA-HQ-OAR-2003-0129?api_key=DEMO_KEY
Posting a comment
Posting an anonymous comment without attachment:

POST https://api.regulations.gov/v4/comments {
  "data": {
    "attributes": {
      "commentOnDocumentId":"FDA-2009-N-0501-0012",
      "comment":"test comment",
      "submissionType":"API",
      "submitterType":"ANONYMOUS"
    },
    "type":"comments"
  }
}
Note: No submission key is needed for comments with no attached files.

Posting a comment with attachment:

Step 1: Get a submission key:

POST https://api.regulations.gov/v4/submission-keys {
  "data": {
    "type":"submission-keys"
  }
}
Step 2: Get presigned url for each attachment:

POST https://api.regulations.gov/v4/file-upload-urls {
  "data": {
    "type":"file-upload-urls",
    "attributes": {
      "fileName":"test.jpg",
      "submissionKey":"kex-d31z-fe04",
      "contentType":"image/jpeg"
    }
  }
}
Step 3: Upload binaries to presigned url

Step 4: Submit your comment

POST https://api.regulations.gov/v4/comments {
  "data": {
    "attributes": {
      "commentOnDocumentId":"FDA-2009-N-0501-0012",
      "comment":"test comment",
      "submissionType":"API",
      "submissionKey":"kex-d31z-fe04",
      "submitterType":"ANONYMOUS",
      "files":[ "test.jpg" ]
    },
    "type":"comments"
  }
}
Posting a comment with agency category:

Step 1: Get agency categories for agency:

https://api.regulations.gov/v4/agency-categories?filter[acronym]=FDA&api_key=DEMO_KEY
Step 2: Submit your comment with category:

POST https://api.regulations.gov/v4/comments {
  "data": {
    "attributes": {
      "commentOnDocumentId":"FDA-2009-N-0501-0012",
      "comment":"test comment",
      "submissionType":"API",
      "submitterType":"ANONYMOUS",
      "category":"Academia - E0007"
    },
    "type":"comments"
  }
}
Posting multiple submissions in a single comment:

To post a comment with attachment that carries 5 submissions, user should follow the following steps:

Step 1: Get a submission key:

POST https://api.regulations.gov/v4/submission-keys {
  "data": {
    "type":"submission-keys"
  }
}
Step 2: Get presigned url for the attachment with multiple submissions:

POST https://api.regulations.gov/v4/file-upload-urls {
  "data": {
    "type":"file-upload-urls",
    "attributes": {
      "fileName":"multipleSubmissions.pdf",
      "submissionKey":"kex-d31z-fe04",
      "contentType":"image/jpeg"
    }
  }
}
Step 3: Upload binaries to presigned url

Step 4: Submit your comment with

POST https://api.regulations.gov/v4/comments {
  "data": {
    "attributes": {
      "commentOnDocumentId":"FDA-2009-N-0501-0012",
      "comment":"test comment",
      "submissionType":"API",
      "submissionKey":"kex-d31z-fe04",
      "submitterType":"ANONYMOUS",
      "files":[ "multipleSubmissions.pdf" ],
      "numItemsReceived": 5
    },
    "type":"comments"
  }
}

## Frequently Asked Questions
I am not seeing all fields returned by v3/documents endpoint in v4/documents endpoint. How do I access this information?
Our v3 API had a single search endpoint which returned information about documents, comments and dockets. To streamline our data, we have split our search into three endpoints:

Document Search
Comment Search
Docket Search
Further, some data that could be retrieved using search in v3 has now been moved under details endpoint. For example, you can retrieve RIN for a docket using /dockets/{docketId} endpoint. The rin is not returned by /documents endpoint anymore.

How do I get document status from the new /documents endpoint?
The new /v4/documents carries a withdrawn field. This is a boolean field. If set to true, the document is withdrawn otherwise it’s a posted document.

There are strict pagination limits in v4. How do I retrieve all comments in a docket posted on the same day if the number of comments is greater than 2500?
We have added an example that shows how to retrieve more than 5000 comments on a docket. Please see the example section.

Please note the new parameter lastModifiedDate is in beta and may be removed when we have a permanent bulk download solution available.

I submitted a comment, but I am unable to find it on regs. What happened to my comment?
Comments created via API are not made available in Regulations.gov right away. Agencies need to approve before the newly created comment can be posted out to Regulations.gov.

I am seeing 400 errors from commenting API. What am I doing wrong?
Please make sure you are setting Content-Type to application/vnd.api+json in request header.

What is DEMO_KEY api key?
As indicated by name, DEMO_KEY should only be used for demonstration purposes. We have added this api_key to our examples to make it easier for users to copy/paste the urls. It should not be used for anything more than exploring our APIs.

What is the staging API url?
Users should be able to access our staging API at https://api-staging.regulations.gov. Please use this environment for testing purposes.

I have an API key. How many requests can I make per hour and how do I know I am about to reach my request limit?
Please review https://api.data.gov/docs/rate-limits/ for information on rate limits. Commenting API is restricted to 50 requests per minute with a secondary limit of 500 requests per hour.

Can I request rate limit increases for my keys?
GSA may grant a rate limit increase on the GET keys for an indefinite period. Such requests must establish the need to justify the rate limit increases. Each submission will be reviewed and considered on a case-by-case basis. GSA is unable to increase the rate limits for POST API keys upon requests at this time. However, the current POST API key holders can request one additional key without going through the validation process again.


API Calls
Regulations.gov API
 4.0 
OAS 3.0
Public API for Regulations.gov

Servers

https://api.regulations.gov/v4 - Production endpoint for Regulations.gov API

Authorize
documents


GET
/documents
List of documents

This endpoint returns list of documents

Parameters
Name	Description
filter[agencyId]
string
(query)
'Filters results for the agency acronym specified in the value. Example: ''EPA'''

filter[agencyId]
filter[commentEndDate]
string($date)
(query)
Filters results relative to the comment end date. The value must be formatted as yyyy-MM-dd.

Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used.
ge - greater than or equal
le - less than or equal

filter[commentEndDate]
filter[docketId]
string
(query)
Filters results on the specified docket ID.

filter[docketId]
filter[documentType]
string
(query)
Filters results on the specified document type.

Available values : Notice, Rule, Proposed Rule, Supporting & Related Material, Other


--
filter[frDocNum]
string
(query)
Filters results on the specified frDocNum.

filter[frDocNum]
filter[searchTerm]
string
(query)
Filters results on the given term.

filter[searchTerm]
filter[postedDate]
string($date)
(query)
Filters results relative to the posted date. The value must be formatted as yyyy-MM-dd.

Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used.
ge - greater than or equal
le - less than or equal

filter[postedDate]
filter[lastModifiedDate]
string($date)
(query)
Filters results relative to the last modified date. The value must be formatted as yyyy-MM-dd HH:mm:ss.

Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used.
ge - greater than or equal
le - less than or equal

filter[lastModifiedDate]
filter[subtype]
string
(query)
Filters results on the supplied document subtype

filter[subtype]
filter[withinCommentPeriod]
boolean
(query)
Filters results for documents that are open for comment by setting the value to true.

False is not an acceptable value for this parameter, hence it should be removed when not being used.


--
sort
string
(query)
Sorts the results on the field specified in the value. The default behavior will sort the results in ascending order; to sort in descending order, prepend a minus sign to the value.

Supported values are commentEndDate, postedDate, lastModifiedDate, documentId and title. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.

sort
page[number]
integer
(query)
Specifies the number for the page of results that will be returned from the query.

Acceptable values are numerical between, and including, 1 and 20.

page[number]
page[size]
integer
(query)
Specifies the size per page of results that will be returned from the query.

Acceptable values are numerical between, and including, 5 and 250.

page[size]
Responses
Code	Description	Links
200	
A JSON:API document with the a list of documents

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "data": [
    {
      "id": "string",
      "type": "string",
      "attributes": {
        "agencyId": "string",
        "commentEndDate": "2024-12-18T00:05:46.447Z",
        "commentStartDate": "2024-12-18T00:05:46.447Z",
        "docketId": "string",
        "documentType": "Notice",
        "frDocNum": "string",
        "highlightedContent": "string",
        "lastModifiedDate": "2024-12-18T00:05:46.447Z",
        "objectId": "string",
        "openForComment": true,
        "postedDate": "string",
        "subtype": "string",
        "title": "string",
        "withdrawn": true
      },
      "links": [
        {
          "self": "string"
        }
      ]
    }
  ],
  "meta": {
    "hasNextPage": true,
    "hasPreviousPage": true,
    "numberOfElements": 0,
    "pageNumber": 0,
    "pageSize": 0,
    "totalElements": 0,
    "totalPages": 0,
    "firstPage": true,
    "lastPage": true
  }
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

GET
/documents/{documentId}
Get detailed information for specified documentId

Gets the detailed information of a specific document with the passed documentId.

Parameters
Name	Description
documentId *
string
(path)
ID of document to return

documentId
include
string
(query)
resources to include

Example : attachments

attachments
Responses
Code	Description	Links
200	
successful operation

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "id": "string",
  "type": "string",
  "attributes": {
    "address1": "string",
    "address2": "string",
    "agencyId": "string",
    "city": "string",
    "category": "string",
    "comment": "string",
    "country": "string",
    "docAbstract": "string",
    "docketId": "string",
    "documentType": "Notice",
    "email": "string",
    "fax": "string",
    "field1": "string",
    "field2": "string",
    "fileFormats": [
      {
        "fileUrl": "string",
        "format": "string",
        "size": 0
      }
    ],
    "firstName": "string",
    "govAgency": "string",
    "govAgencyType": "string",
    "lastName": "string",
    "legacyId": "string",
    "modifyDate": "2024-12-18T00:05:46.450Z",
    "objectId": "string",
    "openForComment": true,
    "organization": "string",
    "originalDocumentId": "string",
    "pageCount": "string",
    "phone": "string",
    "postedDate": "2024-12-18T00:05:46.450Z",
    "postmarkDate": "2024-12-18T00:05:46.450Z",
    "reasonWithdrawn": "string",
    "receiveDate": "2024-12-18T00:05:46.450Z",
    "restrictReason": "string",
    "restrictReasonType": "string",
    "stateProvinceRegion": "string",
    "subtype": "string",
    "title": "string",
    "trackingNbr": "string",
    "withdrawn": true,
    "zip": "string",
    "additionalRins": [
      "string"
    ],
    "allowLateComments": true,
    "authorDate": "2024-12-18T00:05:46.450Z",
    "authors": [
      "string"
    ],
    "cfrPart": "string",
    "commentEndDate": "2024-12-18T00:05:46.450Z",
    "commentStartDate": "2024-12-18T00:05:46.450Z",
    "effectiveDate": "2024-12-18T00:05:46.450Z",
    "exhibitLocation": "string",
    "exhibitType": "string",
    "frDocNum": "string",
    "frVolNum": "string",
    "implementationDate": "2024-12-18T00:05:46.450Z",
    "media": "string",
    "ombApproval": "string",
    "paperLength": 0,
    "paperWidth": 0,
    "regWriterInstruction": "string",
    "sourceCitation": "string",
    "startEndPage": "string",
    "subject": "string",
    "topics": [
      "string"
    ]
  },
  "relationships": {
    "data": [
      {
        "type": "string",
        "id": "string"
      }
    ],
    "links": {
      "self": "string",
      "related": "string"
    }
  },
  "links": [
    {
      "self": "string"
    }
  ],
  "included": [
    {
      "id": "string",
      "type": "string",
      "attributes": {
        "agencyNote": "string",
        "authors": [
          "string"
        ],
        "docAbstract": "string",
        "docOrder": 0,
        "fileFormats": [
          {
            "fileUrl": "string",
            "format": "string",
            "size": 0
          }
        ],
        "modifyDate": "2024-12-18T00:05:46.450Z",
        "publication": "string",
        "restrictReason": "string",
        "restrictReasonType": "string",
        "title": "string"
      },
      "links": [
        {
          "self": "string"
        }
      ]
    }
  ]
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
404	
Document not found

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
comments


GET
/comments
List of comments

This endpoint returns list of comments

Parameters
Name	Description
filter[agencyId]
string
(query)
'Filters results for the agency acronym specified in the value. Example: ''EPA'''

filter[agencyId]
filter[searchTerm]
string
(query)
Filters results on the given term.

filter[searchTerm]
filter[postedDate]
string($date)
(query)
Filters results relative to the posted date. The value must be formatted as yyyy-MM-dd.

Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used.
ge - greater than or equal
le - less than or equal

filter[postedDate]
filter[lastModifiedDate]
string($date)
(query)
Filters results relative to the last modified date. The value must be formatted as yyyy-MM-dd HH:mm:ss.

Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used.
ge - greater than or equal
le - less than or equal

filter[lastModifiedDate]
filter[commentOnId]
string
(query)
Filters results on the supplied commentOnId

filter[commentOnId]
sort
string
(query)
Sorts the results on the field specified in the value. The default behavior will sort the results in ascending order; to sort in descending order, prepend a minus sign to the value.

The only supported values are postedDate, lastModifiedDate and documentId. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.

sort
page[number]
integer
(query)
Specifies the number for the page of results that will be returned from the query.

Acceptable values are numerical between, and including, 1 and 20.

page[number]
page[size]
integer
(query)
Specifies the size per page of results that will be returned from the query.

Acceptable values are numerical between, and including, 5 and 250.

page[size]
Responses
Code	Description	Links
200	
A JSON:API document with the a list of comments

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "data": [
    {
      "id": "string",
      "type": "string",
      "attributes": {
        "agencyId": "string",
        "documentType": "Notice",
        "highlightedContent": "string",
        "lastModifiedDate": "2024-12-18T00:05:46.454Z",
        "objectId": "string",
        "postedDate": "string",
        "title": "string",
        "withdrawn": true
      },
      "links": [
        {
          "self": "string"
        }
      ]
    }
  ],
  "meta": {
    "hasNextPage": true,
    "hasPreviousPage": true,
    "numberOfElements": 0,
    "pageNumber": 0,
    "pageSize": 0,
    "totalElements": 0,
    "totalPages": 0,
    "firstPage": true,
    "lastPage": true
  }
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

POST
/comments
Creates a new comment.

Parameters
No parameters

Request body

application/vnd.api+json
A JSON object containing comment information

Example Value
Schema
{
  "type": "string",
  "attributes": {
    "category": "string",
    "comment": "string",
    "commentOnDocumentId": "string",
    "email": "string",
    "files": [
      "string"
    ],
    "numItemsReceived": 0,
    "sendEmailReceipt": true,
    "submissionKey": "string",
    "submissionType": "string",
    "city": "string",
    "country": "string",
    "firstName": "string",
    "lastName": "string",
    "phone": "string",
    "stateProvinceRegion": "string",
    "submitterType": "Anonymous",
    "zip": "string"
  }
}
Responses
Code	Description	Links
201	
Created

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "id": "string",
  "type": "string",
  "attributes": {
    "numItemsReceived": 0,
    "receiveDate": "string",
    "category": "string",
    "comment": "string",
    "commentOnDocumentId": "string",
    "email": "string",
    "files": [
      "string"
    ],
    "sendEmailReceipt": true,
    "submissionKey": "string",
    "submissionType": "string",
    "city": "string",
    "country": "string",
    "firstName": "string",
    "lastName": "string",
    "phone": "string",
    "stateProvinceRegion": "string",
    "submitterType": "Anonymous",
    "zip": "string"
  }
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
404	
Document not found

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

GET
/comments/{commentId}
Get detailed information for specified commentId

Gets the detailed information of a specific comment with the passed commentId.

Parameters
Name	Description
commentId *
string
(path)
ID of comment to return

commentId
include
string
(query)
resources to include

Example : attachments

attachments
Responses
Code	Description	Links
200	
successful operation

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "id": "string",
  "type": "string",
  "attributes": {
    "address1": "string",
    "address2": "string",
    "agencyId": "string",
    "city": "string",
    "category": "string",
    "comment": "string",
    "country": "string",
    "docAbstract": "string",
    "docketId": "string",
    "documentType": "Notice",
    "email": "string",
    "fax": "string",
    "field1": "string",
    "field2": "string",
    "fileFormats": [
      {
        "fileUrl": "string",
        "format": "string",
        "size": 0
      }
    ],
    "firstName": "string",
    "govAgency": "string",
    "govAgencyType": "string",
    "lastName": "string",
    "legacyId": "string",
    "modifyDate": "2024-12-18T00:05:46.459Z",
    "objectId": "string",
    "openForComment": true,
    "organization": "string",
    "originalDocumentId": "string",
    "pageCount": "string",
    "phone": "string",
    "postedDate": "2024-12-18T00:05:46.459Z",
    "postmarkDate": "2024-12-18T00:05:46.459Z",
    "reasonWithdrawn": "string",
    "receiveDate": "2024-12-18T00:05:46.459Z",
    "restrictReason": "string",
    "restrictReasonType": "string",
    "stateProvinceRegion": "string",
    "subtype": "string",
    "title": "string",
    "trackingNbr": "string",
    "withdrawn": true,
    "zip": "string",
    "commentOnDocumentId": "string",
    "duplicateComments": 0
  },
  "relationships": [
    {
      "data": [
        {
          "type": "string",
          "id": "string"
        }
      ],
      "links": {
        "self": "string",
        "related": "string"
      }
    }
  ],
  "links": [
    {
      "self": "string"
    }
  ],
  "included": [
    {
      "id": "string",
      "type": "string",
      "attributes": {
        "agencyNote": "string",
        "authors": [
          "string"
        ],
        "docAbstract": "string",
        "docOrder": 0,
        "fileFormats": [
          {
            "fileUrl": "string",
            "format": "string",
            "size": 0
          }
        ],
        "modifyDate": "2024-12-18T00:05:46.459Z",
        "publication": "string",
        "restrictReason": "string",
        "restrictReasonType": "string",
        "title": "string"
      },
      "links": [
        {
          "self": "string"
        }
      ]
    }
  ]
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
404	
Document not found

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
dockets


GET
/dockets
List of dockets

This endpoint returns list of dockets

Parameters
Name	Description
filter[agencyId]
string
(query)
'Filters results for the agency acronym specified in the value. Example: ''EPA'''

filter[agencyId]
filter[searchTerm]
string
(query)
Filters results on the given term.

filter[searchTerm]
filter[lastModifiedDate]
string($date)
(query)
Filters results relative to the last modified date. The value must be formatted as yyyy-MM-dd HH:mm:ss.

Omission of a parameter modifier will match results to the exact date provided, otherwise, one of the parameter modifiers below may be used.
ge - greater than or equal
le - less than or equal

filter[lastModifiedDate]
filter[docketType]
string
(query)
Filters results on the specified docket type.

Available values : Rulemaking, Nonrulemaking


--
sort
string
(query)
Sorts the results on the field specified in the value. The default behavior will sort the results in ascending order; to sort in descending order, prepend a minus sign to the value.

The only supported values are title, docketId and lastModifiedDate. Multiple sort options can be passed in as a comma separated list to sort results by multiple fields.

sort
page[number]
integer
(query)
Specifies the number for the page of results that will be returned from the query.

Acceptable values are numerical between, and including, 1 and 20.

page[number]
page[size]
integer
(query)
Specifies the size per page of results that will be returned from the query.

Acceptable values are numerical between, and including, 5 and 250.

page[size]
Responses
Code	Description	Links
200	
A JSON:API document with the a list of dockets

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "data": [
    {
      "id": "string",
      "type": "string",
      "attributes": {
        "agencyId": "string",
        "docketType": "Rulemaking",
        "highlightedContent": "string",
        "lastModifiedDate": "2024-12-18T00:05:46.462Z",
        "objectId": "string",
        "title": "string"
      },
      "links": [
        {
          "self": "string"
        }
      ]
    }
  ],
  "meta": {
    "hasNextPage": true,
    "hasPreviousPage": true,
    "numberOfElements": 0,
    "pageNumber": 0,
    "pageSize": 0,
    "totalElements": 0,
    "totalPages": 0,
    "firstPage": true,
    "lastPage": true
  }
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

GET
/dockets/{docketId}
Get detailed information for specified docketId

Gets the detailed information of a specific docket with the passed docketId.

Parameters
Name	Description
docketId *
string
(path)
ID of docket to return

docketId
Responses
Code	Description	Links
200	
successful operation

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "id": "string",
  "type": "string",
  "attributes": {
    "agencyId": "string",
    "category": "string",
    "dkAbstract": "string",
    "docketType": "Rulemaking",
    "effectiveDate": "2024-12-18T00:05:46.463Z",
    "field1": "string",
    "field2": "string",
    "generic": "string",
    "keywords": [
      "string"
    ],
    "legacyId": "string",
    "modifyDate": "2024-12-18T00:05:46.463Z",
    "objectId": "string",
    "organization": "string",
    "petitionNbr": "string",
    "program": "string",
    "rin": "string",
    "shortTitle": "string",
    "subType": "string",
    "subType2": "string",
    "title": "string"
  },
  "links": [
    {
      "self": "string"
    }
  ]
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
404	
Document not found

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
comment submission utilities


GET
/agency-categories
Returns a list of categories

This endpoint returns list of categories

Parameters
Name	Description
filter[acronym] *
string
(query)
'Filters results for the agency acronym specified in the value. Example: ''EPA'''

filter[acronym]
Responses
Code	Description	Links
200	
List of agency categories

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "data": [
    {
      "default": true,
      "acronym": "string",
      "categories": "string"
    }
  ]
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

POST
/submission-keys
Creates the unique submission key

Parameters
No parameters

Request body

application/vnd.api+json
Example Value
Schema
{
  "data": {
    "type": "submissionKeys"
  }
}
Responses
Code	Description	Links
201	
Created

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "data": {
    "id": "string",
    "type": "submission-keys",
    "links": {
      "self": "string"
    }
  }
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

POST
/file-upload-urls
Creates a presigned url to upload file

Returns a pre-signed URL to upload a file to the S3 bucket

Parameters
No parameters

Request body

application/vnd.api+json
Example Value
Schema
{
  "data": {
    "type": "file-upload-urls",
    "attributes": {
      "submissionKey": "string",
      "fileName": "string",
      "contentType": "string"
    }
  }
}
Responses
Code	Description	Links
201	
Created

Media type

application/vnd.api+json
Controls Accept header.
Example Value
Schema
{
  "data": {
    "id": "string",
    "type": "file-upload-urls",
    "attributes": {
      "submissionKey": "string",
      "fileName": "string",
      "contentType": "string"
    }
  }
}
No links
400	
Validation error

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links
403	
API key is missing or invalid

Media type

application/vnd.api+json
Example Value
Schema
{
  "errors": [
    {
      "status": 0,
      "title": "string",
      "detail": "string"
    }
  ]
}
No links

Schemas
DocumentFindAllResponse{
description:	
A JSON:API document with a list of resources

data	[
uniqueItems: true
The list of documents where each document is a JSON:API document

DocumentFindAllItem{...}]
meta	FindAllResponseMetadata{
description:	
A JSON:API document

hasNextPage	boolean
hasPreviousPage	boolean
numberOfElements	integer
pageNumber	integer
pageSize	integer
totalElements	integer
totalPages	integer
firstPage	boolean
lastPage	boolean
}
}
CommentFindAllResponse{
description:	
A JSON:API document with a list of resources

data	[
uniqueItems: true
The list of comments where each comment is a JSON:API document

CommentFindAllItem{
description:	
A JSON:API document which represents a single document in the list

id	string
The JSON:API resource ID documentId

type	string
The JSON:API resource type comments

attributes	Comment{...}
links	[SelfLink{...}]
}]
meta	FindAllResponseMetadata{
description:	
A JSON:API document

hasNextPage	boolean
hasPreviousPage	boolean
numberOfElements	integer
pageNumber	integer
pageSize	integer
totalElements	integer
totalPages	integer
firstPage	boolean
lastPage	boolean
}
}
DocketFindAllResponse{
description:	
A JSON:API document with a list of resources

data	[
uniqueItems: true
The list of dockets where each docket is a JSON:API document

DocketFindAllItem{
description:	
A JSON:API document which represents a single document in the list

id	string
The JSON:API resource ID docketId

type	string
The JSON:API resource type dockets

attributes	Docket{
agencyId	[...]
docketType	DocketTypestring
the type of docket

Enum:
Array [ 2 ]
highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date docket was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the docket in our system.

title	string
The formal title of the docket.

}
links	[SelfLink{
description:	
Link to self

self	Linkstring($uri-reference)
uniqueItems: true
A string containing the link URL.

}]
}]
meta	FindAllResponseMetadata{
description:	
A JSON:API document

hasNextPage	boolean
hasPreviousPage	boolean
numberOfElements	integer
pageNumber	integer
pageSize	integer
totalElements	integer
totalPages	integer
firstPage	boolean
lastPage	boolean
}
}
DocumentFindAllItem{
description:	
A JSON:API document which represents a single document in the list

id	string
The JSON:API resource ID documentId

type	string
The JSON:API resource type documents

attributes	Document{
agencyId	string
The acronym used to abbreviate the name of the agency associated with the document.

commentEndDate	string($date-time)
nullable: true
The date that closes the period when public comments may be submitted on the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

commentStartDate	string($date-time)
nullable: true
The date that begins the period when public comments may be submitted on the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

docketId	string
The ID of the docket to which the document corresponds.

documentType	DocumentTypestring
type of document. This field is always returned in JSON response

Enum:
[ Notice, Rule, Proposed Rule, Supporting & Related Material, Other ]
frDocNum	[...]
highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date document was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the document in our system.

openForComment	boolean
Conveys if the document is open for comment

postedDate	string
The date that the document was posted by the agency to the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

subtype	string
nullable: true
An agency-specific attribute to further categorize a document beyond the type (documentType).

title	string
The formal title of the document.

withdrawn	boolean
Conveys if the document is withdrawn

}
links	[SelfLink{
description:	
Link to self

self	Linkstring($uri-reference)
uniqueItems: true
A string containing the link URL.

}]
}
CommentFindAllItem{
description:	
A JSON:API document which represents a single document in the list

id	string
The JSON:API resource ID documentId

type	string
The JSON:API resource type comments

attributes	Comment{
agencyId	string
The acronym used to abbreviate the name of the agency associated with the document.

documentType	DocumentTypestring
type of document. This field is always returned in JSON response

Enum:
[ Notice, Rule, Proposed Rule, Supporting & Related Material, Other ]
highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date comment was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the comment in our system.

postedDate	string
The date that the document was posted by the agency to the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

title	string
The formal title of the document.

withdrawn	boolean
Conveys if the document is withdrawn

}
links	[SelfLink{
description:	
Link to self

self	Linkstring($uri-reference)
uniqueItems: true
A string containing the link URL.

}]
}
DocketFindAllItem{
description:	
A JSON:API document which represents a single document in the list

id	string
The JSON:API resource ID docketId

type	string
The JSON:API resource type dockets

attributes	Docket{
agencyId	string
The acronym used to abbreviate the name of the agency associated with the docket.

docketType	DocketTypestring
the type of docket

Enum:
[ Rulemaking, Nonrulemaking ]
highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date docket was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the docket in our system.

title	string
The formal title of the docket.

}
links	[SelfLink{
description:	
Link to self

self	Linkstring($uri-reference)
uniqueItems: true
A string containing the link URL.

}]
}
AttachmentFindAllItem{
description:	
A JSON:API document which represents a single document in the list

id	string
The JSON:API resource ID attachmentId

type	string
The JSON:API resource type attachments

attributes	Attachment{
agencyNote	string
The note by agency

authors	[
The individual, organization, or group of collaborators that contributed to the creation of the attachment.

string]
docAbstract	string
The detailed description of the attachment.

docOrder	integer
The order of the attachment

fileFormats	[
list of file formats

FileFormat{...}]
modifyDate	string($date-time)
The date when the attachment was last modified.

publication	string
The publication date

restrictReason	string
If the attachment is restricted, this field will state the reason.

restrictReasonType	string
If the attachment is restricted, this field will state the type of restriction.

title	string
The formal title of the attachment

}
links	[SelfLink{
description:	
Link to self

self	Linkstring($uri-reference)
uniqueItems: true
A string containing the link URL.

}]
}
FindAllResponseMetadata{
description:	
A JSON:API document

hasNextPage	boolean
hasPreviousPage	boolean
numberOfElements	integer
pageNumber	integer
pageSize	integer
totalElements	integer
totalPages	integer
firstPage	boolean
lastPage	boolean
}
DocumentFindOneResponse{
description:	
A JSON:API document which represents a single document

id	string
The JSON:API resource ID (documentId of the document)

type	string
The JSON:API resource type documents

attributes	DocumentDetail{
address1	string
nullable: true
The first line of the submitter's address.

address2	string
nullable: true
The second line of the submitter's address.

agencyId	string
The acronym used to abbreviate the name of the agency associated with the document. This field is always returned in JSON response.

city	string
nullable: true
The city associated with the submitter's address. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

category	string
nullable: true
An agency-specific category allowing agencies to group comments according to their type.

comment	string
The comment text associated with the comment submission. This field is always returned in JSON response.

country	string
nullable: true
The country associated with the submitter's address. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

docAbstract	string
The detailed description of the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

docketId	string
The ID of the docket to which the document corresponds. This field is always returned in JSON response.

documentType	DocumentType[...]
email	string
nullable: true
The submitter's e-mail address.

fax	string
nullable: true
The submitter's fax number.

field1	string
nullable: true
An agency-specific field used for storing additional data with the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

field2	string
nullable: true
An agency-specific field used for storing additional data with the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

fileFormats	[
list of file formats

FileFormat{...}]
firstName	string
nullable: true
The submitter's first name. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

govAgency	string
nullable: true
The name of the government agency that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

govAgencyType	string
nullable: true
The type of government agency that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

lastName	string
nullable: true
The submitter's last name. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

legacyId	string
nullable: true
An agency-specific identifier that was given to the document in the legacy system. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

modifyDate	string($date-time)
The date when the document was last modified.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the document in our system.

openForComment	boolean
Conveys if a document is open for comment.

organization	string
nullable: true
The organization that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

originalDocumentId	string
The document ID that was assigned when first entered into the system should a change occur that requires a new document ID to be assigned.

pageCount	string
nullable: true
Conveys the number of pages contained in the document. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

phone	string
nullable: true
The submitter's phone number.

postedDate	string($date-time)
The date that the document was posted by the agency to the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z. This field is always returned in JSON response.

postmarkDate	string($date-time)
nullable: true
The postmark date of a document that was sent by mail.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

reasonWithdrawn	string
nullable: true
If the document is withdrawn, this field will state the reason. If data exists, it is always returned in JSON response.

receiveDate	string($date-time)
The date that the document was received by the agency to the system.

The date is formatted as ISO 8601 with an offset such as 2018-06-29T04:00:00Z. This field is always returned in JSON response.

restrictReason	string
If the document is restricted, this field will state the reason. If data exists, it is always returned in JSON response.

restrictReasonType	string
If the document is restricted, this field will state the type of restriction. If data exists, it is always returned in JSON response.

stateProvinceRegion	string
nullable: true
The submitter's state,province or region. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

subtype	string
nullable: true
An agency-specific attribute to further categorize a document beyond the documentType. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

title	string
The formal title of the document. This field is always returned in JSON response.

trackingNbr	string
The tracking number of the submission. This field is always returned in JSON response.

withdrawn	boolean
Conveys if the document is withdrawn. This field is always returned in JSON response.

zip	string
The zip associated with the submitter's address. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

additionalRins	[
nullable: true
One or more Regulatory Information Numbers (RINs) to which the document relates.

string]
allowLateComments	boolean
Indicates whether the owning agency will accept comments on the document after the due date.

authorDate	string($date-time)
nullable: true
The date that the authors wrote or published the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

authors	[
nullable: true
The individual, organization, or group of collaborators that contributed to the creation of the document.

[...]]
cfrPart	string
nullable: true
The Code of Federal Regulations (CFR) Citation applicable to the document.

commentEndDate	string($date-time)
nullable: true
The date that closes the period when public comments may be submitted on the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

commentStartDate	string($date-time)
nullable: true
The date that begins the period when public comments may be submitted on the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

effectiveDate	string($date-time)
nullable: true
The date the document is put into effect.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

exhibitLocation	string
nullable: true
The physical location of an exhibit to which a document refers.

exhibitType	string
nullable: true
The type of exhibit to which a document refers.

frDocNum	string
nullable: true
The unique identifier of a document originating in the Federal Register.

frVolNum	string
nullable: true
The Federal Register volume number where the document was published.

implementationDate	string($date-time)
nullable: true
The date the document is to be implemented.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

media	string
nullable: true
The media in which the document is stored.

ombApproval	string
nullable: true
The control number assigned when approval is given by the Office of Management and Budget (OMB) in accordance with the Paperwork Reduction Act (PRA).

paperLength	integer
When the document is in paper format, indicates the length of the paper.

paperWidth	integer
When the document is in paper format, indicates the width of the paper.

regWriterInstruction	string
nullable: true
Additional instructions provided by the writer of the regulation.

sourceCitation	string
nullable: true
The citation for the source that published the document.

startEndPage	string
nullable: true
The starting and ending pages where the document was published.

subject	string
nullable: true
The subject of the document.

topics	[
nullable: true
The principal topics to which the document pertains.

string]
}
relationships	Relationship{
description:	
A single relationship object

data	RelationshipToAttachment[...]
links	RelationshipLinks{...}
}
links	[SelfLink{
description:	
Link to self

self	Linkstring($uri-reference)
uniqueItems: true
A string containing the link URL.

}]
included	[
uniqueItems: true
The list of documents where each document is a JSON:API document

AttachmentFindAllItem{...}]
}
CommentFindOneResponse
DocketFindOneResponse
Relationship
RelationshipToAttachment
RelationshipLinks
SelfLink
Link
JSONResourcePostRequestObject
JSONResourcePostResponseObject{
description:	
A JSON:API document which represents the response from post

id	[...]
type	string
The JSON:API resource type comments

attributes	CommentPostResponse{
numItemsReceived	integer
The number of items included in the submission

receiveDate	string
The date comment was received.

oneOf ->	
IndividualComment{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[string
The names of the files submitted with the submission

]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

city	string
maxLength: 50
The city associated with the submitter's address.

country	string
maxLength: 50
The country associated with the submitter's address.

firstName*	string
maxLength: 25
The submitter's first name.

lastName*	string
maxLength: 25
The submitter's last name.

phone	string
maxLength: 50
The submitter's phone number.

stateProvinceRegion	string
maxLength: 50
The email associated with the submitter's address.

submitterType*	SubmitterTypestring
the submitter type

Enum:
[ Anonymous, Individual, Organization ]
zip	string
maxLength: 10
The zip associated with the submitter's address.

}
OrganizationComment{...}
AnonymousComment{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[[...]]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

submitterType*	SubmitterTypestring
the submitter type

Enum:
Array [ 3 ]
}
}
}
JSONError{
description:	
A JSON:API document

errors	[
List of JSON:API Error

Error{
status	[...]
title	[...]
detail	[...]
}]
}
DocumentTypestring
type of document. This field is always returned in JSON response

Enum:
[ Notice, Rule, Proposed Rule, Supporting & Related Material, Other ]
DocketTypestring
the type of docket

Enum:
[ Rulemaking, Nonrulemaking ]
SubmitterTypestring
the submitter type

Enum:
[ Anonymous, Individual, Organization ]
FileFormat{
fileUrl	string
URL of the file on S3

format	string
The format of the file such as pdf

size	integer
The file size

}
Attachment
Document{
agencyId	string
The acronym used to abbreviate the name of the agency associated with the document.

commentEndDate	string($date-time)
nullable: true
The date that closes the period when public comments may be submitted on the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

commentStartDate	string($date-time)
nullable: true
The date that begins the period when public comments may be submitted on the document.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

docketId	string
The ID of the docket to which the document corresponds.

documentType	DocumentTypestring
type of document. This field is always returned in JSON response

Enum:
[ Notice, Rule, Proposed Rule, Supporting & Related Material, Other ]
frDocNum	string
The federal register document number of the document.

highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date document was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the document in our system.

openForComment	boolean
Conveys if the document is open for comment

postedDate	string
The date that the document was posted by the agency to the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

subtype	string
nullable: true
An agency-specific attribute to further categorize a document beyond the type (documentType).

title	string
The formal title of the document.

withdrawn	boolean
Conveys if the document is withdrawn

}
Comment{
agencyId	string
The acronym used to abbreviate the name of the agency associated with the document.

documentType	DocumentTypestring
type of document. This field is always returned in JSON response

Enum:
Array [ 5 ]
highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date comment was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the comment in our system.

postedDate	string
The date that the document was posted by the agency to the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

title	string
The formal title of the document.

withdrawn	boolean
Conveys if the document is withdrawn

}
Docket{
agencyId	string
The acronym used to abbreviate the name of the agency associated with the docket.

docketType	DocketTypestring
the type of docket

Enum:
[ Rulemaking, Nonrulemaking ]
highlightedContent	string
nullable: true
Content highlighted by search engine for the searchTerm. Only returned for searches with searchTerm.

lastModifiedDate	string($date-time)
The date docket was last modified in the system.

The date is formatted as ISO 8601 with an offset such as 2019-01-20T13:15:45Z.

objectId	string
The internal ID of the docket in our system.

title	string
The formal title of the docket.

}
BasicDetailModel{
address1	[...]
address2	[...]
agencyId	[...]
city	[...]
category	[...]
comment	[...]
country	[...]
docAbstract	[...]
docketId	[...]
documentType	DocumentType[...]
email	[...]
fax	[...]
field1	[...]
field2	[...]
fileFormats	[...]
firstName	[...]
govAgency	[...]
govAgencyType	[...]
lastName	[...]
legacyId	[...]
modifyDate	[...]
objectId	string
The internal ID of the document in our system.

openForComment	boolean
Conveys if the document is open for commenting.

organization	string
nullable: true
The organization that the submitter represents. This is an agency configurable field. An agency can configure this field to make it not publicly accessible.

originalDocumentId	[...]
pageCount	[...]
phone	[...]
postedDate	[...]
postmarkDate	[...]
reasonWithdrawn	[...]
receiveDate	[...]
restrictReason	[...]
restrictReasonType	[...]
stateProvinceRegion	[...]
subtype	[...]
title	[...]
trackingNbr	[...]
withdrawn	[...]
zip	[...]
}
DocumentDetail
CommentDetail
DocketDetail
BaseCommentPayload
IndividualComment{
allOf ->	
BaseCommentPayload{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[string
The names of the files submitted with the submission

]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

}
{
city	string
maxLength: 50
The city associated with the submitter's address.

country	string
maxLength: 50
The country associated with the submitter's address.

firstName*	string
maxLength: 25
The submitter's first name.

lastName*	string
maxLength: 25
The submitter's last name.

phone	string
maxLength: 50
The submitter's phone number.

stateProvinceRegion	string
maxLength: 50
The email associated with the submitter's address.

submitterType*	SubmitterTypestring
the submitter type

Enum:
[ Anonymous, Individual, Organization ]
zip	string
maxLength: 10
The zip associated with the submitter's address.

}
}
OrganizationComment{
allOf ->	
BaseCommentPayload{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[string
The names of the files submitted with the submission

]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

}
{
organization*	string
maxLength: 120
The organization that the submitter represents.

organizationType*	string
The agency specific organization type that the submitter represents.

submitterType*	SubmitterTypestring
the submitter type

Enum:
[ Anonymous, Individual, Organization ]
}
}
AnonymousComment{
allOf ->	
BaseCommentPayload{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[string
The names of the files submitted with the submission

]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

}
{
submitterType*	SubmitterType[...]
}
}
CommentPostResponse{
allOf ->	
{
oneOf ->	
IndividualComment{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[[...]]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

city	string
maxLength: 50
The city associated with the submitter's address.

country	string
maxLength: 50
The country associated with the submitter's address.

firstName*	string
maxLength: 25
The submitter's first name.

lastName*	string
maxLength: 25
The submitter's last name.

phone	string
maxLength: 50
The submitter's phone number.

stateProvinceRegion	string
maxLength: 50
The email associated with the submitter's address.

submitterType*	SubmitterTypestring
the submitter type

Enum:
[ Anonymous, Individual, Organization ]
zip	string
maxLength: 10
The zip associated with the submitter's address.

}
OrganizationComment{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[string
The names of the files submitted with the submission

]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

organization*	string
maxLength: 120
The organization that the submitter represents.

organizationType*	string
The agency specific organization type that the submitter represents.

submitterType*	SubmitterTypestring
the submitter type

Enum:
[ Anonymous, Individual, Organization ]
}
AnonymousComment{
category	string
An agency-specific category allowing agencies to group comments according to their type.

comment*	string
maxLength: 5000
The comment text

commentOnDocumentId*	string
documentId of the parent document

email	string
maxLength: 100
The email address to receive email receipt for the commenrt

files	[string
The names of the files submitted with the submission

]
numItemsReceived	integer
The number of items included in the submission

sendEmailReceipt	boolean
Conveys if the user would like to receive an email receipt for the comment

submissionKey	string
The unique identifier associated with the submission

submissionType*	string
The submitter type - Its always going to be API for comments submitted via API

submitterType*	SubmitterTypestring
the submitter type

Enum:
Array [ 3 ]
}
}
{
numItemsReceived	integer
The number of items included in the submission

receiveDate	string
The date comment was received.

}
}
Error{
status	integer
title	string
detail	string
}

</regulations_gov_api_documentation>
