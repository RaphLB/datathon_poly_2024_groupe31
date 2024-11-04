# Use the Converse API to send a text message to Claude 3 Haiku.
import boto3
from botocore.exceptions import ClientError
import os
import pandas as pd

os.environ["AWS_DEFAULT_REGION"] = "us-west-2"
os.environ["AWS_ACCESS_KEY_ID"] = "ASIA3IJIDNOGU255XLJ3"
os.environ["AWS_SECRET_ACCESS_KEY"] = "SV+3ieB3RZsAtMleFkpA4tqDTa+8Pbg3uQS7nX8q"
os.environ["AWS_SESSION_TOKEN"] = "IQoJb3JpZ2luX2VjEG8aCXVzLWVhc3QtMSJIMEYCIQD54fvrwEM2LofBXBzcDq5sW+zMXZBWEwV1/ySrOIqrzQIhALSjZorQ5k8DYCnErZzKgRryL5TIsKEKd2QX1Srup8CYKqICCOj//////////wEQARoMNzczNzE1MDk0NDEzIgyyGAQUxib/XTGcPdIq9gEwc/ZsfaEE7Hyq6MGa5C6bJKLmM/tnHq9RVHZuAPSMwq9HijJTHklXHFXWjWX8tZgQC/g9aBE86NgV0F2PB9NJQ1tyIPTcuDbKSUGra99XCAOMJfOnQtX3yhbm4Bj6h79AN5BCYGi0EpaY4ze02+omsp/khaCkPRMk3QDbtXThIgfunml0FL7abpWhAZuiS44i4/5ewtkoC1yGOpXb7XUQlQ9IQBXighUnqFuMPHdtPqhWkZ6YFobm1KdgH4EdAQdxVhdJSuxIuq4bWmwMgEM0rWKr+1Yknooc9aRyUVmJqUfodjkuZxytcsKX8k5klj4qiHM74XkwvtKhuQY6nAHBUsxuh1QekgEab1+kEmv/oG0bf2XfMZavugVBiayd313PRV5uPvhhXEsNsM5wm1MoV+na1WTauRHhVaxyMBRqgk+lf0Oi0GBLPfuREWffG9RpZXzKnTxkFxYW01LUsgZDCFdXQScYb0ny8IAVFUwqYKbhzUK9qAaMmUVxJOs45eukpZP4nyzZOljYa4siMkktLBLWWpUlKWIZ82g="

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the model ID, e.g., Titan Text Premier.
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

def script_LLM_option_1(pdf_text) : 
    # Global summaryse of the pdf_text
    user_message = f"""
    You are an AI assistant helping a financial analyst by extracting and summarizing key information from financial reports. 
    The analyst will provide raw text from a financial report, which may be in French or English, and you should respond in the language of the text provided. 
    Here is the text to summarize:
    {pdf_text}
    
    Please structure your summary by including the following sections:
    
    - **Company Name**: Identify the name of the company in the report.
    - **Date**: Include the date of the report or relevant financial period.
    - **Industry**: Specify the industry or sector of the company, such as "Industrie," "Consommation de base," "Services publics," "Télécommunications," etc.
    - **Key Financial Highlights**: Summarize main financial metrics, trends, or significant events impacting the company's financial position.
    - **Risks and Opportunities**: Note any risks, opportunities, or strategic directions mentioned in the document.
    - **Conclusion**: Provide an overall assessment if available, summarizing the outlook or strategic priorities highlighted in the report.

    After listing this information, please proceed with a more detailed summary as you would normally do, focusing on the main points and insights relevant to the financial analyst.
    
    """
    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":1000,"temperature":1},
            additionalModelRequestFields={"top_k":250}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        print(response_text)

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

def script_LLM_option_2(pdf_text) : 
    # Summaryse of the message from the direction
    user_message = f"""
    You are an AI assistant tasked with helping a financial analyst by extracting and summarizing key information from financial reports. 
    The analyst wants to analyze the sentiment of the message from management in the annual report. 

    Please process the provided text from the first 20 pages of the report, which may be in French or English. Respond in the same language as the text.
    
    Here is the text to summarize:
    {pdf_text}

    Your tasks are as follows:
    1. Identify and extract the management message by searching for keywords such as "message", "lettre", or "letter".
    2. Summarize the extracted message.
    3. Provide your sentiment analysis of the message.
    """

    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":1000,"temperature":1},
            additionalModelRequestFields={"top_k":250}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)

def script_LLM_option_3(task, text = None) : 
    
    if task == 1 :
        user_message = f"""
        You are now a chatbot designed to assist a financial analyst in quickly extracting information from financial reports. 
        The analyst has a specific request: to perform a keyword search within the provided text of the annual report.

        Please start by greeting the analyst and asking them politely for the keywords they would like to search for in the report. 
        """
    if task == 2:
        user_message = f"""
        You are now a chatbot designed to assist a financial analyst in quickly extracting information from financial reports. 
        In the previous interaction, you asked the analyst for keywords they would like to search for in the annual report. 
        Now, based on the analyst's response, please extract the keywords from their message.

        Your response should be structured strictly as follows:
        Here are the keywords from the analyst: keyword1, keyword2, keyword3, ...
        If the keywords are in french make sure to include their translation in english as well and vice-versa.
        Make sure to separate each keyword with a comma and a space. If no keywords are identified, do not write anything at all.

        Here is the analyst's input:
        {text}  
        """
    if task == 3:
        if text!=None:
            df = pd.read_csv(text)
            text = df.to_string(index=False)
        user_message = f"""

You are a data analysis assistant with expertise in extracting relevant information from CSV files. The client has requested an analysis by keywords from a PDF document, which we have converted into a CSV. Each row in the CSV corresponds to a specific keyword or key term, with associated information. Your task is to review the CSV content provided in text format and respond with a clear, polite summary, as if the user had directly requested an analysis by keywords.

1 :Analyze the CSV: Identify and summarize the main elements, including columns, data types, and relevant descriptive statistics (e.g., mean, median, frequency, unique values) that highlight keyword trends. Note any patterns or anomalies that may be insightful for understanding the document's focus.

2 :Present the Results: Organize the findings in a structured manner. If possible, generate a formatted table with key details for each keyword, or highlight samples to illustrate noteworthy trends, making it easy for the user to review the results.

3 :Return a Response: Provide a concise, user-friendly response that summarizes the keyword-related insights and suggests how the user might interpret or further explore these data.

Here is the data from the csv file in a text format :

        {text}  
        """

    conversation = [
        {
            "role": "user",
            "content": [{"text": user_message}],
        }
    ]

    try:
        # Send the message to the model, using a basic inference configuration.
        response = client.converse(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            messages=conversation,
            inferenceConfig={"maxTokens":1000,"temperature":1},
            additionalModelRequestFields={"top_k":250}
        )

        # Extract and print the response text.
        response_text = response["output"]["message"]["content"][0]["text"]
        return response_text

    except (ClientError, Exception) as e:
        print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
        exit(1)