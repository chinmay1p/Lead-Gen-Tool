import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def match_icp(icp_data, companies):
    """Match companies with ICP criteria and score them, handling 'Any' values."""
    model = genai.GenerativeModel('gemini-2.0-flash')  
    matched_companies = []

    for company in companies:
        try:
            company_name = company.get('name', 'Unknown Company')  
            company_location = company.get('address', 'Unknown Location')
            company_website = company.get('website', '')

            company_info = f"Company: {company_name}, Location: {company_location}, Website: {company_website}"

            prompt_parts = []
            prompt_parts.append("Analyze if this company matches the ICP criteria:\n\n")
            prompt_parts.append(f"Company: {company_info}\n\n")
            prompt_parts.append("ICP Criteria:\n")

            criteria_details = []
            if icp_data['company_size'].lower() != 'any':
                criteria_details.append(f"- Company Size: {icp_data['company_size']}")
            if icp_data['revenue_range'].lower() != 'any':
                criteria_details.append(f"- Revenue Range: {icp_data['revenue_range']}")
            if icp_data['funding_stage'].lower() != 'any':
                criteria_details.append(f"- Funding Stage: {icp_data['funding_stage']}")
            if icp_data['tech_stack'].lower() != 'any':
                criteria_details.append(f"- Tech Stack: {icp_data['tech_stack']}")
            if icp_data['pain_points'].lower() != 'any':
                criteria_details.append(f"- Pain Points: {icp_data['pain_points']}")

            if not criteria_details:
                print(f"Skipping {company_name} - all ICP criteria set to 'Any'")
                continue 

            prompt_parts.append("\n".join(criteria_details) + "\n\n")
            prompt_parts.append("""
            Respond with:
            1. Score (0-5) based on how many criteria likely match.  A score of 0 means no information available or a clear mismatch.  A score of 5 means a very strong potential match.
            2. Brief explanation of the match
            
            Format: SCORE: X | EXPLANATION: your explanation
            """)

            prompt = "".join(prompt_parts)

            response = model.generate_content(prompt)
            result = response.text

            # Parse response
            try:
                parts = result.split('|')
                score = int(parts[0].split(':')[1].strip())
                explanation = parts[1].split(':')[1].strip()
            except Exception as parse_error:
                score = 0
                explanation = f"Could not analyze: {parse_error}"

            enriched_company = company.copy()
            enriched_company.update({
                'company_size': icp_data['company_size'],
                'revenue_range': icp_data['revenue_range'],
                'funding_stage': icp_data['funding_stage'],
                'tech_stack': icp_data['tech_stack'],
                'pain_points': icp_data['pain_points'],
                'icp_score': score,
                'icp_explanation': explanation
            })

            matched_companies.append(enriched_company)

        except Exception as e:
            print(f"Error processing {company_name}: {e}")
            continue

    matched_companies.sort(key=lambda x: x['icp_score'], reverse=True)

    return matched_companies