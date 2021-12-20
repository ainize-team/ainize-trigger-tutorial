FROM yeop2/gpt2-prideandprejudice

WORKDIR /workspace

COPY . .

RUN pip install -r requirements.txt

EXPOSE 3000

CMD ["python3", "test.py"]
