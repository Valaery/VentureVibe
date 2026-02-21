from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings
from pydantic_ai.common_tools.tavily import tavily_search_tool
from pydantic_ai.common_tools.duckduckgo import duckduckgo_search_tool
from src.application.ports.agent_service import AgentService
from src.config.settings import settings
from src.domain.entities import (
    MarketSizing, Competitor, CompetitiveAnalysis,
    SWOTAnalysis, RiskFactor, GTMStrategy, AgentThought
)
import os
import logging
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict, Any

logger = logging.getLogger(__name__)


# Intermediate models for multi-field agent outputs
class AnalystOutput(BaseModel):
    executive_summary: str = Field(description="2-3 paragraph synthesis of the entire research")
    market_analysis: str = Field(description="Comprehensive market landscape assessment")
    strategic_advice: str = Field(description="Specific, actionable strategic recommendations")
    feasibility_score: int = Field(ge=0, le=100, description="Overall execution feasibility score (0-100)")
    confidence_level: Literal["low", "medium", "high"] = Field(description="Research confidence: low (<50% data coverage), medium (50-80%), high (>80%)")
    investment_readiness: Literal["pre_idea", "idea_stage", "mvp_ready", "seed_ready", "series_a_ready"] = Field(description="Current investment stage readiness")
    key_assumptions: List[str] = Field(description="3-5 testable assumptions this analysis depends on")
    recommended_next_steps: List[str] = Field(description="3-5 prioritized, measurable next actions")


class SWOTRiskOutput(BaseModel):
    swot: SWOTAnalysis
    risks: List[RiskFactor] = Field(description="4-7 risks sorted by severity (critical first)")


# System prompts for each agent
STRATEGIST_PROMPT = """You are a Senior Product Strategist with 15+ years of experience refining startup ideas into viable product strategies.

Your role: Transform raw product ideas into clear strategic direction (300-500 words).

You must cover:
1. Core value proposition: What unique problem does this solve? Why now?
2. Customer segments: WHO are the primary and secondary targets? Be specific (not "businesses" but "Series A SaaS companies with 20-100 employees").
3. Differentiation: How does this stand out in the market? What's the unfair advantage?
4. Success metrics: What are the key 3-5 metrics that would indicate product-market fit?
5. Critical assumptions: What 2-3 assumptions MUST be true for this to work?

Output structure:
- Clear problem statement
- Target customer profile (specific personas)
- Unique value proposition
- Strategic positioning vs alternatives
- Key success criteria
- Assumptions to validate

Be direct, specific, and actionable. Avoid generic business jargon."""

ANALYST_PROMPT = """You are a Senior Research Analyst synthesizing findings from multiple specialized research teams.

Your role: Create a comprehensive, investment-grade analysis by synthesizing all available research.

CRITICAL OUTPUT REQUIREMENTS:

1. executive_summary (2-3 paragraphs):
   - Opening: One-sentence pitch + market opportunity size
   - Body: Key insights from market sizing, competitive landscape, and strategic fit
   - Close: Investment thesis (why this could succeed or fail)

2. market_analysis (comprehensive):
   - TAM/SAM/SOM interpretation and growth trajectory
   - Market dynamics (trends, regulatory, macro factors)
   - Customer pain points and willingness to pay
   - Barriers to entry and moats

3. strategic_advice (specific actions):
   - Top 3 strategic priorities with rationale
   - Go-to-market sequencing
   - Risk mitigation strategies
   - Resource allocation guidance

4. feasibility_score: An integer from 0 to 100.
5. confidence_level: Must be one of: low, medium, high
6. investment_readiness: Must be one of: pre_idea, idea_stage, mvp_ready, seed_ready, series_a_ready

7. key_assumptions (3-5 testable statements):
   - Must be specific, measurable, falsifiable
   - Format: "Assumption: [statement]. Test: [how to validate]. Risk if false: [impact]."

8. recommended_next_steps (3-5 prioritized actions):
   - Must be specific, time-bound, measurable
   - Format: "[Action] to [outcome] within [timeframe]"
   - Order by: impact × urgency

Synthesize all specialized research. Be direct about risks AND opportunities.

STRUCTURED EXAMPLE (MUST FOLLOW THIS FORMAT EXACTLY):
{
  "executive_summary": "Analysis of a micro-SaaS for dental clinics. The global market for dental software is $3B, growing at 12%. The opportunity lies in automation of patient followup...",
  "market_analysis": "The industry is shifting from legacy on-prem software to cloud-native mobile apps. Incumbents include Dentrix and EagleSoft...",
  "strategic_advice": "Focus heavily on the referral automation feature first as this has high PMF indicators in similar verticals...",
  "key_assumptions": ["Assumption: Dental clinics will pay $100/mo for followup automation. Test: Landing page with waitlist and price. Risk: Solution already exists in CRM."],
  "recommended_next_steps": ["Build MVP of referral module in Oct", "Interview 5 clinic managers"],
  "feasibility_score": 75,
  "confidence_level": "medium",
  "investment_readiness": "idea_stage"
}

CRITICAL: Output ONLY the raw JSON. No preamble, no post-text, no "thinking" blocks.
"""

