states = [
    "initiated",
    "pending review",
    "under review",
    "accepted",
    "rejected",
]

transitions = [
    {"trigger": "submit", "source": "initiated", "dest": "pending review"},
    {"trigger": "start_review", "source": "pending review", "dest": "under review"},
    {"trigger": "approve", "source": ["pending review", "under review"], "dest": "accepted"},
    {"trigger": "reject", "source": ["pending review", "under review"], "dest": "rejected"},
]