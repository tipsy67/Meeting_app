Application for friendly meetings

Commands for run taskiq: 
taskiq worker api_app.core.taskiq_broker:broker --fs-discover --tasks-pattern "**/tasks" --workers 1
taskiq scheduler api_app.core.taskiq_broker:scheduler --skip-first-run


