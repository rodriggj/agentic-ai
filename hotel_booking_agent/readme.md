# Hotel Booking Agent 

## Referencen Materials
- [ ] See Taj Fort Aguada Resort [here](https://www.tajhotels.com/en-in/hotels/taj-fort-aguada-goa)


## Procedures 

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

> NOTE: There may be issues when attempting to sync. It could be 1. The Role was not created correctly, 2. You don't have access to the Titan Model we used for the Embeddings, or 3. You could be in the wrong Region, or 4. The Trust Relationship to assume the role isn't configured correctly. See the `Sync-Troubleshooting.txt` file for resolution to any of these issues. 