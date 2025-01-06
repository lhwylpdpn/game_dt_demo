from twisted.internet import protocol, reactor
import card_game_pb2


class CardGameProtocol(protocol.Protocol):
    def dataReceived(self, data):
        try:
            if len(data) < 4:
                print("Incomplete data: waiting for length prefix")
                return

            length_prefix = int.from_bytes(data[:4], byteorder="big")
            payload = data[4:4 + length_prefix]

            request = card_game_pb2.ReadyGameRequest()
            request.ParseFromString(payload)
            print(f"Received Request: client_id={request.client_id}, game_id={request.game_id}")

            response = card_game_pb2.ReadyGameResponse()
            response.success = True
            response.message = f"Player {request.client_id} is ready for game {request.game_id}"

            serialized_response = response.SerializeToString()
            length_prefix = len(serialized_response).to_bytes(4, byteorder="big")
            self.transport.write(length_prefix + serialized_response)
        except Exception as e:
            print(f"Error processing request: {e}")


class CardGameFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return CardGameProtocol()


if __name__ == "__main__":
    reactor.listenTCP(8000, CardGameFactory())
    print("Server is running on port 8000.")
    reactor.run()
