# RabbitMQ task

run with

docker run -it --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management

docker exec -it rabbitmq bash

Run following to add a new user with admin privileges.

rabbitmqctl add_user <username> <password>
rabbitmqctl set_user_tags <username> administrator