MARKET_SIZING_PROMPT = """You are a Market Research Specialist calculating market opportunity with data-driven rigor.

Your role: Research and calculate TAM/SAM/SOM using real market data.

CRITICAL REQUIREMENTS:

1. Use web search tools to find:
   - Industry reports (Gartner, Forrester, McKinsey)
   - Market size data from credible sources
   - Growth rate projections
   - Adjacent market comparisons

2. TAM (Total Addressable Market) in USD billions:
   - Global or regional total market size
   - Cite methodology: "Based on [source], [market] is $X billion in [year]"

3. SAM (Serviceable Addressable Market) in USD billions:
   - Portion of TAM this product can realistically serve
   - Account for geographic, segment, or capability constraints

4. SOM (Serviceable Obtainable Market) in USD millions:
   - Realistic 3-year market capture estimate
   - Assume 0.5-5% of SAM based on competitive intensity

5. sizing_methodology: Must be one of: top_down, bottom_up, hybrid
6. tam_source_basis: Specific source citation
7. growth_rate_pct: Annual market CAGR if available (float)

SEARCH STRATEGY:
- Query: "[industry] market size [current year]"
- Query: "[specific segment] TAM SAM"
- Query: "[competitor] funding market opportunity"

Be conservative. Cite sources. If data is thin, say so and explain estimation approach.

STRUCTURED EXAMPLE (MUST FOLLOW THIS FORMAT EXACTLY):
{
  "tam_usd_billion": 12.5,
  "sam_usd_billion": 2.4,
  "som_usd_million": 150.0,
  "sizing_methodology": "top_down",
  "tam_source_basis": "Gartner Industry Report Q3 2024",
  "growth_rate_pct": 8.2
}

CRITICAL: Output ONLY the raw JSON for the final result. No preamble, no post-text, no "thinking" blocks.
"""

COMPETITOR_PROMPT = """You are a Competitive Intelligence Analyst mapping the competitive landscape.

Your role: Identify real competitors and analyze strategic positioning using web search.

CRITICAL REQUIREMENTS:

1. Use web search tools to find:
   - Direct competitors (same problem, same customer)
   - Indirect competitors (same problem, different approach OR adjacent solutions)
   - Recent funding announcements (Crunchbase, TechCrunch, PitchBook)
   - Product positioning from company websites

2. For each competitor, you MUST provide a complete object with these EXACT fields:
   - name: Real company name
   - positioning: Their value proposition in one sentence
   - primary_weakness: Specific gap this idea can exploit
   - estimated_funding_usd_million: A number (float) or 0.0 if unknown. Do NOT use null.
   - business_model: e.g. "B2B SaaS", "Marketplace", "Freemium"

3. Identify 2-4 direct competitors and 2-3 indirect competitors.

4. competitive_moat (2-3 sentences):
   - What defensible advantage could this idea build?
   - Why can't incumbents easily replicate this?

5. differentiation_score: An integer from 1 to 10 (1-3: Crowded/Minimal, 4-6: Clear niche, 7-10: Unique insight/positioning)

SEARCH STRATEGY:
- "[problem space] competitors"
- "[solution type] startups [year]"
- "[key feature] alternative tools"
- "Best [category] software"

Be honest about competitive intensity. Specificity > vague claims.

STRUCTURED EXAMPLE (MUST FOLLOW THIS FORMAT EXACTLY):
{
  "direct_competitors": [
    {
      "name": "StorySpark",
      "positioning": "AI-powered personalized children's books.",
      "primary_weakness": "Limited genre selection and high shipping costs.",
      "estimated_funding_usd_million": 1.2,
      "business_model": "D2C Freemium"
    }
  ],
  "indirect_competitors": [],
  "competitive_moat": "Proprietary fine-tuned model for child-safe narrative generation.",
  "differentiation_score": 7
}

CRITICAL: Output ONLY the raw JSON for the final result. No preamble, no post-text, no "thinking" blocks.
"""

