# Market Research Multi-Agent System

## Overview
An intelligent system that leverages multiple AI agents to conduct comprehensive market research, generate AI use cases, and provide implementation resources for any company or industry. The system uses the AutoGen framework for agent orchestration, Azure OpenAI for language capabilities, and Tavily for real-time web research.

## Features
- Real-time market research and analysis
- AI/ML use case generation
- Technical resource identification
- Web-based user interface
- Automated report generation
- Export options (Markdown & JSON)

## System Architecture
The system consists of five specialized agents:
1. Project Manager Agent: Orchestrates the analysis workflow
2. Industry Researcher Agent: Conducts market analysis
3. Solutions Architect Agent: Generates AI use cases
4. Technical Resource Agent: Identifies implementation resources
5. User Proxy Agent: Manages user interaction

## Prerequisites
- Python 3.8+
- Azure OpenAI API access
- Tavily API key
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd market-research-agents
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file with the following:
```env
AZURE_API_KEY=your_azure_api_key
AZURE_API_VERSION=your_api_version
AZURE_API_BASE=your_api_base_url
AZURE_DEPLOYMENT_NAME=your_deployment_name
TAVILY_API_KEY=your_tavily_api_key
```

## Usage

### Command Line Interface
Run the analysis through command line:
```bash
python main3.py
```

### Streamlit Web Interface
Launch the web application:
```bash
streamlit run streamlit_app1.py
```

Access the application at `http://localhost:8501`

## Project Structure
```
market-research-agents/
├── main3.py               # Core agent system implementation
├── streamlit_app1.py      # Web interface implementation
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables
└── README.md            # Project documentation
```

## Features Explained

### Market Research
- Real-time web data gathering
- Industry trend analysis
- Competitive landscape assessment
- Market positioning evaluation

### AI Use Case Generation
- Operational efficiency solutions
- Customer experience improvements
- Product innovation opportunities
- Business intelligence applications

### Resource Identification
- Dataset recommendations
- Implementation frameworks
- Technical requirements
- Deployment strategies

## Output Format
The system generates comprehensive reports in two formats:
1. Markdown (.md)
2. JSON

Reports include:
- Industry research and market analysis
- AI/ML use cases and implementation opportunities
- Technical resources and implementation strategy

## Environment Variables

| Variable | Description |
|----------|-------------|
| AZURE_API_KEY | Your Azure OpenAI API key |
| AZURE_API_VERSION | Azure API version |
| AZURE_API_BASE | Azure API base URL |
| AZURE_DEPLOYMENT_NAME | Azure deployment name |
| TAVILY_API_KEY | Your Tavily API key |

## Best Practices
1. Ensure all environment variables are properly set
2. Monitor API rate limits
3. Regular updates of dependencies
4. Error handling implementation

## Known Limitations
- Maximum 7 conversation rounds
- API rate limits apply
- Requires stable internet connection
- Processing time varies with complexity

## Contributing
1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License
[Specify your license here]

## Support
For support or questions, please [open an issue](link-to-issues) or contact [your-contact-info].

## Acknowledgments
- AutoGen framework
- Azure OpenAI
- Tavily Search API
- Streamlit

## Version History
- v1.0.0 (Current): Initial release