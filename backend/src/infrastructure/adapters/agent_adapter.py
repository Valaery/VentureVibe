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

4. feasibility_score (0-100):
   - 0-25: Critical blockers exist
   - 26-50: Significant challenges, requires pivots
   - 51-75: Viable with execution risk
   - 76-100: Strong fundamentals, clear path

5. confidence_level:
   - low: <50% of key data points validated
   - medium: 50-80% data coverage
   - high: >80% data coverage with credible sources

6. investment_readiness:
   - pre_idea: Concept only, no validation
   - idea_stage: Problem validated, solution hypothesis formed
   - mvp_ready: Clear customer segment, ready to build
   - seed_ready: MVP built, initial traction/validation
   - series_a_ready: Product-market fit demonstrated, ready to scale

7. key_assumptions (3-5 testable statements):
   - Must be specific, measurable, falsifiable
   - Format: "Assumption: [statement]. Test: [how to validate]. Risk if false: [impact]."

8. recommended_next_steps (3-5 prioritized actions):
   - Must be specific, time-bound, measurable
   - Format: "[Action] to [outcome] within [timeframe]"
   - Order by: impact × urgency

Synthesize all specialized research. Be direct about risks AND opportunities."""

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

5. sizing_methodology:
   - top_down: Industry total → segment down
   - bottom_up: Unit economics × target customers
   - hybrid: Cross-validate both approaches

6. tam_source_basis:
   - Cite specific source: "[Report name] by [org], [year]"
   - If no source found, state: "Estimated based on adjacent market [X]"

7. growth_rate_pct (optional):
   - Annual market CAGR if available

SEARCH STRATEGY:
- Query: "[industry] market size [current year]"
- Query: "[specific segment] TAM SAM"
- Query: "[competitor] funding market opportunity"

Be conservative. Cite sources. If data is thin, say so and explain estimation approach."""

COMPETITOR_PROMPT = """You are a Competitive Intelligence Analyst mapping the competitive landscape.

Your role: Identify real competitors and analyze strategic positioning using web search.

CRITICAL REQUIREMENTS:

1. Use web search tools to find:
   - Direct competitors (same problem, same customer)
   - Indirect competitors (same problem, different approach OR adjacent solutions)
   - Recent funding announcements (Crunchbase, TechCrunch, PitchBook)
   - Product positioning from company websites

2. For each competitor (Competitor model):
   - name: Real company name
   - positioning: Their value proposition in one sentence
   - primary_weakness: Specific gap this idea can exploit (NOT generic like "expensive" — be specific: "Enterprise-only, no SMB offering" or "Complex setup, 2-week onboarding")
   - estimated_funding_usd_million: Total funding raised (search "[company] funding")
   - business_model: "B2B SaaS", "Marketplace", "Freemium", etc.

3. Identify 2-4 direct competitors and 2-3 indirect competitors.

4. competitive_moat (2-3 sentences):
   - What defensible advantage could this idea build?
   - Why can't incumbents easily replicate this?

5. differentiation_score (1-10):
   - 1-3: Crowded space, minimal differentiation
   - 4-6: Clear niche or approach difference
   - 7-10: Unique insight, technology, or market positioning

SEARCH STRATEGY:
- "[problem space] competitors"
- "[solution type] startups [year]"
- "[key feature] alternative tools"
- "Best [category] software"

Be honest about competitive intensity. Specificity > vague claims."""

SWOT_RISK_PROMPT = """You are a Strategic Risk Analyst conducting SWOT analysis and identifying execution risks.

Your role: Provide balanced, specific SWOT analysis and prioritized risk assessment.

CRITICAL REQUIREMENTS:

1. SWOT Analysis (3-5 items per quadrant):

   Strengths (internal, positive):
   - Specific advantages: technology, team, timing, insight
   - Not generic ("great idea") — concrete ("First mover in X regulated industry")

   Weaknesses (internal, negative):
   - Real constraints: resources, capabilities, dependencies
   - Be honest: "No technical co-founder", "Requires regulatory approval"

   Opportunities (external, positive):
   - Market trends, regulatory changes, technology shifts
   - Time-bound: "New regulation takes effect Q3 2026"

   Threats (external, negative):
   - Competitive moves, market shifts, economic factors
   - Specific: "Incumbent X launched competing feature last month"

2. Risk Factors (4-7 risks, sorted by severity):

   For each risk:
   - category: market | technical | regulatory | competitive | financial | execution
   - description: Specific risk scenario (2-3 sentences)
   - severity: critical (business-ending) > high (major setback) > medium (manageable delay) > low (minor friction)
   - mitigation: Concrete action to reduce likelihood or impact

   Sort order: All critical first, then high, then medium, then low.

   Example:
   - Category: technical
   - Description: "Core NLP feature depends on OpenAI API. If API costs increase 3x (happened in 2023) or access is restricted, unit economics break and product becomes unviable without 12-month rebuild."
   - Severity: critical
   - Mitigation: "Build abstraction layer supporting 3 LLM providers (OpenAI, Anthropic, open-source). Allocate 15% of eng budget to provider redundancy."

Be specific. Prioritize ruthlessly. Every critical risk needs a mitigation plan."""

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

6. time_to_first_revenue_months (integer):
   - Realistic timeline from $0 to first dollar of revenue
   - PLG: 1-3 months
   - SMB sales: 3-6 months
   - Enterprise: 6-12 months

Be realistic. Specificity is critical. ICP should be narrow enough to target in week 1."""


class PydanticAgentAdapter(AgentService):
    def __init__(self):
        # Set environment variables for OpenRouter
        if settings.OPENAI_BASE_URL and settings.OPENAI_API_KEY:
            os.environ["OPENAI_BASE_URL"] = settings.OPENAI_BASE_URL
            os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY

        # Model settings
        flash3_settings = ModelSettings(temperature=1.0)
        tool_settings = ModelSettings(temperature=0.7)
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
            retries=3
        )

        self.swot_risk_agent = Agent(
            settings.LLM_MODEL_FLASH3,
            output_type=SWOTRiskOutput,
            model_settings=flash3_settings,
            system_prompt=SWOT_RISK_PROMPT,
            retries=3
        )

        self.gtm_agent = Agent(
            settings.LLM_MODEL_FLASH3,
            output_type=GTMStrategy,
            model_settings=flash3_settings,
            system_prompt=GTM_PROMPT,
            retries=3
        )

        # Tool-using agents (Gemini 2.5 Flash for stable multi-turn tool use)
        self.market_sizing_agent = Agent(
            settings.LLM_MODEL,
            output_type=MarketSizing,
            tools=search_tools,
            model_settings=tool_settings,
            system_prompt=MARKET_SIZING_PROMPT,
            retries=3
        )

        self.competitor_agent = Agent(
            settings.LLM_MODEL,
            output_type=CompetitiveAnalysis,
            tools=search_tools,
            model_settings=tool_settings,
            system_prompt=COMPETITOR_PROMPT,
            retries=3
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
