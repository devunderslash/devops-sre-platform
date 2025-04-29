terraform {  
  backend "s3" {  
    bucket       = "simple-terraform-state-bucket"  
    key          = "simple_state/statefile.tfstate"  
    region       = "us-east-1"  
    encrypt      = true  
    use_lockfile = true  #S3 native locking
  }  
}
