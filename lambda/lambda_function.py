import boto3
from io import BytesIO
from PIL import Image

s3 = boto3.client('s3')


def lambda_handler(event, context):
    source_bucket = event.get('sourceBucket')
    target_bucket = event.get('targetBucket')
    object_key = event.get('objectKey')

    response = s3.get_object(Bucket=source_bucket, Key=object_key)
    image_content = response['Body'].read()

    image = Image.open(BytesIO(image_content))
    image.thumbnail((128, 128))
    buffer = BytesIO()
    img_format = image.format if image.format else 'JPEG'
    image.save(buffer, format=img_format)
    buffer.seek(0)

    target_key = f"thumbnail-{object_key}"
    s3.put_object(
        Bucket=target_bucket,
        Key=target_key,
        Body=buffer,
        ContentType=response['ContentType']
    )

    return {
        'statusCode': 200,
        'body': f'Successfully resized {object_key} and saved to {target_bucket}'
    }
