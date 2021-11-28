# Imagem Ubuntu
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

resource "aws_instance" "airflow" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t3.large"
  key_name                    = "xurastei"
  associate_public_ip_address = true
  security_groups             = [aws_security_group.airflow_sg.id]
  subnet_id                   = "subnet-64bcc128"
  
  root_block_device {
    volume_size = 64
  }
}