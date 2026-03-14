.PHONY: up down build restart logs logs-a logs-b test clean

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose up --build -d

restart:
	docker compose down && docker compose up --build -d

logs:
	docker compose logs -f

logs-a:
	docker compose logs -f service_a

logs-b:
	docker compose logs -f service_b

test:
	cd service_a && pytest tests/ -v

clean:
	docker compose down -v
