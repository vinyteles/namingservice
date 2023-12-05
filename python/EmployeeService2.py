from concurrent import futures
import logging
import socket
import grpc
import EmployeeService_pb2
import EmployeeService_pb2_grpc
import NameService_pb2
import NameService_pb2_grpc

import const

empDB=[
 {
 'id':101,
 'name':'Saravanan S',
 'title':'Technical Leader'
 },
 {
 'id':201,
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }
 ]

class EmployeeServer(EmployeeService_pb2_grpc.EmployeeServiceServicer):
  def ListAllEmployeesByTitle(self, request, context):
    title = request.title
    list = EmployeeService_pb2.EmployeeNameList()

    for emp in empDB:
      if emp['title'] == title:
        list.employee_name.append(emp['name'])

    return list
  def ListAllTitles(self, request, context):

    list = EmployeeService_pb2.EmployeeTitleList()

    for emp in empDB:
      if emp['title'] not in empDB:
        list.title.append(emp['title'])

    return list


  def CreateEmployee(self, request, context):
    dat = {
    'id':request.id,
    'name':request.name,
    'title':request.title
    }
    empDB.append(dat)
    return EmployeeService_pb2.StatusReply(status='OK')

  def GetEmployeeDataFromID(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    return EmployeeService_pb2.EmployeeData(id=usr[0]['id'], name=usr[0]['name'], title=usr[0]['title'])

  def UpdateEmployeeTitle(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    usr[0]['title'] = request.title
    return EmployeeService_pb2.StatusReply(status='OK')

  def DeleteEmployee(self, request, context):
    usr = [ emp for emp in empDB if (emp['id'] == request.id) ]
    if len(usr) == 0:
      return EmployeeService_pb2.StatusReply(status='NOK')

    empDB.remove(usr[0])
    return EmployeeService_pb2.StatusReply(status='OK')

  def ListAllEmployees(self, request, context):
    list = EmployeeService_pb2.EmployeeDataList()
    for item in empDB:
      emp_data = EmployeeService_pb2.EmployeeData(id=item['id'], name=item['name'], title=item['title'])
      list.employee_data.append(emp_data)
    return list


def register_in_name_service():
    ip_address = str(socket.gethostbyname(socket.gethostname()))
    with grpc.insecure_channel(const.IP + ':' + const.PORT) as channel2:
        stub2 = NameService_pb2_grpc.NameServiceStub(channel2)

        response = stub2.RegisterServer(NameService_pb2.ServerData(name='Xyz', address=ip_address, port='50051'))
        print(str(response))

    return None

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    EmployeeService_pb2_grpc.add_EmployeeServiceServicer_to_server(EmployeeServer(), server)
    tmp_port = server.add_insecure_port('[::]:' + '50051')
    print(tmp_port)
    register_in_name_service()
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
