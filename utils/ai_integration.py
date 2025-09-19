"""
AI integration for GPT-powered responses using LangChain
"""

import os
from typing import Dict, List, Any
import pandas as pd
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
import json

class FetiiAI:
    """AI-powered analytics for Fetii rideshare data"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        
        # Initialize the LLM
        self.llm = ChatOpenAI(
            openai_api_key=self.api_key,
            model_name="gpt-3.5-turbo",  # Can be upgraded to gpt-4
            temperature=0.1,
            max_tokens=500
        )
        
        # System prompt for the AI
        self.system_prompt = """
        You are FetiiAI, an intelligent assistant that analyzes Austin rideshare data from Fetii.
        You help users understand group mobility patterns, popular destinations, peak times, and rider demographics.
        
        Key capabilities:
        - Analyze trip statistics and trends
        - Identify popular destinations and pickup locations
        - Provide insights on group sizes and demographics
        - Suggest optimal ride times and routes
        - Answer questions about Austin rideshare patterns
        
        Always provide data-driven insights with specific numbers when available.
        Be conversational and helpful, but focus on actionable insights.
        """
        
        # Create the prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "Context: {context}\n\nUser Question: {question}\n\nProvide a helpful response based on the data:")
        ])
        
        # Create the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def generate_response(self, question: str, data_context: Dict[str, Any]) -> str:
        """Generate AI response based on question and data context"""
        try:
            # Prepare context from data
            context = self._prepare_context(data_context)
            
            # Generate response
            response = self.chain.run(
                context=context,
                question=question
            )
            
            return response.strip()
        
        except Exception as e:
            return f"I encountered an error while processing your request: {str(e)}. Please try rephrasing your question."
    
    def _prepare_context(self, data_context: Dict[str, Any]) -> str:
        """Prepare context string from data"""
        context_parts = []
        
        # Add basic statistics
        if 'stats' in data_context:
            stats = data_context['stats']
            context_parts.append(f"Dataset Overview:")
            context_parts.append(f"- Total trips: {stats.get('total_trips', 'N/A')}")
            context_parts.append(f"- Average group size: {stats.get('avg_group_size', 'N/A'):.1f}")
            context_parts.append(f"- Peak hour: {stats.get('peak_hour', 'N/A')}:00")
            context_parts.append(f"- Most common group size: {stats.get('most_common_group_size', 'N/A')}")
            context_parts.append(f"- Average rider age: {stats.get('avg_rider_age', 'N/A'):.1f} years")
        
        # Add filtered data insights
        if 'filtered_data' in data_context and data_context['filtered_data'] is not None:
            filtered_df = data_context['filtered_data']
            if len(filtered_df) > 0:
                context_parts.append(f"\nFiltered Data ({len(filtered_df)} trips):")
                context_parts.append(f"- Average group size: {filtered_df['group_size'].mean():.1f}")
                context_parts.append(f"- Average trip duration: {filtered_df['trip_duration_minutes'].mean():.1f} minutes")
                context_parts.append(f"- Average fare: ${filtered_df['fare_amount'].mean():.2f}")
        
        # Add popular destinations
        if 'popular_destinations' in data_context:
            destinations = data_context['popular_destinations']
            if len(destinations) > 0:
                context_parts.append(f"\nTop Destinations:")
                for i, (dest, count) in enumerate(destinations.head(5).items(), 1):
                    context_parts.append(f"{i}. {dest}: {count} trips")
        
        # Add hourly patterns
        if 'hourly_patterns' in data_context:
            hourly = data_context['hourly_patterns']
            if len(hourly) > 0:
                peak_hour = hourly.loc[hourly['trip_count'].idxmax(), 'pickup_hour']
                peak_count = hourly['trip_count'].max()
                context_parts.append(f"\nPeak Hour: {peak_hour}:00 with {peak_count} trips")
        
        # Add demographic insights
        if 'demographics' in data_context:
            demo = data_context['demographics']
            if 'age_distribution' in demo:
                context_parts.append(f"\nAge Distribution:")
                for age_group, count in demo['age_distribution'].head(3).items():
                    context_parts.append(f"- {age_group}: {count} riders")
        
        return "\n".join(context_parts)
    
    def analyze_query_intent(self, question: str) -> Dict[str, Any]:
        """Analyze the user's query to determine intent and required data filters"""
        question_lower = question.lower()
        
        intent = {
            'type': 'general',
            'filters': {},
            'metrics': [],
            'time_range': None,
            'location': None
        }
        
        # Detect query type
        if any(word in question_lower for word in ['moody center', 'moody', 'center']):
            intent['type'] = 'location_specific'
            intent['location'] = 'Moody Center'
        
        elif any(word in question_lower for word in ['peak', 'busy', 'popular time']):
            intent['type'] = 'temporal_analysis'
            intent['metrics'] = ['hourly_patterns']
        
        elif any(word in question_lower for word in ['group size', 'group', 'people']):
            intent['type'] = 'group_analysis'
            intent['metrics'] = ['group_size_distribution']
        
        elif any(word in question_lower for word in ['age', 'demographic', 'rider']):
            intent['type'] = 'demographic_analysis'
            intent['metrics'] = ['age_distribution']
        
        elif any(word in question_lower for word in ['destination', 'where', 'popular place']):
            intent['type'] = 'destination_analysis'
            intent['metrics'] = ['popular_destinations']
        
        # Detect time filters
        if 'last month' in question_lower:
            intent['time_range'] = 'last_month'
        elif 'last week' in question_lower:
            intent['time_range'] = 'last_week'
        elif 'weekend' in question_lower:
            intent['time_range'] = 'weekend'
        elif 'weekday' in question_lower:
            intent['time_range'] = 'weekday'
        
        # Detect group size filters
        if 'large group' in question_lower:
            intent['filters']['group_size'] = {'min': 5}
        elif 'small group' in question_lower:
            intent['filters']['group_size'] = {'max': 3}
        
        return intent
    
    def get_suggested_queries(self) -> List[str]:
        """Get suggested queries for the user"""
        return [
            "How many groups went to Moody Center last month?",
            "What are the peak ride times for large groups?",
            "Show me the most popular destinations in Austin",
            "What's the average group size on weekends?",
            "Tell me about rider age demographics",
            "Which areas have the most pickup requests?",
            "How do ride patterns differ between weekdays and weekends?",
            "What's the busiest hour for rides to the airport?",
            "Show me group size trends over time",
            "Which age groups use rideshare most frequently?"
        ]
