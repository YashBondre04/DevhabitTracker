def calculate_metrics(activities):
    total_active_minutes = 0
    app_durations = {}
    work_apps = {"VS Code", "GitHub", "Terminal", "Slack", "Jira", "Postman", "StackOverflow"}
    non_work_time = 0

    for act in activities:
        duration = act.get("duration_minutes", 0)
        app = act.get("app", "Unknown")
        
        total_active_minutes += duration
        
        if app in app_durations:
            app_durations[app] += duration
        else:
            app_durations[app] = duration
            
        if app not in work_apps:
            non_work_time += duration

    most_used_app = max(app_durations, key=app_durations.get) if app_durations else None
    
    distraction_percentage = 0.0
    if total_active_minutes > 0:
        distraction_percentage = (non_work_time / total_active_minutes) * 100

    return {
        "total_active_minutes": total_active_minutes,
        "most_used_app": most_used_app,
        "distraction_percentage": round(distraction_percentage, 2)
    }
