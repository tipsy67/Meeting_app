Application for friendly meetings

Commands for run taskiq: 
taskiq worker api_app.core.taskiq_broker:broker --fs-discover --tasks-pattern "**/tasks" --workers 1
taskiq scheduler api_app.core.taskiq_broker:scheduler --skip-first-run

Commands for generate keys:
openssl genrsa -out jwt-private.pem 2048
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem


