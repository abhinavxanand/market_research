import os
from typing import List, Dict
import autogen
from dotenv import load_dotenv
from openai import AzureOpenAI
from tavily import TavilyClient

# Load environment variables
load_dotenv()

class MarketResearchAgents:
    def __init__(self):
        # Azure OpenAI setup
        self.azure_api_key = os.getenv("AZURE_API_KEY")
        self.azure_api_version = os.getenv("AZURE_API_VERSION")
        self.azure_api_base = os.getenv("AZURE_API_BASE")
        self.azure_deployment_name = os.getenv("AZURE_DEPLOYMENT_NAME")
        
        # Tavily setup
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        self.tavily_client = TavilyClient(api_key=self.tavily_api_key)

        # Configuration for LLM
        self.llm_config = {
            "model": self.azure_deployment_name,
            "api_key": self.azure_api_key,
            "base_url": self.azure_api_base,
            "api_type": "azure",
            "api_version": self.azure_api_version,
            "temperature": 0.7,
            # "max_tokens": 1500,
            "timeout": 60,
            "seed": 42
        }

        # Initialize agents
        self.setup_agents()
        self.setup_groupchat()

    def is_termination_msg(self, message: Dict) -> bool:
        """Check if a message should terminate the conversation"""
        if not isinstance(message, dict):
            return False
            
        content = message.get("content", "").lower()
        
        if "task_complete" in content:
            return True
            
        required_components = [
            "market analysis",
            "industry trends",
            "competitor analysis", 
            "strategic focus areas",
            "ai use cases",
            "implementation resources",
            "dataset links"
        ]
        has_all_components = all(component in content.lower() for component in required_components)
        
        return has_all_components

    def perform_web_search(self, query: str, search_depth: str = "advanced") -> List[Dict]:
        """Perform a web search using Tavily API"""
        try:
            response = self.tavily_client.search(
                query=query,
                search_depth=search_depth,
                include_domains=[
                    "mckinsey.com", "deloitte.com", "gartner.com", 
                    "forrester.com", "bloomberg.com", "reuters.com",
                    "nexocode.com", "techcrunch.com", "venturebeat.com"
                ],
                max_results=8
            )
            return response.get('results', [])
        except Exception as e:
            print(f"Tavily search error: {e}")
            return []

    def setup_agents(self):
        """Initialize all agent instances with specific roles and capabilities"""
        
        # Project Manager agent
        self.project_manager = autogen.AssistantAgent(
            name="ProjectManager",
            system_message="""You are a Project Manager coordinating market research and AI use case analysis.
            
            Core responsibilities:
            1. Guide the conversation flow between agents
            2. Request specific, concise inputs from each agent
            3. Summarize findings after each stage
            4. Ensure responses stay in proper order
            5. Ensure agent generate responses in proper makedown format
            
            Workflow steps:
            1. Request industry research from IndustryResearcher
            2. After receiving research, request AI use cases from AISolutionsArchitect
            3. After receiving use cases, request resources from TechnicalResourceSpecialist
            4. Provide final summary and mark as complete
            
            When providing final summary End with: "TASK_COMPLETE: Full analysis delivered"
""",
            llm_config=self.llm_config
        )

        # Industry Research Specialist
        self.researcher = autogen.AssistantAgent(
            name="IndustryResearcher",
            system_message="""You are an expert Industry Research Specialist conducting in-depth market analysis.

Core Research Areas:
1. Company Analysis:
   - Business model and revenue streams
   - Market positioning and competitive advantages
   - Key products/services portfolio
   - Strategic focus areas and growth initiatives
   - Recent developments and future roadmap

2. Industry Analysis:
   - Market size and growth projections
   - Key industry trends and drivers
   - Regulatory landscape
   - Technology adoption patterns
   - Industry challenges and opportunities

3. Competitive Analysis:
   - Major competitors and their market share
   - Comparative analysis of offerings
   - Technology implementation by competitors
   - Industry best practices
   - Success stories and case studies

4. Technology Landscape:
   - Current state of AI/ML adoption
   - Emerging technology trends
   - Digital transformation initiatives
   - Innovation opportunities
   - Industry-specific AI applications

Research Methodology:
1. Utilize web_search function to gather current data from:
   - Industry reports (McKinsey, Deloitte, Gartner)
   - Company websites and annual reports
   - News articles and press releases
   - Academic publications
   - Technology forums and blogs

2. Analyze multiple perspectives:
   - Market dynamics
   - Customer needs
   - Operational challenges
   - Technology gaps
   - Growth opportunities

Output Requirements:
1. Structure findings in clear sections with headers
2. Include specific examples and data points
3. Cite all sources with links
4. Highlight key insights and opportunities
5. Format in proper markdown

Only speak when asked by the Project Manager and ensure all insights are actionable and relevant to AI implementation opportunities.
""",
            function_map={
                "web_search": lambda q: self.perform_web_search(q, "advanced")
            },
            llm_config=self.llm_config
        )

        # AI Solutions Architect
        self.use_case_generator = autogen.AssistantAgent(
            name="AISolutionsArchitect",
            system_message="""You are an innovative AI Solutions Architect specializing in generative AI and ML applications.

Use Case Development Focus:
1. Operational Efficiency:
   - Process automation opportunities
   - Resource optimization
   - Quality control enhancement
   - Predictive maintenance
   - Workflow optimization

2. Customer Experience:
   - Personalization engines
   - Conversational AI systems
   - Recommendation systems
   - Customer service automation
   - User engagement optimization

3. Product Innovation:
   - AI-enhanced features
   - Smart product development
   - Predictive analytics
   - Computer vision applications
   - NLP solutions

4. Business Intelligence:
   - Market trend analysis
   - Decision support systems
   - Risk assessment models
   - Performance analytics
   - Forecasting systems

Technical Evaluation Criteria:
1. Implementation Feasibility:
   - Technical requirements
   - Data availability
   - Infrastructure needs
   - Integration complexity
   - Scalability considerations

2. Impact Assessment:
   - ROI potential
   - Resource requirements
   - Timeline estimates
   - Risk factors
   - Success metrics

3. Priority Matrix:
   - Implementation effort
   - Business impact
   - Technical complexity
   - Resource availability
   - Time to value

Output Requirements:
1. Detailed use case descriptions
2. Technical requirements
3. Implementation considerations
4. Success metrics
5. Risk factors
6. Priority recommendations

Format all outputs in proper markdown with clear sections and subsections. Only speak when asked by the Project Manager and ensure all proposed solutions are practical and aligned with industry trends.
""",
            llm_config=self.llm_config
        )

        # Technical Resource Specialist
        self.resource_specialist = autogen.AssistantAgent(
            name="TechnicalResourceSpecialist",
            system_message="""You are a Technical Resource Specialist focused on AI implementation.
            Your responsibilities:
            1. For each use case, identify:
               - Relevant datasets (Kaggle/HuggingFace/GitHub)
               - Existing models and solutions
               - Implementation frameworks
            2. Provide specific resource links
            3. Suggest deployment strategies
            4. Only speak when asked by the Project Manager

Format all outputs in proper markdown with clear sections and clickable links. Only speak when asked by the Project Manager and ensure all resources are current and relevant to the proposed use cases.
""",
            llm_config=self.llm_config
        )

        # User Proxy
        self.user_proxy = autogen.UserProxyAgent(
            name="UserProxy",
            system_message="""Route requests to the group chat and monitor conversation quality.

Termination Criteria:
1. Complete analysis delivery
2. Quality requirements met:
   - Detailed research depth
   - Practical use cases
   - Feasible implementation plans
   - Clear resource documentation
   
3. Project Manager confirmation of completion

4. Maximum rounds reached""",
            human_input_mode="NEVER",
            code_execution_config=False,
            is_termination_msg=self.is_termination_msg
        )

    def setup_groupchat(self):
        """Configure the group chat for agent collaboration"""
        
        self.groupchat = autogen.GroupChat(
            agents=[
                self.project_manager,
                self.researcher,
                self.use_case_generator,
                self.resource_specialist,
                self.user_proxy
            ],
            messages=[],
            max_round=7,
            speaker_selection_method="round_robin",
            allow_repeat_speaker=True
        )

        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config
        )

    def analyze_company(self, company_name: str, industry: str = None) -> Dict:
        """Orchestrate the multi-agent analysis workflow"""
        
        initial_message = f"""
        Conduct a comprehensive analysis of {company_name}{" in the " + industry + " industry" if industry else ""}.
        
        Required Analysis Components:
        1. Industry Research:
           - Company background and market position
           - Industry trends and competitive landscape
           - Strategic focus areas and key offerings
           - Technology adoption patterns
           
        2. AI/ML Opportunities:
           - Identify potential GenAI and ML applications
           - Focus on operational efficiency
           - Customer experience enhancement
           - Innovation opportunities
           
        3. Implementation Resources:
           - Dataset availability
           - Technical requirements
           - Implementation frameworks
           - Success metrics
           
        Project Manager, please coordinate this analysis ensuring comprehensive coverage of all requirements.
        """

        self.user_proxy.initiate_chat(
            self.manager,
            message=initial_message
        )

        messages = self.groupchat.messages
        results = self._process_messages(messages, company_name)
        return results

    def _process_messages(self, messages: List[Dict], company_name: str) -> Dict:
        """Process chat messages to extract analysis results"""
        results = {
            "company": company_name,
            "research": "",
            "use_cases": "",
            "resources": ""
        }
        
        for msg in messages:
            content = msg.get("content", "")
            sender = msg.get("name", "")
            
            if sender == "IndustryResearcher":
                results["research"] += content + "\n\n"
            elif sender == "AISolutionsArchitect":
                results["use_cases"] += content + "\n\n"
            elif sender == "TechnicalResourceSpecialist":
                results["resources"] += content + "\n\n"
            
        return results
    
    def format_report(self, analysis: Dict) -> str:
        """Format the analysis results into a structured report"""
        
        report = f"""
## Industry Research and Market Analysis
{analysis['research']}

## AI/ML Use Cases and Implementation Opportunities
{analysis['use_cases']}

## Technical Resources and Implementation Strategy
{analysis['resources']}
        """
        return report

def main():
    agent_system = MarketResearchAgents()
    
    if not os.getenv("TAVILY_API_KEY"):
        raise ValueError("Please set TAVILY_API_KEY in your environment variables")
    
    company_name = "UrbanClap"
    analysis = agent_system.analyze_company(company_name, industry="")
    
    report = agent_system.format_report(analysis)
    with open(f"{company_name.lower()}_analysis.md", "w") as f:
        f.write(report)

if __name__ == "__main__":
    main()