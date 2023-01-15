FROM python:3.9 
# Or any preferred Python version.
ADD api.py .
RUN pip install requests boto3
CMD [“python”, “./api.py”] 
