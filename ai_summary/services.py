def get_user_summary(user):

    return {
        "missions_active": 0,
        "unread_messages": 0,
        "security_alerts": 0
    }


def build_ai_message(user, summary):

    name = user.first_name or user.username

    missions_active = summary.get("missions_active", 0)
    unread_messages = summary.get("unread_messages", 0)
    security_alerts = summary.get("security_alerts", 0)

    text = f"Hi {name}, AI Assistant reporting. "

    if missions_active == 0:
        text += "No active missions at the moment. System is stable. "
    else:
        text += "Operations are ongoing. Monitor mission progress closely. "

    if unread_messages > 0:
        text += f"You have {unread_messages} unread messages awaiting attention. "
    else:
        text += "No pending messages. Communication channels are clear. "

    if security_alerts > 0:
        text += "Security alerts detected. Review required immediately. "
    else:
        text += "No security threats detected. All systems secure. "

    return text