import grpc
from proto import restaurant_pb2_grpc
from proto import restaurant_pb2


def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = restaurant_pb2_grpc.RestaurantStub(channel)
        response = stub.FoodOrder(
            restaurant_pb2.RestaurantRequest(orderID="69", items=["cock", "dick"])
        )
        print("Restaurnat client received: " + str(response.status))


if __name__ == "__main__":
    run()
