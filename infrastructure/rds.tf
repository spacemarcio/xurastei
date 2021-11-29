resource "aws_db_instance" "rds" {
  identifier                = "xox-db"
  name                      = "xox"
  allocated_storage         = 20
  engine                    = "postgres"
  engine_version            = "11.1"
  instance_class            = "db.t3.micro"
  username                  = var.username
  password                  = var.password
  port                      = var.port
  skip_final_snapshot       = true
  publicly_accessible       = true
}