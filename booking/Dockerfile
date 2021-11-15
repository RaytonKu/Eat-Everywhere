FROM python:3

RUN pip install grpcio
RUN pip install grpcio-tools

RUN mkdir -p /app

COPY booking_service.py /app/

ENV PYTHONPATH /app:/app/event_store:/app/message_queue

RUN git clone ... /app/event_store
RUN git clone ... /app/message_queue

CMD [ "python", "app/booking_service.py" ]
