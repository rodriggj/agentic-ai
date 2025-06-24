# Hotel Booking Agent 

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