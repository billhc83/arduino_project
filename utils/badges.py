# badges.py

badges = {
    "automatic_night_light": {
        "title": "Automatic Night Light",
        "tier": "orange",
        "subtitle": "Engineering Achievement Badge",
        "icon": "🌙💡",
        "points": [
            "📟 Used a sensor",
            "🧠 Solved a real problem"
        ],
        "trigger": lambda unlocked: any("project_eight"in p.lower() for p in unlocked)
    },
    "first_project": {
        "title": "First Project Complete",
        "tier": "green",
        "subtitle": "Getting Started Badge",
        "icon": "🎉",
        "points": ["🚀 Started your first project", "🎯 Completed it successfully"],
        "trigger": lambda unlocked: any("project_one" in p.lower() for p in unlocked)
    },
    "first_challenge":{
        "title": "First Challenge Complete",
        "tier": "blue",
        "subtitle": "Challenge cooker",
        "icon": "📚💻✍🏼📓",
        "points": ["🚀 Completed first challenge", "🎯 code writer!!!"],
        "trigger": lambda unlocked: any("challenge_two" in p.lower() for p in unlocked)
    }
}
