variable "Registry" {
    default = "ghcr.io/erf04"
}

variable "IMAGE_TAG" {
    default = "latest"
}


target "backend" {
    context = "./backend"
    dockerfile = "Dockerfile"
    tags = [ "${ Registry }/backend:${IMAGE_TAG}" ]
    cache-from = ["type=registry,ref=${Registry}/backend:cache"]
    cache-to   = ["type=registry,ref=${Registry}/backend:cache,mode=max"]
}

target "frontend" {
    context = "./frontend"
    dockerfile = "Dockerfile"
    tags = [ "${ Registry }/frontend:${IMAGE_TAG}" ]
    cache-from = ["type=registry,ref=${Registry}/frontend:cache"]
    cache-to   = ["type=registry,ref=${Registry}/frontend:cache,mode=max"]
}

group "default" {
  targets = ["backend", "frontend"]
}
