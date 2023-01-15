FROM python:3.12.0a4-alpine3.17
# Or any preferred Python version.
ADD api.py .
RUN pip install requests boto3
CMD [“python”, “./api.py”]
