#!/usr/bin/env bash
# Guide Step 13: prepare a free-tier EC2 (Amazon Linux 2023 / Ubuntu) for ClaimSense AI.
# Run ONCE on the fresh instance, then: git clone <your-repo> && docker compose up --build
set -euo pipefail

sudo yum update -y 2>/dev/null || sudo apt-get update -y
# Docker
if command -v yum >/dev/null; then
  sudo yum install -y docker
  sudo systemctl enable --now docker
else
  sudo apt-get install -y docker.io docker-compose-plugin
  sudo systemctl enable --now docker
fi
sudo usermod -aG docker "$USER"

# Open ports: 22 (ssh), 5173 (frontend), 8000 (api) in the EC2 security group via console.
echo "Docker ready. Log out/in, then: git clone <repo> && cd claimsense-ai && docker compose up --build -d"
echo "Remember: STOP the instance when not demoing to stay inside free tier."
