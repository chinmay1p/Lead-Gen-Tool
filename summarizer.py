import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_summary(company_name):
    """Generate company summary using Gemini"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Create a detailed company summary for {company_name} including:
        
        1. Company Overview
        2. Business Model
        3. Recent News/Updates
        4. Market Position
        5. Potential Value for Sales Outreach
        
        Keep it concise but informative for sales purposes. Do not include any '*' in the text.
        """
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"Error generating summary for {company_name}: {str(e)}"