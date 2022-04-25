# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the gRPC testing server."""
# I COPIED AND ADAPTED THE ORIGINAL FILE XDD

from concurrent import futures
import logging
import datetime
from dotenv import dotenv_values
from string import ascii_letters

import grpc
import testing_proto_file_pb2 as ReqResModule
import testing_proto_file_pb2_grpc as ClientServerModule

venv_dict = dict(dotenv_values(".env"))
ascii_dict = {key:value for value, key in enumerate(ascii_letters)}

# put here aux functions
print("iniciando servidor")

class TestingRpcFeaturesServicer(ClientServerModule.TestingRpcFeaturesServicer):
    """Provides methods that implement functionality of testing server."""

    # def __init__(self):
    #     self.db = route_guide_resources.read_route_guide_database()

    # rpc CurrentTime(TextMessage) returns (TimeStructure) {}
    # this function should return a single value
    def CurrentTime(self, request, context):    
        messageReceived = request.someMessage
        responseMessage = "IT WOOOORKS"

        print(f'The received message is {messageReceived} and the context is {context}')
        print(f'We are sending back this {responseMessage} \n')
        
        dateTimeObj = datetime.datetime.now()
        
        return ReqResModule.TimeStructure(
            hour = f'{dateTimeObj.hour} : {dateTimeObj.minute} : {dateTimeObj.second}',
            date = f'{dateTimeObj.day}/{dateTimeObj.month}/{dateTimeObj.year}',
            timeMessage = ReqResModule.TextMessage(someMessage=responseMessage)
        )


    # rpc GenRandomNumbersStream(NumberGenParams) returns (stream GeneratedNumber) {}
    # since we are sending a streaming of data back to the client, we have to use
    # the "yield" keyword
    def GenRandomNumbersStream(self, request, context):
        increment = request.increment
        acc = request.floorNumber + increment
        print(f'Valores recibidos: valor base => {acc}; incremento => {increment} \n')
        for i in range(10):
            yield ReqResModule.RealNumber(numberToUse=acc)
            acc+=increment


    # rpc SumOfStreamNumbers(stream RealNumber) returns (GeneratedNumber) {}
    # we will receive a stream of numbers and we have to perform the sum of them
    # to handle streamings we use "request_iterator"
    def SumOfStreamNumbers(self, request_iterator, context):
        acc = 0
        # since we are using gRPC, we no longer have to check types
        for reqElement in request_iterator:
            # we ALWAYS have to access the field property in order to use the value
            print(reqElement.numberToUse)
            acc += reqElement.numberToUse
        
        print(f"Valor de la suma de todos los números {acc}\n")
        return ReqResModule.RealNumber(numberToUse=acc)


    # rpc TransformWordsToNumbers(stream RealNumber) returns (stream TextMessage) {}
    def TransformWordsToNumbers(self, request_iterator, context):
        # reqElement is each letter received from client
        for reqElement in request_iterator:
            requestLetter = reqElement.someMessage 
            print(f'Letra recibida: {requestLetter}')
            yield ReqResModule.RealNumber(numberToUse=ascii_dict[requestLetter])


    # def RouteChat(self, request_iterator, context):
    #     # prev_notes = []
    #     # for new_note in request_iterator:
    #     #     for prev_note in prev_notes:
    #     #         if prev_note.location == new_note.location:
    #     #             yield prev_note
    #     #     prev_notes.append(new_note)
    #     pass

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    ClientServerModule.add_TestingRpcFeaturesServicer_to_server(
        TestingRpcFeaturesServicer(), server)
    server.add_insecure_port(f'[::]:{venv_dict["PORT"]}')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
