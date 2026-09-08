# chains.py
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
# Initialize the LLM
# Ensure your API key is set in your environment (e.g., GROQ_API_KEY)
load_dotenv()
MODEL = os.getenv("MODEL_NAME")
llm = ChatGroq(model=MODEL, temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"))


# =====================================================================
# 1. CLASSIFY CHAIN
# Evaluates shipment issue text and returns exactly one category:
# "delayed", "damaged", "lost", or "unknown"
# =====================================================================
classify_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are an automated logistics support classifier. "
     "Analyze the shipment report and categorize it into EXACTLY ONE of the following categories:\n"
     "- delayed\n"
     "- damaged\n"
     "- lost\n"
     "- unknown\n\n"
     "Respond with ONLY the category word in lowercase (e.g., 'delayed'). Do not include punctuation or extra words."
    ),
    ("human", "Shipment Report: {report_text}")
])

classify_chain = classify_prompt | llm | StrOutputParser()


# =====================================================================
# 2. ESCALATE CHAIN
# Drafts a concise, structured internal memo for a logistics manager.
# =====================================================================
escalate_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are an operations coordinator. Draft a concise, urgent internal escalation note for the Logistics Manager. "
     "Include the Tracking ID, Customer Name, Issue Category, and a clear recommended action (e.g., insurance claim, courier audit, priority dispatch)."
    ),
    ("human", 
     "Tracking ID: {tracking_id}\n"
     "Customer Name: {customer_name}\n"
     "Customer Email: {customer_email}\n"
     "Category: {category}\n"
     "Customer Report: {report_text}"
    )
])

escalate_chain = escalate_prompt | llm | StrOutputParser()


# =====================================================================
# 3. DRAFT EMAIL CHAIN
# Drafts an empathetic, professional customer-facing response email.
# =====================================================================
draft_email_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a professional customer support specialist for an e-commerce logistics company. "
     "Draft a polite, empathetic email to the customer addressing their shipment issue.\n\n"
     "Guidelines:\n"
     "- Greet the customer by name.\n"
     "- Reference their tracking ID.\n"
     "- Acknowledge the specific issue ({category}).\n"
     "- Provide clear next steps and reassurance.\n"
     "- Mention the compensation amount if applicable.\n"
     "- Sign off from 'The Logistics Support Team'."
    ),
    ("human", 
     "Tracking ID: {tracking_id}\n"
     "Customer Name: {customer_name}\n"
     "Category: {category}\n"
     "Compensation Amount: ${compensation_amount:.2f}\n"
     "Customer Report: {report_text}"
    )
])

draft_email_chain = draft_email_prompt | llm | StrOutputParser()