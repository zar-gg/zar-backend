setup:
	chmod +x setup.sh
	bash setup.sh

up:
	docker-compose up -d --build

down:
	docker-compose down --remove-orphans

key:
	@echo "Enter new API Key: "; \
	read KEY; \
	echo "API_KEY=$$KEY" > .env;	
	docker-compose down --remove-orphans
	docker-compose up -d --build
