resource "aws_instance" "backend" {
  ami           = "ami-0dad359ff462124ca"  # Ubuntu 22.04 in eu-west-1
  instance_type = "t3.micro"
  
  security_groups = [aws_security_group.backend_sg.name]
  
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update
              sudo apt install -y docker.io awscli
              sudo systemctl start docker
              
              # Pull and run container
              aws ecr get-login-password --region eu-west-1 | sudo docker login --username AWS --password-stdin 353925322836.dkr.ecr.eu-west-1.amazonaws.com
              
              sudo docker run -d \
                -p 80:8000 \
                -e DATABASE_URL="postgresql://devuser:${var.db_password}@${aws_db_instance.postgres.address}:5432/saas_db" \
                353925322836.dkr.ecr.eu-west-1.amazonaws.com/project-3-saas-backend:latest
              EOF

  tags = {
    Name = "project-3-saas-backend"
  }
}

resource "aws_security_group" "backend_sg" {
  name = "project-3-saas-backend-sg"

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

output "backend_url" {
  value = "http://${aws_instance.backend.public_ip}"
}
