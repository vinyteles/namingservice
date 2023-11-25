from __future__ import print_function
import logging

import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc
import NameService_pb2
import NameService_pb2_grpc


import const

def run(server):
    print("server ip:" + str(server.address)+ ", server port: " + str(server.port))
    with grpc.insecure_channel(str(server.address)+':'+str(server.port)) as channel2:
        stub2 = EmployeeService_pb2_grpc.EmployeeServiceStub(channel2)
        print("passou do stub")
        print(str(stub2))
        # # Query an employee's data
        # response = stub.GetEmployeeDataFromID(EmployeeService_pb2.EmployeeID(id=101))
        # print ('Employee\'s data: ' + str(response))
        #
        # # Add a new employee
        # response = stub.CreateEmployee(EmployeeService_pb2.EmployeeData(id=301, name='Jose da Silva', title='Programmer'))
        # print ('Added new employee ' + response.status)
        #
        # # Change an employee's title
        # response = stub.UpdateEmployeeTitle(EmployeeService_pb2.EmployeeTitleUpdate(id=301, title='Senior Programmer'))
        # print ('Updated employee ' + response.status)
        #
        # # Delete an employee
        # response = stub.DeleteEmployee(EmployeeService_pb2.EmployeeID(id=201))
        # print ('Deleted employee ' + response.status)
        #
        # # List all employees
        # response = stub.ListAllEmployees(EmployeeService_pb2.EmptyMessage())
        # print ('All employees: ' + str(response))

        # List all titles
        response = stub2.ListAllTitles(EmployeeService_pb2.EmptyMessage())
        print('All Titles: \n' + str(response))

        # List all employees by title
        title_tmp = 'Technical Leader'
        response = stub2.ListAllEmployeesByTitle(EmployeeService_pb2.EmployeeTitle(title=title_tmp))
        print('All employee names by the title ' + title_tmp + ':\n' + str(response))

def find_server():
    server = None
    with grpc.insecure_channel(const.IP + ':' + const.PORT) as channel1:
        stub1 = NameService_pb2_grpc.NameServiceStub(channel1)

        server = stub1.LookupServer(NameService_pb2.ServerName(name="server1"))
    print(str(server))
    return server

if __name__ == '__main__':
    logging.basicConfig()
    server = find_server()
    run(server)