from crewai import Task
from src.agents import create_agents

agents = create_agents()

task1 = Task(
    description=(
        "The following event has been reported: {event_description}\n\n"
        "Complete these 3 steps in order using ONLY your provided tools:\n"
        "Step 1: Call the analyze_security_event tool with the event description above.\n"
        "Step 2: Call the get_service_catalog tool to list critical services.\n"
        "Step 3: Call the create_incident_record tool with the severity, event type, and affected services from Steps 1-2.\n\n"
        "After completing all 3 steps, write your Final Answer summarizing the incident.\n"
        "IMPORTANT: You have ONLY 3 tools: analyze_security_event, get_service_catalog, create_incident_record. "
        "Do NOT call any other tool."
    ),
    agent=agents[0],
    expected_output="Incident ID, severity classification, affected services, and BCM plan activation status"
)

task2 = Task(
    description="Perform full business impact assessment. Map every affected service to RTO/RPO, customer count, revenue loss, and regulatory risk. Prioritize recovery order.",
    agent=agents[1],
    expected_output="Prioritized recovery list with exact impact numbers and business justification"
)

task3 = Task(
    description="Build and execute the automated recovery plan using DevOps automation. Include failover steps, feedback loops, and estimated timestamps that meet the 4-hour RTO.",
    agent=agents[2],
    expected_output="Step-by-step numbered recovery plan with automation commands and verification steps"
)

task4 = Task(
    description="Generate and send all stakeholder communications (customers, executives, regulators). Keep messages calm, transparent, and actionable.",
    agent=agents[3],
    expected_output="Full set of ready-to-send messages with timestamps",
    context=[task1, task2, task3]
)