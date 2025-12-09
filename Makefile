# Variables
DOCKER_USERNAME ?= your-dockerhub-username
IMAGE_NAME ?= fastapi-todo
TAG ?= latest
DOCKERFILE_PATH = docker/Dockerfile
CONTEXT_PATH = .

# Full image name
FULL_IMAGE_NAME = $(DOCKER_USERNAME)/$(IMAGE_NAME):$(TAG)

.PHONY: login
login:
	@echo "Logging in to DockerHub..."
	@docker login

.PHONY: build
build:
	@echo "Building Docker image: $(FULL_IMAGE_NAME)"
	@docker build -t $(FULL_IMAGE_NAME) -f $(DOCKERFILE_PATH) $(CONTEXT_PATH)
	@echo "Successfully built: $(FULL_IMAGE_NAME)"

.PHONY: push
push:
	@echo "Pushing Docker image: $(FULL_IMAGE_NAME)"
	@docker push $(FULL_IMAGE_NAME)
	@echo "Successfully pushed: $(FULL_IMAGE_NAME)"

.PHONY: build-push
build-push: build push
	@echo "Build and push completed for: $(FULL_IMAGE_NAME)"

.PHONY: tag
tag:
	@echo "Tagging image $(DOCKER_USERNAME)/$(IMAGE_NAME):latest as $(FULL_IMAGE_NAME)"
	@docker tag $(DOCKER_USERNAME)/$(IMAGE_NAME):latest $(FULL_IMAGE_NAME)
	@echo "Successfully tagged: $(FULL_IMAGE_NAME)"

.PHONY: clean
clean:
	@echo "Removing local image: $(FULL_IMAGE_NAME)"
	@docker rmi $(FULL_IMAGE_NAME) || true
	@echo "Cleanup completed"
