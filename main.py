from flask import Flask, render_template, request, session, redirect, url_for, send_file
import os
import uuid
from dotenv import load_dotenv
from graph import create_graph
import pandas as pd

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

workflow = create_graph()

@app.before_request
def init_session():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
        session['state'] = 'start'
        session['scraped_data'] = []
        session['icp_data'] = []
        session['summaries'] = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'scrape':
            industry = request.form['industry']
            city = request.form['city']
            
            # Run LangGraph workflow
            result = workflow.invoke({
                'action': 'scrape',
                'industry': industry,
                'city': city,
                'state': 'start'
            })
            
            if result['success']:
                session['scraped_data'] = result['scraped_data']
                session['state'] = 'scraped'
                session['industry'] = industry
                session['city'] = city
            else:
                session['error'] = result['error']
        
        elif action == 'download_scraped':
            df = pd.DataFrame(session['scraped_data'])
            csv_path = f"scraped_{session['user_id']}.csv"
            df.to_csv(csv_path, index=False)
            return send_file(csv_path, as_attachment=True, download_name="scraped_companies.csv")
        
        elif action == 'continue_icp':
            session['state'] = 'icp_form'
        
        elif action == 'icp_match':
            icp_data = {
                'company_size': request.form['company_size'],
                'revenue_range': request.form['revenue_range'],
                'funding_stage': request.form['funding_stage'],
                'tech_stack': request.form['tech_stack'],
                'pain_points': request.form['pain_points']
            }
            
            result = workflow.invoke({
                'action': 'icp_match',
                'icp_data': icp_data,
                'scraped_data': session['scraped_data'],
                'state': 'icp_form'
            })
            
            session['icp_data'] = result['icp_data']
            session['state'] = 'icp_matched'
        
        elif action == 'download_icp':
            df = pd.DataFrame(session['icp_data'])
            csv_path = f"icp_{session['user_id']}.csv"
            df.to_csv(csv_path, index=False)
            return send_file(csv_path, as_attachment=True, download_name="icp_matched_companies.csv")
        
        elif action == 'start_summary':
            session['state'] = 'summary_loop'
        
        elif action == 'summarize':
            company = request.form['company_name']
            if company.lower() == 'done':
                session['state'] = 'complete'
            else:
                result = workflow.invoke({
                    'action': 'summarize',
                    'company_name': company,
                    'state': 'summary_loop'
                })
                
                session['summaries'].append({
                    'company': company,
                    'summary': result['summary']
                })
    
    return render_template('index.html',
                         state=session.get('state', 'start'),
                         scraped_data=session.get('scraped_data', []),
                         icp_data=session.get('icp_data', []),
                         summaries=session.get('summaries', []),
                         industry=session.get('industry', ''),
                         city=session.get('city', ''),
                         error=session.get('error', ''))

if __name__ == '__main__':
    app.run(debug=True)