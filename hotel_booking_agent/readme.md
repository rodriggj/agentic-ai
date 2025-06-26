# Hotel Booking Agent 

## Reference Materials
- [ ] See Taj Fort Aguada Resort [here](https://www.tajhotels.com/en-in/hotels/taj-fort-aguada-goa)


## Procedures 

- [ ] [1. Create an Agent](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#agent-creation)
- [ ] [2. Create Tool #1 - RAG Knowledge Base](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#bedrock-knowledge-base-creation---tool-1)
    + - [ ] [S3 Bucket Creation](http://www.google.com)
    + - [ ] [Knowledge Base Creation](http://www.google.com)
- [ ] [3. Create Tool #2 - Room Availability Check](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#aws-lambda-and-openapi-specification-w-dynamodb---tool-2)
    + - [ ] [DynamoDB Configuration](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#dynamodb-table)
    + - [ ] [Lambda Function](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#lambda-function)
    + - [ ] [OpenAPI Schema Creation](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#openapi-schema)
- [ ] [4. Create Tool #3 - Room Booking Capabiliy](https://github.com/rodriggj/agentic-ai/tree/main/
hotel_booking_agent#aws-lambda-and-openapi-specification-w-dynamodb---tool-3)
    + - [ ] [DynamoDB Configuration](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#dynamodb-table)
    + - [ ] [Lambda Function](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#lambda-function)
    + - [ ] [OpenAPI Schema Creation](https://github.com/rodriggj/agentic-ai/tree/main/hotel_booking_agent#openapi-schema)

------------

### Agent Creation
1. Go to AWS console, and query for `Amazon Bedrock`. 

2. When the Amazon Bedrock service screen appears, on the left-nav scroll down and select `Builder Tools \ Agents`. On the right-pane, you'll see a yellow-button that says, `Create Agent` click this button.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/2112cbd4-2a99-4d4f-8ae6-2360b7653f5c" />
</p>

3. Populate the dialog box with `Name` of the agent, and a `Description`, click `Create Agent`. You will verify the Agent was created with a Banner on the redirected page. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/96e60c30-bd07-4afa-b105-9546ea63944a" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/6baa1e57-7d88-4d38-bbc2-742e93e07a1c" />
</p>

4. The Amazon Bedrock service will interact with multple other services to execute its functions (e.g. AWS S3, AWS Lambda, etc.). To do this it will need a Service Role. Bedrock provides an option to manually provision a role or let the service select for you. For this example let the Bedrock service select the appropriate roles by selecting `Create and use a new service role`.

5. Now you will need to select the model that the agent will use from the available options in Amazon Bedrock. Select the yellow-button labeled `Select Model`. When you select this button you are presented with choices for model selection. In this case select the `Anthropic Claude Sonnet 3` Model.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/82218543-cb59-4049-ac15-1acce568f9d1" />
</p>

> The models available to you are a function of selection. If you see the left-nav pane, you can see an option labeled `Models` where you can follow the GUI and select or request access to various models. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/c8418e51-80e3-4015-8700-cf377aeac8b7" />
</p>

6. Now that you've selected your model, you have to give your Agent Instructions. The way to think of this is "if you had a new employee and were providing them with basic guidance on what thier job is". That is what we have to input into the Input Box under `Instructions for Agent`. The input you provide here **WILL** impact your Agent's ability to execute its function so careful and delibrate word choice is needed. 

For this example use the following as input to this Agent's Instructions
```txt
You are a hotel booking assistant for Taj Fort Agunda Resort & Spa, Goa, India
Your primary responsibilities are: 
1. Greet the customer with - Welcome to Taj Fort Agunda Resort & Spa, Goa, India
2. Help customers search for room availabilty and inventory
3. Provide guidance on Room Type
4. Take booking details from the customer
5. Book a hotel room

Follow these guidelines when interacting with customers:
- Be courteous and professional at all times
- Ask for Room Type - Garden or Sea View
- Provide information about Garden or Sea view from Knowledge Base
- Always verify room availability before proceeding with bookings
- Validate the room inventory for Room Type from the customer check-in date
- Collect following information in below format and before booking a room and ask customer for confirmation: 
1. Check-in date
2. Room Type - Garden or Sea
3. Guest Name
4. Number of nights
- Return Booking ID and let the user know that his booking is confirmed

When checking inventory: 
- Verify real-time availability
- Explain room types
```

7. Now click on `Additional Settings`. And apply the following settings: 

- Code Interpretter - "Disabeled"
> This is for allowing the agent to generate code on its own and trying it in a sandbox environment if our use case was to support Software development support. Since we are not for this Agent build we can leave it `Disabled`.

- User Input - "Enabled"
> This is for allowing the Agent to ask clarifying questions to user input. If you leave disabled the agent will make a "best guess" on what input it was provided. 

- KMS Key Selection - "Default"
> If you want to encrypt any data being utilized by the Agent, you can select this option and a KMS key will be provided for when you need to decrypt data.

- Idle Session Timeout - "Default"
> This is a setting that effectively becomes the short term memory. You can set this between 1 - 60 mins, where if set the Agent will store prompts and session information in its respective prompt & session store to utilize with any interactions. Once the time is expired the session and prompt data will be purged. 

8. There are other sections to configure, but for now leave them as default and scroll to the top of the section and click `Save and Exit`. You should now see another banner indicating that the configuration was implemented. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/4416666d-a72a-49f6-a656-10dbaf6aef56" />
</p>

--------------

### Bedrock Knowledge Base Creation - Tool 1

1. Create an S3 bucket to upload Files. Nav to console, `AWS S3` service and create a bucket and call it `gjr-brdemo-s3roominformation`. When creating the bucket, just provide a name, leave all the other config as defaults. 

> Here we create the S3 Bucket
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/365d6cd1-7e00-4681-979e-373411551cba" />
</p>

> Here we utilize the Hotel pdf content as a means to populate our knowledge base
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/1ae6acfb-bb97-4a76-a485-e3698fe034f7" />
</p>

> Here we upload this content to the S3 bucket to populate the Bedrock knowledge base with relevant data
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/4ce4d700-c2a9-4c2c-a8e4-cc3481ed1177" />
</p>

2. Now nav to the AWS Bedrock service from the console. On the left-nav pane, click on `Builder Tools \ Knowledge Bases`. When you click `Create` you are presented with a few options, click `Create Knowledge Base with Vector Store`.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/9dc42004-fa19-4fe5-a1ce-ae51071346ae" />
</p>

3. You will have to configure the `Knowledge Base` in several parts as seen below, for the `Provide Knowledge Base Details` section, populate as follows: 

3a. Name and Description
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/fae6d0d5-327c-4409-8833-8015e0f57002" />
</p>

3b. IAM Role
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/3fb9c2dc-df7d-4a61-88c6-7bff880caca6" />
</p>

3c. Data Source
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/03624484-981b-4c6c-b98e-62860d3293d1" />
</p>

Leave `Tags` and `Log Deliveries` as optional, and click `Next`.

4. Now we will have to configure our data source. In this case becasue we are using S3, the configuration screen is S3 specific. Had we choose to utilzie another data source, the associated configuration screen is slightly different. 

For this screeen simply click the `Browse S3` button, and select the Bucket we created hosting our PDF files. 
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/3ed53abf-ffc3-4c4f-bdac-fc958a6528d5" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/59eca4a3-266a-4812-8030-3e97ec7c8025" />
</p>

Leave the `Chunking` section as default and click `Next`.

5. Next we need to choose the `Embedding` model, which will convert the `Chunking` data into Vector embeddgings. This is a standard part of LLM architectecture. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/d9f7f47e-dbef-48ae-a49d-6479425d7bfa" />
</p>

5a. For the Embeddings Model select - Titan Embeddings
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/a7b0530e-2998-4f99-be2f-603409bece47" />
</p>

5b. Now you have to decide where the Vector embeddings will be stored, so we will select `AWS OpenSearch Serverless`. Then click the `Next` button.
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/3b54c7c9-213f-4273-81df-ffd86c7a868c" />
</p>

6. Finally, you can `Review and Create` the Knowledge Base based on the selections you made previously. Review and click `Create Knowledge Base`

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/07594e47-48bf-4909-ae05-5da71b234afa" />
</p>

Upon clicking `Create Knowledge Base` you will be provided with a banner indicating that the Vector Database and the associated embeddings are being created and stored with OpenSearch Serverless Service. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/dfb00807-1d4f-462b-907b-d195ebcefe29" />
</p>

7. Once the 1. Role Has been provisioned, and 2. The Vector Database has been created, you will need to `Sync` your Knowledge base, with the data source. To do this select your Knowledge bases and press `Sync`. A banner will appear upon successful syncing process. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/121ea7ee-d106-49b7-bdea-dbc965bbd001" />
</p>

> NOTE: There may be issues when attempting to sync. It could be 1. The Role was not created correctly, 2. You don't have access to the Titan Model we used for the Embeddings, or 3. You could be in the wrong Region, or 4. The Trust Relationship to assume the role isn't configured correctly. See the `Sync-Troubleshooting.txt` file for resolution to any of these issues. [Troubleshooting](https://grok.com/share/bGVnYWN5_40ee4530-2683-48bc-b6f7-d8d97f5c4af7)

8. Now lets test our Knowledge base. 

8a. Click on `RoomInformation` Knowledge Base. And then select `Test Your Knowledge Base`. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/ac82ac80-9ba1-4368-9534-21a015aaabeb" />
</p>

8b. Click on `Select Model` 
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/60a4114d-0284-40c0-97f7-13155cd0212a" />
</p>

Select the `Anthropic Claude Sonnet 3` model, and click `Apply`
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/55306a9d-5987-40ab-9e8f-032cbfc909ea" />
</p>

8c. Now we can post a prompt to the Agent and gain some information regarding the Sea View rooms, and receive input from the Vector database that was created to provide input relevant to the Taj rooms. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/c9428882-164b-4dfe-b2a0-a8bcb2401bbf" />
</p>

8d. You can also get some input into the `Chunks` of data that were used to prepare the response. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/d2749eab-a2f6-4b6b-ad97-37a14e089503" />
</p>

9. Now we have to tie the Knowledge Baase to the Agent. 

9a. Copy the Knowledge Base ID

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/c581b391-aade-4494-8cce-46e340e8617b" />
</p>

9b. Navigate back to the AWS Bedrock service, and nav to `Agents` on the left-nav bar. Select the `Hotel_Room_Booking_Agent`. Click `Edit in Agent Builder`
<p alig="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/c581b391-aade-4494-8cce-46e340e8617b" />
</p>

9c. Scroll down to the section called `Knowledge Bases` and click `Add`. Select your Knowledge Base from the drop down. You can also add instructions to the Agent to once again provide it additional context on how to utilize the Knowledge Base. Click the `Add` button. When executed correctly you will see a success banner displayed.

Click on `Save and Exit`. Click on `Prepare`. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/25cc653b-7d36-4ca9-af3e-977ac01b409b" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/3db5d490-2dcf-4372-aead-9bc2e1bee4f0" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/79c14ee2-2004-4439-b600-90181ee7576c" />
</p>

> You can also capture the Knowledge Base Id and input here as well. 

10. Now you can test the agent and see the response. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/1359e76b-1b1c-447b-9e76-0f363c66ec3b" />
</p>

-------------

### AWS Lambda and OpenAPI Specification w/ DynamoDB - Tool 2

#### DynamoDB Table

1. Create the DynamoDB Table. Nav to the AWS console and search for the AWS DynamoDB service. Click `Create Table` and provide a `Table Name` of `hotelRoomAvailabilityTable`. Input the `date` as the Partion Key, leave the rest of the configuration as default, and click `Create Table`.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/c05d2d23-03ee-410e-b3d5-62136f4d71d4" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/adf8ebd8-bc0c-4425-acea-de04c8f92685" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/aab1a51e-a84f-4f1d-9baf-c22bb0f00b25" />
</p>

2. Click on the newly created Table, and then click `Explore Table Items`. Create a series of records as "seed data".

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/dd9fee09-5c74-41f4-9874-83e46d4ee8a2" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/60237c7f-bc18-4849-b0f7-f36509ebd7d2" />
</p>

----

#### Lambda Function 

1. Now navigate to the AWS Lambda service on the AWS Console. Click `Create Lambda`. Name the lambda `hotelAvailabilityFunction`. Change the Runtime to Python 3.13, and click `Create Function`. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/57e45a83-2113-453e-af77-43d8860051f5" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/62db1094-4c02-4ecf-8de7-3bb2aa29fe1d" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/053cb322-c57b-4e2a-a408-08af3c9b7ec3" />
</p>

2. Now that the function has been created, lets modify some of the configuration. 

2a. The lambda function will need time to execute queries and return a result, so we need to increase the `Timeout` configuation. The default is 3 seconds, lets increase it to 1 min 3 seconds. Click `Save`.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/439480ed-713e-4a5d-8233-999bb01dd604" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/9cd21cab-0f4d-4bc3-9f6d-a8bec8053680" />
</p>

2b. Now we need to modify the `Permissions`. 

If you click on the `Role` provided, you will see we only have "basic" permissions. We need to modify these permissions to increase permissions. Just add "Admin" access to the policy permissions. Click `Add Permissions`.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/97f40c18-9bdd-44de-9259-a4938f28171c" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/f2a25312-cc02-4926-be4a-88db4b514de7" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/6a7c6720-0175-4b10-89dd-bb4f377dbeab" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/bd4557f2-f103-40cf-a438-4b31f41e729d" />
</p>

3. Now we need to code the lambda to execute a query to the DDB records and execute some processing. 

3a. Click the `Code` tab of the lambda. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/1fda9333-22c2-451a-9e16-1fa4734b4223" />
</p>

3b. We will now need to execute the following steps within our function: 
```sh
1. Import modules needed - `boto3`
2. Create a client connection to DDB - [documentation here](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
3. Store the user input - date of booking
4. Reference the DDB Table and retrieve data
5. Format the response as per the requirement of Bedrock Agent Action Group - [documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html)
6. Use GET parameters as data retrieval
7. Replace the value of 'body' and print the value of Response Body
8. Add rest of code as expected by Agent - [documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html)
```

Item #1: Input the following import statement in the function
```python
# 1. Import modules needed 
import boto3
```

Item #2: Input the following variable in the function
```python
# 2. Create a client connection to DDB
client = boto3.client('dynamodb')
```

Item #3: Create a Test Payload
First need to create a Test payload. Click the Test button and input the following JSON payload. 
```json
{
    "checkInDate": "2025-12-25"
}
```
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/c5689072-2acc-467e-aa8d-f69bebc64b7e" />
</p>

Input the following print statement in the function
```python
print(f"The user input is {event}")
```

Click, `Deploy` and then click `Test`, and you should get a UI output that looks similar to the following, where you can valdiate that the event is being returned in the correct format. 
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/dda9985c-6b04-45a8-b109-4bc4d74b45f4" />
</p>

Input the following variable assignment in the function 
```python
user_input_date = event['checkInDate']
```

Item #4: GET item
```python
response = client.get_item(TableName='hotelRoomAvailabilityTable', Key={'date': {'S': user_input_date}})
print(response)
```

You can `Deploy` and `Test` again, to make sure that the `response` is yielding a query to the DDB table correctly. 
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/fa9dc995-5c5d-469f-9dd7-3442924ca99e" />
</p>

You can see from the response payload how the response is formatted. Now we can be specific about that response components within the payload we want to retrieve which is just the `Item`. Add the following to the lambda function 
```python
room_inventory_data = response['Item']
```

See the updated view in the Lambda console
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/11212781-cad7-4fa0-a60d-e2506697ad1c" />
</p>

Item #5. We need to allow the response to be formatted so the Bedrock Service can access the response. We need format to the requirement of a `Bedrock Agent Action Group`
Nav to this link and scroll down to see the OpenAPI specification to create a Bedrokc Agent Action Group [here](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-lambda.html). 

Copy/Paste the following into your lambda: 
```python
agent = event['agent']
    actionGroup = event['actionGroup']
    api_path = event['apiPath']
    # get parameters
    get_parameters = event.get('parameters', [])
    # post parameters
    post_parameters = event['requestBody']['content']['application/json']['properties']   # Delete this line

    response_body = {
        'application/json': {
            'body': "sample response"
        }
    }
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
    return api_response
```

#Edits: 
- [ ] We are not POSTing any data in this use case, so delete the `post_parameters` line.
- [ ] In the response body, replace `sample_response` with `room_inventory_data`
- [ ] Add a print statement to validate the response body
- [ ] Add a print statement for final `api_response`

The completed lambda body will be the following: 

```python
import json
# 1. Import modules needed - `boto3`
import boto3

# 2. Create a client connection to DDB
client = boto3.client('dynamodb')

def lambda_handler(event, context):
# 3. Store the user input 
    print(f"The user input is {event}")
    user_input_date = event['parameters'][0]['value']

# 4. Reference the DDB Table and retrieve data
    response = client.get_item(TableName='hotelRoomAvailabilityTable', Key={'date': {'S': user_input_date}})
    # print(response)
    room_inventory_data = response['Item']
    print(room_inventory_data)

#5. Format the response as per the requirement of Bedrock Agent Action Group
    agent = event['agent']
    actionGroup = event['actionGroup']
    api_path = event['apiPath']
    # get parameters
    get_parameters = event.get('parameters', [])

    response_body = {
        'application/json': {
            'body': json.dumps(room_inventory_data)
        }
    }

    print(f"The response that will be provided to the agent is {response_body}")
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
    print(f"The final api response is {api_response}")
    return api_response
```

#### OpenAPI Schema
1. Navigate to the Amazon Bedrock service. Select your Agent, and click `Edit in Agent Builder`

2. Scroll down to the `Action Group` section, and click `Add`. Provide a `Name` and a `Description`
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/156d1778-607a-4e05-807a-ba8abcafdfc5" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/1c6415c3-77db-4fba-837a-f2521610fc7e" />
</p>

3. There are 2 `Action Group Types`. In this case because we have a lambda that does the processing, and we will utilzie the API schema for Agent to interact with that Lambda, select the `Define API Schema` option. From the dropdown select the Lambda function we've built - `hotelAvailabilityFunction`

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/1eb422e9-17cc-459c-a864-4978f25a4482" />
</p>

4. Now we need to define the `Action Group Schema`. We can do it again in 2 ways. We can 1. select an existing Schema or 2. Define via in-line schema editor. B/c we have created a custom lambda, it makes sense to process the option 2. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/14830baf-384b-433b-bc97-9ef46d319d0f" />
</p>

4a. To edit the schema, Copy/Paste the example and input into a text editor. Then modify according to the API specification that you want to see implemented. See file called `HotelRoomAvailabilityAPI.yaml`. 

4b. Copy/paste the OpenAPI spec into the Bedrock editor for the API scheam definition.  Click `Create`. Then click `Save and Exit`. Then click on `Prepare`.

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/2635baa1-9b35-44fd-9f35-c7aabb531534" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/66bc2609-d0c5-4d9f-baab-3ffcf6021bef" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/4cc4bd72-5e93-4381-b79c-b9cd81984d80" />
</p>

5. Now we need to return to the Lambda function and give the `Agent` permissions to utilize the Lambda. 

5a. Nav to the Lambda service. Select our lamdba, and click `Configuration`. Now click `Add Permissions`. Click on `AWS Service`

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/146cdc05-dce5-4be2-b78c-53ead04fae60" />
</p>

You can see there is no service that says `Agent` listed here. We need to add it. Click `Other`. 

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/d698b51d-603b-47c6-adb8-f65767134ef8" />
</p>

Here we need to provide the following: 
- [ ] Statement ID: You can put whatever you want. 'hotel-booking-inventory'
- [ ] Principal: This will be the Bedrock Agent. 'bedrock.amazonaws.com'
- [ ] Source ARN: (You can get this from the Bedrock \ Agent screen) 'arn:aws:bedrock:us-west-2:551061066810:agent/I9HPADAM84'
- [ ] Action: Here you will have a drop down, select the 'lambdaInvoke' permission. 
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/9a5d47ae-f3d4-4c4e-acf2-17e3084814a5" />
</p>

6. Now we can test the Bedrock agent, and see what it has to say about specific dates. 
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/f2bfb3e6-b71e-469d-ab15-16e2d0c5cdc0" />
</p>

------ 

### AWS Lambda and OpenAPI Specification w/ DynamoDB - Tool 3

#### Create DDB Table

#### Create Lambda Function 

1. Modify the permissions
2. Execute the following steps in the lambda function: 

```txt
1. Imports (boto3, uuid)
2. Initialize DDB connection
3. Store the user input - get event details.
4. Retrieve the data from the event - guestName, checkInDate, numberOfNights, & roomType
5. Get room availabilty from hotelRoomAvailability Table using get_item method
6. Get room inventory data for SeaView rooms and GardenView rooms and print values
7. If inventory for Gardenview and Seaview = 0; send error message to the user -- No rooms available for specified date.
8. Generate unique booking ID to store in DDB table along with booking and send back booking id to user
9. Create booking record by inserting this data into hotelRoomBookingTable using boto3 put_items method
10. Print return bookingID
11. Add details the Bedrock Agent expects 
12. Use POST parameters and send back bookingID to user, print booking id
13. Replace value of responseBody and print, return api_response
```

Repeat the same steps above to ensure that the Lambda is configured. 

```python
# 1. Execute imports
import json
import boto3
import uuid

# 2. Make client connection
client = boto3.client('dynamodb')

def lambda_handler(event, context):
# 3. Store the user input - get event details.
    print(f"The user input from the Agent is {event}")
    input_event = event
 
# 4. Retrieve the data from the event - guestName, checkInDate, numberOfNights, & roomType
    input_data = event['requestBody']['content']['application/json']['properties']
    print(type(input_data))
    print(input_data)

    for item in input_data:
        if item['name'] == 'guestName': 
            guestName = item['value']
        elif item['name'] == 'checkInDate':
            checkInDate = item['value']
        elif item['name'] == 'numberOfNights':
            numberOfNights = item['value']
        elif item['name'] == 'roomType':
            roomType = item['value']
    print(guestName)

    # guestName = input_event['guestName']
    # checkInDate = input_event['checkInDate']
    # numberOfNights = input_event['numberOfNights']
    # roomType = input_event['roomType']
    # print(f"The guest name is {guestName}")

# 5. Get room availabilty from hotelRoomAvailability Table using get_item method
    response = client.get_item(TableName='hotelRoomAvailabilityTable', Key={'date': {'S': checkInDate}})
    # print(response)
    room_inventory_data = response['Item']
    print(room_inventory_data)

# 6. Get room inventory data for SeaView rooms and GardenView rooms and print values
    current_gardenview_rooms = int(room_inventory_data['gardenView']['S'])
    current_seaview_rooms = int(room_inventory_data['seaView']['S'])
    print(f"The gardenview inventory is : {current_gardenview_rooms}")
    print(f"The seaview inventory is : {current_seaview_rooms}")

# 7. If inventory for Gardenview and Seaview = 0; send error message to the user -- No rooms available for specified date.
    if current_gardenview_rooms == 0 and current_seaview_rooms == 0:
        print("No rooms available for specified date")
        return {
            'statusCode': 404,
            'body': json.dumps('No rooms available for specified date')
        }
        print(response)
        return response
    else:

# 8. Generate unique booking ID to store in DDB table along with booking and send back booking id to user
        booking_id = str(uuid.uuid4())
        print(f"The booking id is {booking_id}")

# 9. Create booking record by inserting this data into hotelRoomBookingTable using boto3 put_items method
    response_booking = client.put_item(
        TableName='hotelRoomBookingTable', 
        Item={
            'bookingID': {'S': booking_id}, 
            'guestName': {'S': guestName}, 
            'checkInDate': {'S': checkInDate}, 
            'numberOfNights': {'S': numberOfNights}, 
            'roomType': {'S': roomType}
        }
    )

# 10. Print return bookingID
    print(f"The response from Lambda is {booking_id}")

# 11. Add details the Bedrock Agent expects 
    agent = event['agent']
    actionGroup = event['actionGroup']
    api_path = event['apiPath']

    # post parameters
    post_parameters = event['requestBody']['content']['application/json']['properties']

    response_body = {
        'application/json': {
            'body': json.dumps(booking_id)
        }
    }
    
    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': 200,
        'responseBody': response_body
    }
    
    session_attributes = event['sessionAttributes']
    prompt_session_attributes = event['promptSessionAttributes']
    
    api_response = {
        'messageVersion': '1.0', 
        'response': action_response,
        'sessionAttributes': session_attributes,
        'promptSessionAttributes': prompt_session_attributes
    }
        
# 13. Replace value of responseBody and print, return api_response
    return api_response
```
<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/83d4169e-59ed-47ef-8804-92249f0a410c" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/32241fde-2caf-4eba-a57a-61c8c5c8f9f3" />
</p>

<p align="center">
<img width="300" alt="Image" src="https://github.com/user-attachments/assets/658e0243-fe6c-48b1-b5ef-64be758f3049" />
</p>

