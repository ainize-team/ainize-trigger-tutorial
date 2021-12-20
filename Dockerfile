FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-devel

WORKDIR /workspace

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python3", "test.py"]