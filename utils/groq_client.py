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

    def optimize_process(self, code, optimization_areas, optimization_level, include_code_examples, model):
        """Optimize TIBCO processes for better performance and efficiency"""

        prompt = f"""
You are an expert TIBCO BusinessWorks performance architect and optimization specialist. Analyze the following TIBCO code/XML and provide comprehensive optimization recommendations.

TIBCO Code/XML:
{code}

Optimization Requirements:
- Focus Areas: {', '.join(optimization_areas)}
- Optimization Level: {optimization_level}
- Include Code Examples: {include_code_examples}

Please provide detailed optimization analysis covering:

1. **Performance Bottlenecks**
   - Identify current performance issues
   - Resource utilization problems
   - Scalability limitations

2. **Memory Optimization**
   - Memory usage patterns
   - Object lifecycle management
   - Garbage collection optimization

3. **Connection Management**
   - Connection pooling strategies
   - Resource sharing opportunities
   - Database connection optimization

4. **Async Processing**
   - Opportunities for asynchronous execution
   - Parallel processing recommendations  
   - Queue management strategies

5. **Error Handling Optimization**
   - Efficient error processing
   - Graceful degradation patterns
   - Recovery mechanisms

6. **Caching Strategies**
   - Data caching opportunities
   - Result set caching
   - Configuration caching

7. **Optimization Recommendations**
   - Specific code changes
   - Configuration adjustments
   - Architecture improvements
   {"- Complete optimized code examples" if include_code_examples else "- High-level implementation guidance"}

8. **Performance Metrics**
   - Expected performance improvements
   - Resource usage reduction estimates
   - Scalability enhancements

Format with clear sections, specific recommendations, and measurable outcomes.
Focus on TIBCO BusinessWorks best practices and proven optimization patterns.
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks performance architect specializing in process optimization and performance tuning."},
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

    def generate_documentation(self, code, doc_types, doc_format, include_diagrams, model):
        """Generate comprehensive documentation for TIBCO processes"""

        prompt = f"""
You are an expert TIBCO BusinessWorks technical writer and documentation specialist. Generate comprehensive documentation for the following TIBCO code/XML.

TIBCO Code/XML:
{code}

Documentation Requirements:
- Documentation Types: {', '.join(doc_types)}
- Format: {doc_format}
- Include Diagrams: {include_diagrams}

Please generate documentation covering:

1. **Technical Overview**
   - Process purpose and functionality
   - High-level architecture
   - Key components and their roles

2. **API Documentation**
   - Input/output specifications
   - Service interfaces
   - Data contracts and schemas

3. **Component Details**
   - Individual component descriptions
   - Configuration parameters
   - Dependencies and relationships

4. **Data Flow**
   - Data transformation steps
   - Processing pipeline
   {"- ASCII flow diagrams" if include_diagrams else "- Textual flow descriptions"}

5. **Configuration Reference**
   - Required settings
   - Optional parameters
   - Environment-specific configurations

6. **Deployment Guide**
   - Installation procedures
   - Environment setup
   - Deployment best practices

7. **Troubleshooting**
   - Common issues and solutions
   - Error codes and meanings
   - Debugging procedures

8. **Performance Guidelines**
   - Tuning recommendations
   - Monitoring strategies
   - Capacity planning

Format the documentation in {doc_format} format with proper structure, headers, and formatting.
Make it comprehensive yet readable for both technical and business stakeholders.
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks technical writer specializing in comprehensive documentation generation."},
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

    def analyze_migration(self, code, migration_type, migration_areas, migration_priority, include_migration_code, model):
        """Analyze and assist with TIBCO migrations and modernization"""

        prompt = f"""
You are an expert TIBCO BusinessWorks migration architect and modernization specialist. Analyze the following legacy TIBCO code and provide comprehensive migration guidance.

Legacy TIBCO Code/XML:
{code}

Migration Requirements:
- Migration Type: {migration_type}
- Focus Areas: {', '.join(migration_areas)}
- Priority Level: {migration_priority}
- Include Migration Code: {include_migration_code}

Please provide detailed migration analysis covering:

1. **Compatibility Assessment**
   - Current version compatibility
   - Deprecated features identification
   - Breaking changes analysis

2. **Component Migration**
   - Component-by-component migration plan
   - Modern equivalents for deprecated components
   - API changes and updates

3. **Configuration Changes**
   - Required configuration updates
   - New configuration options
   - Environment-specific changes

4. **Architecture Modernization**
   - Cloud-native opportunities
   - Microservices potential
   - Container readiness assessment

5. **Security Updates**
   - Security improvements available
   - Authentication/authorization changes
   - Compliance considerations

6. **Performance Impact**
   - Performance improvements expected
   - Potential performance issues
   - Optimization opportunities

7. **Migration Roadmap**
   - Step-by-step migration plan
   - Risk assessment for each phase
   - Rollback strategies

8. **Code Updates**
   {"- Complete migrated code examples" if include_migration_code else "- High-level code change guidance"}
   - Required code modifications
   - Best practice implementations

9. **Testing Strategy**
   - Migration testing approach
   - Validation procedures
   - Regression testing recommendations

10. **Risk Mitigation**
    - Identified risks and mitigation strategies
    - Critical success factors
    - Contingency planning

Format with clear sections, actionable recommendations, and practical implementation guidance.
Focus on proven migration patterns and TIBCO best practices.
"""

        try:
            response = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an expert TIBCO BusinessWorks migration architect specializing in version migrations and platform modernization."},
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