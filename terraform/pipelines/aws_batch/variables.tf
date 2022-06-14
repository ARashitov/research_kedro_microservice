variable max_vcpus {
  type        = number
  default     = 10
  description = "Maximum VCPus to utilize"
}

variable min_vcpus {
  type        = number
  default     = 0
  description = "Minimum VCPus to utilize"
}

variable instance_type {
  type        = list(string)
  default     = [
    "c5a.large",
  ]
  description = "Instance types to use during processing"
}

variable docker_image_id {
  type        = string
  default     = "946627858531.dkr.ecr.us-east-1.amazonaws.com/dev_gps_clustering_pipelines:0.1.1"
  description = "Job baseline docker image"
}

variable docker_memory {
  type        = number
  default     = 3500
  description = "Amount of ram used by single docker container"
}

variable docker_vcpus {
  type        = number
  default     = 2
  description = "Amount of virtual CPU-s to use by a single docker container"
}

variable aws_access_key_id {
  type        = string
  description = "aws access key id used for export as env variable to batch job definition"
}

variable aws_secret_access_key {
  type        = string
  description = "aws secret access key used for export as env variable to batch job definition"
}
