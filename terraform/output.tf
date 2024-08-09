# Output Region set for AWS
output "aws_region" {
  description = "Region set for AWS"
  value       = var.aws_region
}

output "bucket_name" {
  description = "S3 bucket name."
  value       = aws_s3_bucket.test-s3-bucket.id
}

output "rds_database_name" {
  description = "Database name in the RDS cluster"
  value       = aws_db_instance.rds_instance.db_name
}

output "rds_instance_endpoint" {
  description = "Endpoint of the RDS cluster"
  value       = aws_db_instance.rds_instance.endpoint
}

output "rds_username" {
  description = "Username of the RDS cluster"
  value       = aws_db_instance.rds_instance.username
}

output "rds_password" {
  description = "Password for the RDS cluster"
  value       = var.rds_password
  sensitive   = true
}

output "rds_port" {
  description = "Port for the RDS cluster"
  value       = aws_db_instance.rds_instance.port
}
