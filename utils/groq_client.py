import os
from groq import Groq
import streamlit as st

class GroqClient:
    def __init__(self, api_key):
        self.client = Groq(api_key=api_key)
    
    def generate_test_cases(self, code, test_types, complexity_level, model):
        """Generate test cases for TIBCO BusinessWorks code"""
        
        prompt = f"""
You are an expert TIBCO BusinessWorks developer and test engineer. Analyze the following TIBCO code/XML and generate comprehensive test cases.

TIBCO Code/XML:
{code}

Test Requirements:
- Test Types: {', '.join(test_types)}
- Complexity Level: {complexity_level}

Please provide:
1. **Test Case Overview** - Brief summary of the process being tested
2. **Input Data Sets** - Specific input values for each test scenario
3. **Expected Results** - What the expected output should be for each input
4. **Test Steps** - Detailed steps to execute each test
5. **Edge Cases** - Boundary conditions and edge scenarios
6. **Error Scenarios** - Invalid inputs and error handling tests
7. **Validation Points** - Key checkpoints to verify during testing

Format the response in clear sections with bullet points and code examples where applicable.
Focus on TIBCO BusinessWorks specific testing patterns and best practices.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks developer specializing in comprehensive test case generation."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
                temperature=0.3,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")
            return None
    
    def analyze_complexity(self, code, analysis_types, detail_level, model):
        """Analyze TIBCO code complexity and identify issues"""
        
        prompt = f"""
You are an expert TIBCO BusinessWorks architect and code reviewer. Analyze the following TIBCO code/XML for complexity, patterns, and potential issues.

TIBCO Code/XML:
{code}

Analysis Requirements:
- Analysis Areas: {', '.join(analysis_types)}
- Detail Level: {detail_level}

Please provide a comprehensive analysis covering:

1. **Complexity Metrics**
   - Cyclomatic complexity score
   - Nesting levels and depth
   - Number of decision points

2. **Architecture Analysis**
   - Process flow complexity
   - Component interactions
   - Data transformation complexity

3. **Dependency Analysis**
   - External dependencies
   - Coupling between components
   - Resource dependencies

4. **Anti-pattern Detection**
   - Common TIBCO anti-patterns
   - Code smells specific to BusinessWorks
   - Maintainability issues

5. **Performance Implications**
   - Potential bottlenecks
   - Memory usage concerns
   - Processing efficiency

6. **Recommendations**
   - Refactoring suggestions
   - Best practice improvements
   - Optimization opportunities

7. **Risk Assessment**
   - Maintainability score (1-10)
   - Complexity rating (Low/Medium/High)
   - Priority areas for improvement

Format the response with clear sections, metrics, and actionable recommendations.
Use TIBCO BusinessWorks terminology and best practices throughout.
"""
        
        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks architect specializing in code analysis and complexity assessment."},
                    {"role": "user", "content": prompt}
                ],
                model=model,
                temperature=0.2,
                max_tokens=4000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            st.error(f"Groq API Error: {str(e)}")
            return None
