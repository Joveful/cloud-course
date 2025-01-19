terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  project = "css-jorivehkakoski-2024"
  region  = "europe-central2"
  zone    = "europe-central2-a"
}


variable "vm_name_input" {
  type        = string
  description = "VM instance name"
}

resource "google_compute_network" "vpc_network" {
  name = "terraform-network2"
}

resource "google_compute_firewall" "vpc_firewall" {
  name    = "my-firewall"
  network = google_compute_network.vpc_network.name

  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  allow {
    protocol = "tcp"
    ports    = ["22"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http", "ssh"]
}

resource "google_compute_instance" "vm_instance" {
  name         = var.vm_name_input
  machine_type = "f1-micro"

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  tags = ["http", "ssh"]

  network_interface {
    network = google_compute_network.vpc_network.name
    access_config {
    }
  }

  labels = {
    course = "css-gcp"
  }

  metadata_startup_script = <<-EOF
  #!/bin/bash
  sudo apt update -y
  sudo apt install apache2 -y
  sudo systemctl start apache2.service
  EOF
}

output "vm_name" {
  value       = google_compute_instance.vm_instance.name
  description = "VM instace name"
}

output "public_ip" {
  value = google_compute_instance.vm_instance.network_interface[0].access_config[0].nat_ip
}

