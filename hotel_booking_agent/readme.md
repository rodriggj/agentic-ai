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