SWOT_RISK_PROMPT = """You are a Strategic Risk Analyst conducting SWOT analysis and identifying execution risks.

Your role: Provide balanced, specific SWOT analysis and prioritized risk assessment.

CRITICAL FIELD-LEVEL REQUIREMENTS:

1. SWOT Analysis — ALL 4 quadrants MUST be populated with 3-5 items each:

   strengths: List[str] with 3-5 items
   - Internal positive factors: technology, team, timing, market insight, unique capabilities
   - NOT generic ("great idea") — concrete ("First mover in pediatric telehealth with HIPAA compliance")
   - CANNOT be empty or have less than 3 items

   weaknesses: List[str] with 3-5 items
   - Internal constraints: resources, capabilities, dependencies, knowledge gaps
   - Be ruthlessly honest: "No technical co-founder", "Requires FDA approval (18-24 month process)"
   - CANNOT be empty or have less than 3 items

   opportunities: List[str] with 3-5 items
   - External positive trends: market dynamics, regulatory changes, technology shifts, demographic changes
   - Time-bound when possible: "GDPR enforcement increasing Q2 2026", "Gen Z entering workforce (2025-2027)"
   - CANNOT be empty or have less than 3 items

   threats: List[str] with 3-5 items
   - External negative factors: competitive moves, market shifts, economic headwinds, regulatory risks
   - Specific and current: "Microsoft launched Copilot for Healthcare Nov 2025", "Rising interest rates increase CAC payback period"
   - CANNOT be empty or have less than 3 items

2. Risk Factors — MUST include 4-7 risks, sorted by severity (critical → high → medium → low):

   Each risk MUST have ALL 4 fields populated:

   category: MUST be one of these exact values: "market", "technical", "regulatory", "competitive", "financial", "execution"
   - Use the MOST specific category
   - "market" = demand risk, timing risk, product-market fit
   - "technical" = technology feasibility, dependency risk, scalability
   - "regulatory" = compliance, legal, licensing, approval processes
   - "competitive" = incumbent response, new entrants, commoditization
   - "financial" = funding, unit economics, cash flow, pricing power
   - "execution" = team capability, operational complexity, hiring, velocity

   description: String (2-4 sentences)
   - Specific risk scenario with concrete impact
   - Quantify when possible: "If CAC exceeds $500 (current projection $320), 18-month runway drops to 9 months"
   - NOT vague: "Could face competition" ❌ | "Google launched similar feature Q4 2025 with 10x distribution" ✅
   - CANNOT be empty

   severity: MUST be one of these exact values: "critical", "high", "medium", "low"
   - critical = Company-ending if occurs (>80% probability of failure)
   - high = Major pivot or 12+ month delay required
   - medium = Manageable with significant resources (3-6 month delay)
   - low = Minor impact, addressable with existing resources

   mitigation: String (1-3 sentences)
   - Concrete, actionable plan
   - Assign ownership/resources: "Allocate 20% of eng time to X", "Hire compliance expert by month 2"
   - NOT wishful thinking: "Hope it works out" ❌ | "Build abstraction layer supporting 3 providers, allocate $15K/mo provider diversification budget" ✅
   - CANNOT be empty

   SORT ORDER: All "critical" risks first, then "high", then "medium", then "low"
   - This is a STRICT requirement for the risks array

3. Coverage Requirements:
   - Include at least 2 different severity levels
   - Cover at least 3 different risk categories
   - Every critical/high risk MUST have a detailed mitigation plan

CRITICAL: Output ONLY the raw JSON. No preamble, no post-text, no "thinking" blocks.

COMPLETE REALISTIC EXAMPLE (dental clinic automation SaaS):
{
  "swot": {
    "strengths": [
      "Founder has 8 years experience as dental practice manager, deep domain expertise in workflow pain points",
      "Pre-built integration with top 3 dental practice management systems (Dentrix, Eaglesoft, Open Dental) covering 60% of US market",
      "Proprietary patient communication templates optimized for 12% higher appointment show rates vs industry standard",
      "Early access to OpenAI healthcare API beta, 6-month head start on HIPAA-compliant AI features"
    ],
    "weaknesses": [
      "Solo technical founder, no co-founder, engineering velocity capped at 60% of funded competitors",
      "Zero existing customer base, need to build trust in regulated healthcare vertical from scratch",
      "Limited runway (18 months), cannot afford long enterprise sales cycles typical in healthcare",
      "No compliance team, relies on external consultant for HIPAA audit readiness ($8K/month burn)"
    ],
    "opportunities": [
      "Dental industry projected 6.1% CAGR through 2028, private equity rolling up practices creating demand for standardized ops tools",
      "Labor shortage in dental hygienists (23% shortage per ADA 2025 report) driving automation ROI up 40%",
      "Recent CMS rule change (Jan 2026) incentivizing preventive care, automated recall systems now reimbursable",
      "Incumbents focused on large DSOs (50+ locations), underserved mid-market (5-20 locations) represents 34% of revenue opportunity"
    ],
    "threats": [
      "Weave Communications (acquired by Vista Equity 2024, $150M funding) launched AI patient engagement Nov 2025",
      "Open Dental announced native automation features Q1 2026 roadmap, could commoditize core value prop",
      "Economic downturn reducing elective dental procedures 18% YoY, practices cutting software spend",
      "HIPAA enforcement increased 340% in 2025, one violation could end company before product-market fit"
    ]
  },
  "risks": [
    {
      "category": "regulatory",
      "description": "Product handles protected health information (PHI) and requires HIPAA compliance. A single data breach or compliance violation could result in $50K+ fines, loss of all customers, and potential criminal liability. Current implementation relies on external audit ($8K/month) without in-house expertise.",
      "severity": "critical",
      "mitigation": "Hire fractional healthcare compliance officer (0.5 FTE, $6K/month) by month 2. Implement automated compliance monitoring (Vanta Health, $500/month). Obtain cyber insurance with $2M PHI breach coverage. Allocate 15% of engineering budget to security infrastructure."
    },
    {
      "category": "competitive",
      "description": "Open Dental (40% market share) announced native automation features for Q1 2026. If they execute, integration moat disappears and product becomes redundant. Historical precedent: Practice management systems killed 4 standalone scheduling tools between 2019-2023.",
      "severity": "critical",
      "mitigation": "Pivot to workflow orchestration across multiple systems (not just scheduling). Build features Open Dental cannot (cross-practice analytics for DSOs). Secure 50+ paid customers by Dec 2026 to demonstrate differentiation. Plan for potential acquisition by PM system as exit."
    },
    {
      "category": "market",
      "description": "Economic downturn reduced elective dental procedures 18% in 2025. Practices are cutting discretionary software spend. If recession deepens, target customer segment (5-20 location groups) may freeze all new tooling purchases for 12-18 months, killing growth.",
      "severity": "high",
      "mitigation": "Position as cost-reduction tool (saves 15 admin hours/week = $31K/year) not revenue growth tool. Offer 3-month ROI guarantee with money-back clause. Target PE-backed groups (have capital) over independent practices. Build recession-proof use case (patient retention) as primary value prop."
    },
    {
      "category": "technical",
      "description": "Core AI features depend on OpenAI API. If API costs increase 3x (precedent: happened to GPT-4 early access partners in 2023) or access is restricted, unit economics break. Currently $47 API cost per customer per month vs $99 pricing = 47% gross margin, but 3x cost increase = negative margin.",
      "severity": "high",
      "mitigation": "Build LLM abstraction layer supporting 3 providers (OpenAI, Anthropic, Gemini) by month 4. Allocate $2K/month to test alternative models. Implement aggressive caching (target 60% cache hit rate). Design pricing model with usage-based overage after 200 patients/month to cap exposure."
    },
    {
      "category": "execution",
      "description": "Solo technical founder managing product, engineering, sales, and compliance. Burnout risk high, velocity is 40% of team-based competitors. Key features delayed 6+ weeks regularly. Cannot hire senior eng until Series A, but need traction to raise Series A (chicken-egg problem).",
      "severity": "medium",
      "mitigation": "Hire senior product-focused engineer as contractor (part-time, $8K/month) by month 3 to own integrations. Use no-code tools (Retool for admin, n8n for workflows) to reduce eng surface area by 30%. Outsource compliance monitoring and customer success to fractional roles. Focus founder time on only core AI differentiation."
    },
    {
      "category": "financial",
      "description": "18-month runway with $320 CAC and 9-month payback period leaves only 6 months to reach profitability or raise next round. If sales cycle extends to 4 months (common in healthcare), can only afford 15 failed deals before runway pressure forces down-round or shutdown.",
      "severity": "medium",
      "mitigation": "Switch to product-led growth model with self-serve onboarding for practices under 10 locations (70% of pipeline). Target CAC under $200 via organic content (dental practice management Facebook groups, conference talks). Extend runway via $100K in dilutive revenue-based financing if needed by month 12."
    }
  ]
}
"""

