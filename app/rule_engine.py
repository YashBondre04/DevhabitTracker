def calculate_metrics(activities):
    total_active_minutes = 0
    app_durations = {}
    work_apps = {"VS Code", "GitHub", "Terminal", "Slack", "Jira", "Postman", "StackOverflow", "Chrome StackOverflow"}
    non_work_time = 0

    context_switches = 0
    current_focus_session = 0
    longest_focus_session = 0
    focus_sessions = 0
    
    previous_app = None

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
            current_focus_session = 0
        else:
            if previous_app not in work_apps or previous_app is None:
                focus_sessions += 1
                current_focus_session = duration
            else:
                current_focus_session += duration
                
            if current_focus_session > longest_focus_session:
                longest_focus_session = current_focus_session

        if previous_app and previous_app != app:
            context_switches += 1
            
        previous_app = app

    most_used_app = max(app_durations, key=app_durations.get) if app_durations else None
    
    distraction_percentage = 0.0
    if total_active_minutes > 0:
        distraction_percentage = (non_work_time / total_active_minutes) * 100
        
    average_focus_duration = 0
    if focus_sessions > 0:
        average_focus_duration = (total_active_minutes - non_work_time) / focus_sessions

    return {
        "total_active_minutes": total_active_minutes,
        "most_used_app": most_used_app,
        "distraction_percentage": round(distraction_percentage, 2),
        "context_switches": context_switches,
        "focus_sessions": focus_sessions,
        "average_focus_duration": round(average_focus_duration, 2),
        "longest_focus_session": longest_focus_session
    }


def detect_patterns(metrics):
    evidence = []
    total = metrics["total_active_minutes"]
    switches = metrics["context_switches"]
    avg_focus = metrics["average_focus_duration"]
    distraction_pct = metrics["distraction_percentage"]
    longest = metrics["longest_focus_session"]
    hours = round(total / 60, 1)

    # Classify user behavior into one of 5 distinct productivity patterns
    # based on heuristic thresholds to prevent LLM hallucination
    if switches >= 5 and avg_focus < 40:
        pattern_type = "fragmented_workflow"
        evidence.append(f"{switches} context switches in {hours} hours")
        evidence.append(f"Average focus session is only {avg_focus} minutes")
    elif distraction_pct >= 30:
        pattern_type = "high_distraction"
        evidence.append(f"{distraction_pct}% of active time spent on non-work apps")
        evidence.append(f"Only {round(100 - distraction_pct, 1)}% of session was productive")
    elif longest >= 90 and distraction_pct > 15:
        pattern_type = "burnout_cycle"
        evidence.append(f"Longest focus block was {longest} minutes without a break")
        evidence.append(f"Distraction spike of {distraction_pct}% suggests post-focus fatigue")
    elif avg_focus >= 60 and distraction_pct < 15:
        pattern_type = "deep_focus"
        evidence.append(f"Average focus session of {avg_focus} minutes indicates strong concentration")
        evidence.append(f"Distraction rate of only {distraction_pct}%")
    else:
        pattern_type = "moderate_productivity"
        evidence.append(f"{switches} context switches across {hours} hours")
        evidence.append(f"Average focus duration of {avg_focus} minutes")

    return {
        "type": pattern_type,
        "evidence": evidence
    }
