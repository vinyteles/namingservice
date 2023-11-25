from concurrent import futures
import logging

import grpc
import NameService_pb2
import NameService_pb2_grpc

import const

name_service_table = {}

class NameServer(NameService_pb2_grpc.NameServiceServicer):
    def RegisterServer(self, request, context):
        tmp_server = {"address": request.address, "port": request.port}
        name_service_table[request.name] = tmp_server
        print("adding new Server")
        print(str(name_service_table))

        return NameService_pb2.StatusReply(status='OK')

    def UnregisterServer(self, request, context):
        name_service_table.pop(request.name)

    def LookupServer(self, request, context):
        tmp_server = {"name": "", "address": "", "port": ""}
        print("finding server with name: " + request.name)

        if request.name in name_service_table:
            tmp_server = name_service_table[request.name]
            print("server found!")
            print(str(tmp_server))
        else:
            print("server not found")

        return NameService_pb2.ServerData(name=request.name, address=tmp_server["address"], port=tmp_server["port"])


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    NameService_pb2_grpc.add_NameServiceServicer_to_server(NameServer(), server)
    tmp_port = server.add_insecure_port('[::]:'+'5000')
    print(tmp_port)
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
