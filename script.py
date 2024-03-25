from whatsapp_api_client_python import API
import re
def main():
  greenAPI.webhooks.startReceivingNotifications(handler)


def handler(type_webhook: str, body: dict) -> None:
    if type_webhook == "incomingMessageReceived":
        incoming_message_received(body)

def incoming_message_received(body: dict) -> None:
    data = dumps(body, ensure_ascii=False, indent=4)
    x = re.search(r'"textMessage":.*"', data)
    message=(x.group().split(':')[1][2:(len(x.group().split(':')[1])-1)])
    print(message)

if __name__ == '__main__':
    main()
