mkdir -p src/logs
touch src/logs/celery_beat.log
touch src/logs/celery_worker.log
touch .env
echo "Enter API Key: "; \
read KEY; \
echo "API_KEY=$KEY" > .env;