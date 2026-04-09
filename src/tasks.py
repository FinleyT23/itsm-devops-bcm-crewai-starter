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
    description=(
        "Assess business impact for each affected service.\n\n"
        "Complete these steps using ONLY your provided tool:\n"
        "Step 1: Call calculate_impact(service='Mobile Banking')\n"
        "Step 2: Call calculate_impact(service='Fraud Detection')\n"
        "Step 3: Call calculate_impact(service='Online Transfers')\n\n"
        "After all 3 calls, write your Final Answer with a prioritized recovery list.\n"
        "IMPORTANT: You have ONLY 1 tool: calculate_impact. It takes ONLY a service name string. "
        "Do NOT call any other tool. Do NOT pass extra parameters."
    ),
    agent=agents[1],
    expected_output="Prioritized recovery list with impact numbers per service"
)

task3 = Task(
    description=(
        "Execute the recovery plan for affected services.\n\n"
        "Complete these steps using ONLY your provided tools:\n"
        "Step 1: Call failover_service(service='Mobile Banking')\n"
        "Step 2: Call failover_service(service='Fraud Detection')\n"
        "Step 3: Call failover_service(service='Online Transfers')\n"
        "Step 4: Call log_lesson with a summary of the recovery actions taken.\n\n"
        "After all steps, write your Final Answer with the recovery results.\n"
        "IMPORTANT: You have ONLY 2 tools: failover_service and log_lesson. "
        "Do NOT call any other tool."
    ),
    agent=agents[2],
    expected_output="Recovery results for each service with timestamps"
)

task4 = Task(
    description=(
        "Send stakeholder notifications about the incident and recovery.\n\n"
        "Complete these steps using ONLY your provided tool:\n"
        "Step 1: Call send_notification(message='...', audience='customers')\n"
        "Step 2: Call send_notification(message='...', audience='executives')\n"
        "Step 3: Call send_notification(message='...', audience='regulators')\n\n"
        "After all 3 calls, write your Final Answer with all messages sent.\n"
        "IMPORTANT: You have ONLY 1 tool: send_notification. It takes message and audience. "
        "Do NOT call any other tool."
    ),
    agent=agents[3],
    expected_output="All notification messages sent with audiences listed",
    context=[task1, task2, task3]
)