import json
import boto3
import zipfile
import io
import os

code_pipeline = boto3.client('codepipeline')
s3 = boto3.client('s3')
lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    try:
        print(f"event: {event}")
        job_id = event['CodePipeline.job']['id']
        job_data = event['CodePipeline.job']['data']
        
        # 입력 아티팩트 처리
        input_artifact = job_data['inputArtifacts'][0]
        bucket = input_artifact['location']['s3Location']['bucketName']
        key = input_artifact['location']['s3Location']['objectKey']
        
        # S3에서 아티팩트 다운로드
        response = s3.get_object(Bucket=bucket, Key=key)
        zip_bytes = response['Body'].read()
        
        # Lambda 함수 업데이트
        lambda_client.update_function_code(
            FunctionName=context.function_name,
            ZipFile=zip_bytes
        )
        
        # CodePipeline에 성공 결과 전송
        code_pipeline.put_job_success_result(jobId=job_id)
        
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Lambda function updated successfully"
            })
        }
        
    except Exception as e:
        print(f"Error: {str(e)}")
        if 'job_id' in locals():
            code_pipeline.put_job_failure_result(
                jobId=job_id,
                failureDetails={
                    'type': 'JobFailed',
                    'message': str(e)
                }
            )
        raise e