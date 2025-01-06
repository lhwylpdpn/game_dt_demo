from twisted.internet import protocol, reactor
import card_game_pb2


class CardGameClient(protocol.Protocol):
    def connectionMade(self):
        print("Connected to server")

        request = card_game_pb2.ReadyGameRequest()
        request.client_id = "player_123"
        request.game_id = "game_456"

        serialized_request = request.SerializeToString()
        length_prefix = len(serialized_request).to_bytes(4, byteorder="big")
        self.transport.write(length_prefix + serialized_request)

    def dataReceived(self, data):
        try:
            if len(data) < 4:
                print("Incomplete data: waiting for length prefix")
                return

            length_prefix = int.from_bytes(data[:4], byteorder="big")
            payload = data[4:4 + length_prefix]

            response = card_game_pb2.ReadyGameResponse()
            response.ParseFromString(payload)
            print(f"Received Response: success={response.success}, message={response.message}")
        except Exception as e:
            print(f"Error parsing response: {e}")

        self.transport.loseConnection()


class CardGameClientFactory(protocol.ClientFactory):
    protocol = CardGameClient

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason}")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection closed.")
        reactor.stop()


if __name__ == "__main__":
    reactor.connectTCP("localhost", 8000, CardGameClientFactory())
    reactor.run()
