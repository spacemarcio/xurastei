## Step-by-step to setup infrastructure

1. Just execute the command `terraform apply`
2. The terraform state file is stored at S3. To make things work, you have to:
* 2.1 Edit provier.tf file
* 2.2 Comment the lines 5 to 11
* 2.3 Execute the command `terraform apply`
* 2.3 Create a bucket and put the `terraform.state` in there
* 2.4 Uncomment the lines 5 to 11