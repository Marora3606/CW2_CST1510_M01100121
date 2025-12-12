# AI Assistant Service
# Provides AI-powered assistance and analysis

import openai
from typing import List, Dict, Any, Optional
import json

class AIAssistant:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def analyze_text(self, text: str, domain: str = "general") -> Dict[str, Any]:
        """Analyze text content using AI"""
        system_prompts = {
            "cybersecurity": "You are a cybersecurity analyst. Analyze the following text for security threats, vulnerabilities, and provide recommendations.",
            "data": "You are a data analyst. Analyze the following data/text and provide insights, patterns, and recommendations.",
            "general": "You are a helpful assistant. Analyze the following text and provide insights."
        }

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompts.get(domain, system_prompts["general"])},
                    {"role": "user", "content": f"Please analyze this text: {text}"}
                ],
                max_tokens=500
            )

            analysis = response.choices[0].message.content
            return {
                "success": True,
                "analysis": analysis,
                "domain": domain
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "domain": domain
            }

    def generate_report(self, data: Dict[str, Any], report_type: str = "summary") -> Dict[str, Any]:
        """Generate AI-powered reports"""
        try:
            prompt = f"Generate a {report_type} report based on the following data: {json.dumps(data, indent=2)}"

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a professional report writer. Create clear, concise, and well-structured reports."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000
            )

            report = response.choices[0].message.content
            return {
                "success": True,
                "report": report,
                "type": report_type
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "type": report_type
            }

    def classify_incident(self, incident_description: str) -> Dict[str, Any]:
        """Classify security incidents using AI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a cybersecurity incident classifier. Classify the incident by severity (Critical, High, Medium, Low) and type (Malware, Phishing, DDoS, etc.). Provide brief justification."},
                    {"role": "user", "content": f"Classify this incident: {incident_description}"}
                ],
                max_tokens=200
            )

            classification = response.choices[0].message.content
            return {
                "success": True,
                "classification": classification,
                "incident": incident_description[:100] + "..." if len(incident_description) > 100 else incident_description
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def suggest_actions(self, situation: str, context: str = "general") -> Dict[str, Any]:
        """Suggest actions for given situations"""
        try:
            prompt = f"Situation: {situation}\nContext: {context}\n\nSuggest appropriate actions to resolve or handle this situation."

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert advisor. Provide practical, actionable suggestions for various situations."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300
            )

            suggestions = response.choices[0].message.content
            return {
                "success": True,
                "suggestions": suggestions,
                "situation": situation
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

# Note: Initialize with actual API key when using
# ai_assistant = AIAssistant(api_key="your-openai-api-key")
