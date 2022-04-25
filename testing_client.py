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
"""The Python implementation of the gRPC testing client."""
# I COPIED AND ADAPTED THE ORIGINAL FILE XDD

from __future__ import print_function

import logging
from math import floor
import random
from dotenv import dotenv_values

import grpc
import testing_proto_file_pb2 as ReqResModule
import testing_proto_file_pb2_grpc as ClientServerModule

venv_dict = dict(dotenv_values(".env"))


def testing_Get_CurrentTime(stub):
    print("\n\n-------------- testing_Get_CurrentTime --------------\n\n")

    messageToSend = "this is a message from the stub/client. HELLO GUORLD"
    serverResponse = stub.CurrentTime(
        ReqResModule.TextMessage(
            someMessage = messageToSend
    ))
    print(f'The server response is \n{serverResponse}')


def testing_Get_RandomNumbersStream(stub):
    print("\n\n-------------- testing_Get_RandomNumbersStream --------------\n\n")

    randomNumberToSend = random.randint(100, 200)
    incrementValueToSend = random.randint(15, 60)

    print(f'Datos a enviar: floorNumber {randomNumberToSend}; increment {incrementValueToSend}')

    serverResponse_iterator = stub.GenRandomNumbersStream(
        ReqResModule.NumberGenParams(
            floorNumber = randomNumberToSend,
            increment = incrementValueToSend
        )
    )
    for i in serverResponse_iterator:
        print(i)



def generateStreamOfValues(arr, valueType=None):
    if (valueType == "str"):
        for strElement in arr:
            yield ReqResModule.TextMessage(someMessage = strElement)
    else: # numbers
        for intElement in arr:
            yield ReqResModule.RealNumber(numberToUse = intElement)

def testing_Get_SumOfStreamNumbers(stub):
    print("\n\n-------------- testing_Get_SumOfStreamNumbers --------------\n\n")
    
    valuesToSend = [random.randint(100, 200) for x in range(10)]
    print(f'Values to send: {",".join([str(x) for x in valuesToSend])}')

    numbers_iterator = generateStreamOfValues(valuesToSend)
    serverResponse = stub.SumOfStreamNumbers(numbers_iterator)
    print(f'Sum of all values: {serverResponse}')


def testing_TransformWordsToNumbers(stub):
    print("\n\n-------------- testing_TransformWordsToNumbers --------------\n\n")
    
    optionWords = ["Aluvion", "Completos", "Perritos", "Bitcoin"]
    randomChoise = random.randint(0,len(optionWords))
    print(f'Word to send: {optionWords[randomChoise]}')
    
    numbers_iterator = generateStreamOfValues([x for x in optionWords[randomChoise]], "str")
    serverResponse = stub.TransformWordsToNumbers(numbers_iterator)

    acc = ""
    for resElement in serverResponse:
        print(f'Number equivalent: {resElement.numberToUse}')
        acc += str(resElement.numberToUse)
    print(f'\nFinal code getted: {acc}\n')






def getKeyboardInput(requestOptions):
    print(f'Request options: {"  -  ".join(list(requestOptions.keys()))}')
    while True:
        keyboardInput = input("Select a request to be made: ")
        if (keyboardInput in requestOptions): return keyboardInput

def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    requestsOptions = {
            "CurrentTime": testing_Get_CurrentTime,
            "GenRandomNumbersStream": testing_Get_RandomNumbersStream,
            "SumOfStreamNumbers": testing_Get_SumOfStreamNumbers,
            "TransformWordsToNumbers": testing_TransformWordsToNumbers
    }

    with grpc.insecure_channel(f'localhost:{venv_dict["PORT"]}') as channel:
        stub = ClientServerModule.TestingRpcFeaturesStub(channel)
        userChoise = getKeyboardInput(requestsOptions)
        selectedRequest = requestsOptions[userChoise]

        selectedRequest(stub)

        # print("\n\n-------------- testing_Get_CurrentTime --------------\n\n")
        # testing_Get_CurrentTime(stub)

        # print("-------------- testing_Get_RandomNumbersStream --------------")
        # testing_Get_RandomNumbersStream(stub)

        # print("-------------- testing_Get_SumOfStreamNumbers --------------")
        # testing_Get_SumOfStreamNumbers(stub)

        # print("-------------- testing_TransformWordsToNumbers --------------")
        # testing_TransformWordsToNumbers(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
