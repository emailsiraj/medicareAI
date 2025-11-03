"""
Apply CORS configuration to S3 bucket to allow PDF access from frontend.
"""

import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION', 'us-east-1')
)

bucket = 'plansmedicare1'

cors_configuration = {
    'CORSRules': [
        {
            'AllowedOrigins': ['*'],  # Allow all origins (you can restrict to your domain)
            'AllowedMethods': ['GET', 'HEAD'],
            'AllowedHeaders': ['*'],
            'MaxAgeSeconds': 3000
        }
    ]
}

print("="*80)
print(f"APPLYING CORS CONFIGURATION TO: {bucket}")
print("="*80)
print("\nCORS Rules:")
print(json.dumps(cors_configuration, indent=2))
print("\n" + "="*80)

try:
    response = s3_client.put_bucket_cors(
        Bucket=bucket,
        CORSConfiguration=cors_configuration
    )

    print("✅ CORS configuration applied successfully!")
    print("\nVerifying configuration...")

    # Verify
    cors = s3_client.get_bucket_cors(Bucket=bucket)
    print("✅ Verified - CORS is now configured:")
    for i, rule in enumerate(cors['CORSRules'], 1):
        print(f"\n   Rule {i}:")
        print(f"      Allowed Origins: {rule.get('AllowedOrigins')}")
        print(f"      Allowed Methods: {rule.get('AllowedMethods')}")
        print(f"      Allowed Headers: {rule.get('AllowedHeaders')}")
        print(f"      Max Age: {rule.get('MaxAgeSeconds')} seconds")

    print("\n" + "="*80)
    print("🎉 PDFs should now open in production!")
    print("="*80)

except Exception as e:
    print(f"❌ Error applying CORS: {e}")
    print("\nYou may need to:")
    print("1. Check IAM permissions (s3:PutBucketCORS)")
    print("2. Apply CORS manually via AWS Console")
