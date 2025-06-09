from typing import Dict, Any
from scraper import scrape_maps
from icp_matcher import match_icp
from summarizer import get_summary

def scrape_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Scrape companies from Google Maps"""
    industry = state.get('industry', '')
    city = state.get('city', '')
    
    try:
        results = scrape_maps(industry, city)
        
        if isinstance(results, str):
            return {
                **state,
                'success': False,
                'error': results,
                'scraped_data': []
            }
        
        return {
            **state,
            'success': True,
            'error': '',
            'scraped_data': results
        }
    except Exception as e:
        return {
            **state,
            'success': False,
            'error': f"Scraping failed: {str(e)}",
            'scraped_data': []
        }

def icp_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Match companies with ICP criteria"""
    icp_data = state.get('icp_data', {})
    scraped_data = state.get('scraped_data', [])
    
    try:
        matched_data = match_icp(icp_data, scraped_data)
        
        return {
            **state,
            'success': True,
            'error': '',
            'icp_data': matched_data
        }
    except Exception as e:
        return {
            **state,
            'success': False,
            'error': f"ICP matching failed: {str(e)}",
            'icp_data': []
        }

def summary_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """Generate company summary"""
    company = state.get('company_name', '')
    
    try:
        summary = get_summary(company)
        
        return {
            **state,
            'success': True,
            'error': '',
            'summary': summary
        }
    except Exception as e:
        return {
            **state,
            'success': False,
            'error': f"Summary failed: {str(e)}",
            'summary': f"Summary failed: {str(e)}"
        }