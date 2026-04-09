from crewai.tools import BaseTool
from pydantic import BaseModel

class AnalyzeSecurityEventTool(BaseTool):
    name: str = "analyze_security_event"
    description: str = "Analyzes and classifies a security or infrastructure event. Pass in the event description to get severity classification and affected services."
    def _run(self, event_description: str):
        event_lower = event_description.lower()
        if "ransomware" in event_lower or "encrypted" in event_lower:
            return (
                "Classification: CATASTROPHIC | Type: Ransomware/Encryption Attack | "
                "Affected: Primary Data Center | Services Down: Mobile Banking, Online Transfers | "
                "Data Exfiltration: None confirmed | "
                "Recommended: Immediate BCM invocation, isolate affected systems, activate DR site"
            )
        elif "ddos" in event_lower or "outage" in event_lower:
            return (
                "Classification: MAJOR | Type: Infrastructure Outage + DDoS | "
                "Affected: Cloud Provider Region | Services Degraded: All | "
                "Recommended: Activate failover, engage provider support, BCM invocation"
            )
        else:
            return (
                "Classification: MINOR | Type: Unclassified disruption | "
                "Recommended: Monitor and escalate if impact grows"
            )

class ServiceCatalogTool(BaseTool):
    name: str = "get_service_catalog"
    description: str = "Returns critical services with RTO/RPO"
    def _run(self):
        return "Mobile Banking (RTO:4h, RPO:15m), Fraud Detection (RTO:2h), Online Transfers (RTO:4h)"

class ImpactTool(BaseTool):
    name: str = "calculate_impact"
    description: str = "Calculates customer & financial impact"
    def _run(self, service: str):
        return f"{service} impacts 1.2M customers and $2.4M/hour revenue loss"

class FailoverTool(BaseTool):
    name: str = "failover_service"
    description: str = "Triggers automated failover to secondary cloud"
    def _run(self, service: str):
        return f"✅ {service} successfully failed over to DR site in 87 seconds"

class NotificationTool(BaseTool):
    name: str = "send_notification"
    description: str = "Sends stakeholder updates"
    def _run(self, message: str, audience: str):
        return f"📨 Message sent to {audience}: {message[:80]}..."

class LogLessonTool(BaseTool):
    name: str = "log_lesson"
    description: str = "Logs a lesson learned for continual improvement"
    def _run(self, lesson: str):
        return f"📝 Lesson logged for post-incident review: {lesson}"


analyze_security_event = AnalyzeSecurityEventTool()
get_service_catalog = ServiceCatalogTool()
calculate_impact = ImpactTool()
failover_service = FailoverTool()
send_notification = NotificationTool()
log_lesson = LogLessonTool()
