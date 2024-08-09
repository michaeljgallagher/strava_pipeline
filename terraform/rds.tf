resource "aws_db_instance" "rds_instance" {
  engine                 = "postgres"
  identifier             = "rds-terraform"
  allocated_storage      = 20
  engine_version         = "14.12"
  instance_class         = "db.t3.micro"
  username               = "awsadmin"
  password               = var.rds_password
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.rds_security_group.id]

}


resource "aws_security_group" "rds_security_group" {
  name = "rds_security_group"
  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
