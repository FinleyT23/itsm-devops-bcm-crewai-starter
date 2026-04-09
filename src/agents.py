from crewai import Agent, LLM
from src.tools import analyze_security_event, create_incident_record, get_service_catalog, calculate_impact, failover_service, send_notification, log_lesson

ollama_llm = LLM(
    model="ollama/qwen3:8b-q4_K_M",
    base_url="http://localhost:11434",
    timeout=1200
)


def create_agents():
    detection_agent = Agent(
        role="Incident Classification Specialist",
        goal=(
            "You have exactly 3 tools: analyze_security_event, get_service_catalog, create_incident_record. "
            "Use ONLY these 3 tools. Do NOT invent or call any other tool."
        ),
        backstory=(
            "You classify incidents at FinServe. Your workflow is always the same 3 steps: "
            "Step 1: call analyze_security_event. Step 2: call get_service_catalog. "
            "Step 3: call create_incident_record. Then write your final answer. "
            "You never call any tool that is not in your tool list."
        ),
        tools=[analyze_security_event, get_service_catalog, create_incident_record],
        verbose=True,
        llm=ollama_llm,
        allow_delegation=False
    )

    impact_agent = Agent(
        role="Business Impact Analyst",
        goal=(
            "You have exactly 1 tool: calculate_impact. "
            "Use ONLY this tool. Do NOT invent or call any other tool. "
            "Call calculate_impact once per affected service, passing ONLY the service name as a string."
        ),
        backstory=(
            "You assess business impact at FinServe. Your workflow: "
            "Call calculate_impact(service='Mobile Banking'), then "
            "call calculate_impact(service='Fraud Detection'), then "
            "call calculate_impact(service='Online Transfers'). "
            "Then write your Final Answer with a prioritized recovery list. "
            "You never call any tool that is not in your tool list."
        ),
        tools=[calculate_impact],
        llm=ollama_llm,
        verbose=True,
        allow_delegation=False
    )

    recovery_agent = Agent(
        role="Recovery Engineer",
        goal=(
            "You have exactly 2 tools: failover_service and log_lesson. "
            "Use ONLY these 2 tools. Do NOT invent or call any other tool."
        ),
        backstory=(
            "You execute disaster recovery at FinServe. Your workflow: "
            "Call failover_service for each affected service, then "
            "call log_lesson to record what happened. "
            "Then write your Final Answer with the recovery plan. "
            "You never call any tool that is not in your tool list."
        ),
        tools=[failover_service, log_lesson],
        llm=ollama_llm,
        verbose=True,
        allow_delegation=False
    )

    comms_agent = Agent(
        role="Stakeholder Communicator",
        goal=(
            "You have exactly 1 tool: send_notification. "
            "Use ONLY this tool. Do NOT invent or call any other tool."
        ),
        backstory=(
            "You send stakeholder communications at FinServe. Your workflow: "
            "Call send_notification for each audience (customers, executives, regulators). "
            "Then write your Final Answer with all messages sent. "
            "You never call any tool that is not in your tool list."
        ),
        tools=[send_notification],
        llm=ollama_llm,
        verbose=True,
        allow_delegation=False
    )

    return [detection_agent, impact_agent, recovery_agent, comms_agent]