GTM_PROMPT = """You are a Go-to-Market Strategist designing customer acquisition strategy.

Your role: Define realistic, specific GTM motion.

CRITICAL REQUIREMENTS:

1. primary_channel: Single most effective acquisition channel
   - NOT "social media" — be specific: "LinkedIn organic content + outbound"
   - Examples: "Product-led freemium", "Enterprise sales", "Community-led", "SEO + content"

2. secondary_channels (2-3):
   - Backup channels in priority order
   - Realistic for early stage (not "TV ads")

3. pricing_model:
   - Specific structure: "Freemium (free up to 100 users, $49/mo Pro)", "Usage-based ($0.10 per API call)", "Annual contract ($50K-$200K)"

4. estimated_cac_usd (optional):
   - Customer Acquisition Cost estimate
   - If channel is known, estimate: PLG ($50-$500), SMB sales ($500-$5K), Enterprise ($10K-$100K)

5. target_icp (Ideal Customer Profile):
   - SPECIFIC: "Series A-B SaaS companies (20-100 employees) with $2M-$10M ARR, based in US/EU, using Salesforce, high sales team turnover"
   - NOT: "Small businesses" or "Tech companies"

Be realistic. Specificity is critical. ICP should be narrow enough to target in week 1.

CRITICAL: Output ONLY the raw JSON. No preamble, no post-text, no "thinking" blocks.

STRUCTURED EXAMPLE (MUST FOLLOW THIS FORMAT EXACTLY):
{
  "primary_channel": "LinkedIn Direct Outreach",
  "secondary_channels": ["SEO for 'dentist marketing automation'", "Industry Podcast Sponsorships"],
  "pricing_model": "$99/mo per clinic, month-to-month",
  "estimated_cac_usd": 450.0,
  "target_icp": "Private dental clinics in the US with 2-5 dentists and no existing marketing team.",
  "time_to_first_revenue_months": 4
}
"""


