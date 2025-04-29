resource "aws_s3_bucket" "simple_bucket" {
  bucket = "simple-test-bucket"

  tags = {
    Name        = "simple bucket"
    Environment = "Dev"
  }
}

# KMS for bucket
resource "aws_kms_key" "simple_key" {
  description             = "This key is used to encrypt bucket objects"
  deletion_window_in_days = 10

}


resource "aws_s3_bucket_server_side_encryption_configuration" "simp[le_sse_config" {
  bucket = aws_s3_bucket.simple_bucket.id

  rule {
    apply_server_side_encryption_by_default {
      kms_master_key_id = aws_kms_key.simple_bucket.arn
      sse_algorithm     = "aws:kms"
    }
  }
}