variable "REGISTRY" {
    default = "ghcr.io/erf04"
}

variable "IMAGE_TAG" {
}


target "backend" {
    context = "./backend"
    dockerfile = "Dockerfile"

    tags = [ "${ REGISTRY }/backend:${IMAGE_TAG}" ]
    cache-from = ["type=registry,ref=${REGISTRY}/backend:cache"]
    cache-to   = ["type=registry,ref=${REGISTRY}/backend:cache,mode=max"]
}

target "frontend" {
    context = "./frontend"
    dockerfile = "Dockerfile"
    tags = [ "${ REGISTRY }/frontend:${IMAGE_TAG}" ]
    cache-from = ["type=registry,ref=${REGISTRY}/frontend:cache"]
    cache-to   = ["type=registry,ref=${REGISTRY}/frontend:cache,mode=max"]
}

group "default" {
  targets = ["backend", "frontend"]
}
