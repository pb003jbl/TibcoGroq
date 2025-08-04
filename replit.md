# TIBCO Developer Assistant

## Overview

This project is a Streamlit-based web application that serves as an intelligent assistant for TIBCO BusinessWorks developers. The application leverages Groq's AI models (particularly Llama 3.3 70b) to analyze TIBCO BusinessWorks code and XML, automatically generating comprehensive test cases and providing code analysis capabilities. The tool is designed to streamline the testing process for TIBCO developers by providing intelligent test scenario generation based on uploaded process definitions.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
The application uses **Streamlit** as the web framework, providing a clean and interactive user interface. The frontend is configured with a wide layout and expandable sidebar for better user experience. The interface includes:
- Main content area for code input and results display
- Sidebar for configuration options including AI model selection
- Real-time formatting and display of generated test cases
- Error handling and user feedback mechanisms

### Backend Architecture
The backend follows a **modular service-oriented design** with clear separation of concerns:
- **GroqClient**: Handles all AI model interactions and API communications
- **Formatters**: Responsible for processing and formatting AI responses for display
- **Main Application**: Orchestrates the overall application flow and user interactions

The architecture uses **caching strategies** (`@st.cache_resource`) to optimize API client initialization and reduce redundant operations.

### AI Integration Pattern
The system implements a **prompt-based AI interaction model** where:
- Structured prompts are crafted for specific TIBCO BusinessWorks analysis tasks
- Multiple Groq models are supported with configurable selection
- Responses are processed and formatted for optimal readability
- Error handling ensures graceful degradation when API issues occur

### Data Processing Flow
The application follows a **linear processing pipeline**:
1. User inputs TIBCO code/XML through the web interface
2. Code is passed to the GroqClient with specific testing parameters
3. AI generates comprehensive test cases based on TIBCO best practices
4. Formatters process the raw AI output for improved presentation
5. Results are displayed with proper formatting and structure

## External Dependencies

### AI Service Integration
- **Groq API**: Primary AI service provider using Llama 3.3 70b and other models
- **API Key Management**: Environment variable-based configuration for secure API access

### Python Libraries
- **Streamlit**: Web application framework for the user interface
- **Groq Python SDK**: Official client library for Groq API interactions
- **Regular Expressions (re)**: Text processing and formatting utilities
- **OS Module**: Environment variable management and system interactions

### Model Support
The application supports multiple Groq AI models:
- llama-3.3-70b-versatile (primary/default)
- llama-3.1-70b-versatile
- llama-3.1-8b-instant
- mixtral-8x7b-32768

### Environment Configuration
- **GROQ_API_KEY**: Required environment variable for API authentication
- **Runtime Dependencies**: Standard Python environment with Streamlit deployment capabilities