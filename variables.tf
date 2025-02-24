variable "hetzner_cloud_api_token" {
  sensitive   = true
    type        = string
    description = "Hetzner Cloud API Token"
}

variable "hetzner_ssh_key_fingerprint" {
    sensitive   = true
    type        = string
    description = "Hetzner SSH Key Fingerprint"
}
