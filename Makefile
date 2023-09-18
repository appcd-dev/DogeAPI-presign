help:
	@echo "Targets:"
	@echo "    make pull"
	@echo "    make build"

pull:
	docker-compose pull

build:
	docker-compose build
