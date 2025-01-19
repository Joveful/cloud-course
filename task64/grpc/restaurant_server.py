from concurrent import futures
import grpc
import grpc.experimental
import sys
from proto import restaurant_pb2
from proto import restaurant_pb2_grpc

RESTAURANT_ITEMS_FOOD = ["chips", "fish", "burger", "pizza", "pasta", "salad"]
RESTAURANT_ITEMS_DRINK = ["water", "fizzy drink", "juice", "smoothie", "coffee", "beer"]
RESTAURANT_ITEMS_DESSERT = [
    "ice cream",
    "chocolate cake",
    "cheese cake",
    "brownie",
    "pancakes",
    "waffles",
]


class Restaurant(restaurant_pb2_grpc.RestaurantServicer):
    # Check that items are in the menus
    def CheckItems(self, request_items, restaurant_items):
        for i in request_items:
            if i not in restaurant_items:
                return False
        return True

    def FoodOrder(self, request, context):
        response = restaurant_pb2.RestaurantResponse(
            orderID=request.orderID,
            status=(0 if self.CheckItems(request.items, RESTAURANT_ITEMS_FOOD) else 1),
        )
        for item in request.items:
            it = restaurant_pb2.items(itemName=item)
            response.itemMessage.append(it)
        return response

    def DrinkOrder(self, request, context):
        response = restaurant_pb2.RestaurantResponse(
            orderID=request.orderID,
            status=(0 if self.CheckItems(request.items, RESTAURANT_ITEMS_DRINK) else 1),
        )
        for item in request.items:
            it = restaurant_pb2.items(itemName=item)
            response.itemMessage.append(it)
        return response

    def DessertOrder(self, request, context):
        response = restaurant_pb2.RestaurantResponse(
            orderID=request.orderID,
            status=(
                0 if self.CheckItems(request.items, RESTAURANT_ITEMS_DESSERT) else 1
            ),
        )
        for item in request.items:
            it = restaurant_pb2.items(itemName=item)
            response.itemMessage.append(it)
        return response

    def MealOrder(self, request, context):
        response = restaurant_pb2.RestaurantResponse(
            orderID=request.orderID,
            status=(
                0
                if request.items[0] in RESTAURANT_ITEMS_FOOD
                and request.items[1] in RESTAURANT_ITEMS_DRINK
                and request.items[2] in RESTAURANT_ITEMS_DESSERT
                else 1
            ),
        )
        for item in request.items:
            it = restaurant_pb2.items(itemName=item)
            response.itemMessage.append(it)
        return response


def serve():
    # Logic goes here
    # Remember to start the server on localhost and a port defined by the first command line argument
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    restaurant_pb2_grpc.add_RestaurantServicer_to_server(Restaurant(), server)
    server.add_insecure_port("localhost:{}".format(sys.argv[1]))
    print("localhost:{}".format(sys.argv[1]))
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
