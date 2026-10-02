resource "aws_security_group" "rds" {
  name = "project-3-saas-rds-sg"

  ingress {
    from_port   = 5432
    to_port     = 5432
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

resource "aws_db_instance" "postgres" {
  identifier     = "project-3-saas-db"
  engine         = "postgres"
  engine_version = "15"
  instance_class = "db.t3.micro"
  
  allocated_storage = 20
  
  db_name  = "saas_db"
  username = "devuser"
  password = var.db_password
  
  publicly_accessible = true
  skip_final_snapshot = true
  vpc_security_group_ids = [aws_security_group.rds.id]
  
  tags = {
    Name = "project-3-saas-db"
  }
}

variable "db_password" {
  type      = string
  sensitive = true
}

output "rds_endpoint" {
  value = aws_db_instance.postgres.endpoint
}