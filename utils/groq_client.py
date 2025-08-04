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

    def _generate_test_cases_for_chunk(self, chunk_prompt, test_types, complexity_level, model):
        """Generate test cases for a single chunk"""

        full_prompt = f"""{chunk_prompt}

Test Requirements:
- Test Types: {', '.join(test_types)}
- Complexity Level: {complexity_level}

Please provide test cases for the components in this chunk:
1. **Chunk Analysis** - What components/logic are present in this chunk
2. **Test Scenarios** - Specific test cases for this chunk's functionality
3. **Input Data** - Required inputs for testing this chunk
4. **Expected Results** - Expected outputs from this chunk
5. **Integration Points** - How this chunk connects to other parts

Format concisely but thoroughly. Focus on TIBCO BusinessWorks patterns.
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks developer specializing in test case generation for code chunks."},
                    {"role": "user", "content": full_prompt}
                ],
                model=model,
                temperature=0.3,
                max_tokens=3000
            )

            return response.choices[0].message.content

        except Exception as e:
            st.error(f"Groq API Error processing chunk: {str(e)}")
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

    def _analyze_complexity_for_chunk(self, chunk_prompt, analysis_types, detail_level, model):
        """Analyze complexity for a single chunk"""

        full_prompt = f"""{chunk_prompt}

Analysis Requirements:
- Analysis Areas: {', '.join(analysis_types)}
- Detail Level: {detail_level}

Please analyze this chunk covering:
1. **Chunk Complexity** - Complexity metrics for this specific chunk
2. **Local Dependencies** - Dependencies within this chunk
3. **Component Analysis** - TIBCO components and their complexity
4. **Chunk-specific Issues** - Problems identified in this chunk
5. **Integration Impact** - How this chunk affects overall process complexity

Be concise but thorough. Focus on actionable insights.
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks architect specializing in code complexity analysis for large files."},
                    {"role": "user", "content": full_prompt}
                ],
                model=model,
                temperature=0.2,
                max_tokens=3000
            )

            return response.choices[0].message.content

        except Exception as e:
            st.error(f"Groq API Error analyzing chunk: {str(e)}")
            return None