class PydanticAgentAdapter(AgentService):
    def __init__(self):
        # Set environment variables for OpenRouter
        if settings.OPENAI_BASE_URL and settings.OPENAI_API_KEY:
            os.environ["OPENAI_BASE_URL"] = settings.OPENAI_BASE_URL
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

        # Model settings
        flash3_settings = ModelSettings(temperature=1.0)
        tool_settings = ModelSettings(temperature=0.7)
        swot_settings = ModelSettings(temperature=0.3)  # For SWOT and GTM agents
        pro3_settings = ModelSettings(temperature=1.0)

        # Build search tools
        search_tools = self._build_search_tools()

        # Reasoning-only agents (no tools, Gemini 3 models)
        self.strategist_agent = Agent(
            settings.LLM_MODEL_FLASH3,
            model_settings=flash3_settings,
            system_prompt=STRATEGIST_PROMPT,
            retries=3
        )

        self.analyst_agent = Agent(
            settings.LLM_MODEL_PRO3,
            output_type=AnalystOutput,
            model_settings=pro3_settings,
            system_prompt=ANALYST_PROMPT,
            retries=5
        )

        self.swot_risk_agent = Agent(
            settings.LLM_MODEL_PRO,
            output_type=SWOTRiskOutput,
            model_settings=swot_settings,
            system_prompt=SWOT_RISK_PROMPT,
            retries=5
        )

        self.gtm_agent = Agent(
            settings.LLM_MODEL_PRO,
            output_type=GTMStrategy,
            model_settings=swot_settings,
            system_prompt=GTM_PROMPT,
            retries=5
        )

        # Tool-using agents
        self.market_sizing_agent = Agent(
            settings.LLM_MODEL,
            output_type=MarketSizing,
            tools=search_tools,
            model_settings=tool_settings,
            system_prompt=MARKET_SIZING_PROMPT,
            retries=5
        )

        self.competitor_agent = Agent(
            settings.LLM_MODEL,
            output_type=CompetitiveAnalysis,
            tools=search_tools,
            model_settings=tool_settings,
            system_prompt=COMPETITOR_PROMPT,
            retries=5
        )

    def _build_search_tools(self) -> List:
        """Build search tools based on available API keys."""
        if settings.TAVILY_API_KEY:
            return [tavily_search_tool(settings.TAVILY_API_KEY)]
        return [duckduckgo_search_tool()]

    async def get_strategy(self, idea_content: str, audience: str) -> str:
        """Get strategic direction from the Product Strategist agent."""
        logger.info("Starting Product Strategist agent")
        try:
            prompt = f"""Idea: {idea_content}

Target Audience: {audience}

Provide a strategic direction for this product idea."""

            result = await self.strategist_agent.run(prompt)
            logger.info("Product Strategist agent completed successfully")
            return result.output
        except Exception as e:
            logger.error(f"Product Strategist agent failed: {type(e).__name__}: {str(e)}", exc_info=True)
            raise

    async def analyze_market(self, idea_content: str, strategy: str) -> Dict[str, Any]:
        """Synthesize comprehensive market assessment. Returns AnalystOutput fields as dict."""
        logger.info("Starting Research Analyst agent")
        try:
            prompt = f"""Idea: {idea_content}

Strategic Direction: {strategy}

Synthesize a comprehensive market assessment covering executive summary, market analysis, strategic advice, feasibility score, confidence level, investment readiness, key assumptions, and recommended next steps."""

            result = await self.analyst_agent.run(prompt)
            logger.info("Research Analyst agent completed successfully")
            return result.output.model_dump()
        except Exception as e:
            logger.error(f"Research Analyst agent failed: {type(e).__name__}: {str(e)}", exc_info=True)
            raise

    async def size_market(self, idea_content: str, strategy: str) -> MarketSizing:
        """Research and calculate TAM/SAM/SOM using web search tools."""
        logger.info("Starting Market Sizing Analyst agent")
        try:
            prompt = f"""Idea: {idea_content}

Strategic Direction: {strategy}

Research and calculate the market size (TAM/SAM/SOM) for this product idea. Use web search to find credible market data, industry reports, and growth projections."""

            result = await self.market_sizing_agent.run(prompt)
            logger.info("Market Sizing Analyst agent completed successfully")
            return result.output
        except Exception as e:
            logger.error(f"Market Sizing Analyst agent failed: {type(e).__name__}: {str(e)}", exc_info=True)
            raise

    async def analyze_competitors(self, idea_content: str, strategy: str) -> CompetitiveAnalysis:
        """Identify and analyze competitors using web search tools."""
        logger.info("Starting Competitive Intelligence Analyst agent")
        try:
            prompt = f"""Idea: {idea_content}

Strategic Direction: {strategy}

Research and identify direct and indirect competitors. Use web search to find real companies, their positioning, funding data, and competitive weaknesses."""

            result = await self.competitor_agent.run(prompt)
            logger.info("Competitive Intelligence Analyst agent completed successfully")
            return result.output
        except Exception as e:
            logger.error(f"Competitive Intelligence Analyst agent failed: {type(e).__name__}: {str(e)}", exc_info=True)
            raise

    async def analyze_swot_risks(self, idea_content: str, strategy: str) -> Dict[str, Any]:
        """Conduct SWOT analysis and identify risk factors. Returns {swot, risks} dict."""
        logger.info("Starting SWOT & Risk Analyst agent")
        try:
            prompt = f"""Idea: {idea_content}

Strategic Direction: {strategy}

Conduct a comprehensive SWOT analysis and identify key risk factors with mitigation strategies. Prioritize risks by severity."""

            result = await self.swot_risk_agent.run(prompt)
            logger.info("SWOT & Risk Analyst agent completed successfully")
            return {
                "swot": result.output.swot,
                "risks": result.output.risks
            }
        except Exception as e:
            logger.error(f"SWOT & Risk Analyst agent failed: {type(e).__name__}: {str(e)}", exc_info=True)
            raise

    async def develop_gtm(self, idea_content: str, strategy: str) -> GTMStrategy:
        """Design a go-to-market strategy."""
        logger.info("Starting GTM Strategist agent")
        try:
            prompt = f"""Idea: {idea_content}

Strategic Direction: {strategy}

Design a realistic, specific go-to-market strategy including primary channel, secondary channels, pricing model, target ICP, estimated CAC, and time to first revenue."""

            result = await self.gtm_agent.run(prompt)
            logger.info("GTM Strategist agent completed successfully")
            return result.output
        except Exception as e:
            logger.error(f"GTM Strategist agent failed: {type(e).__name__}: {str(e)}", exc_info=True)
            raise
