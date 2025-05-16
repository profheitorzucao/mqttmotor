import machine
import time
import network
from umqtt.simple import MQTTClient

# Configuração do WiFi
SSID = 'devsenai'  # Substitua pelo nome da sua rede WiFi
PASSWORD = '12345678'  # Substitua pela senha da sua rede WiFi

# Configuração do cliente MQTT
MQTT_BROKER = 'jaragua.lmq.cloudamqp.com'
MQTT_TOPIC = 'test/esp32'
MQTT_USER = 'iouytvhh:iouytvhh'
MQTT_PASSWORD = 'Ct8TS8VQpbyTGL1OtKEr_KBUxsSzvQUr'

# Configuração do pino ADC (usando GPIO34 neste caso)
pot_pin = machine.Pin(34)  # Pino GPIO34 como entrada
adc = machine.ADC(pot_pin)  # Configura o pino como ADC
adc.atten(machine.ADC.ATTN_0DB)  # Atenuação 0 dB para a faixa de 0-3.3V
adc.width(machine.ADC.WIDTH_12BIT)  # Resolução de 12 bits (0-4095)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Conectando-se à rede...')
        wlan.connect(SSID, PASSWORD)
        while not wlan.isconnected():
            time.sleep(1)
    print('Conexão estabelecida:', wlan.ifconfig())

# Função de callback para o MQTT (quando uma nova mensagem é recebida)
def mqtt_callback(topic, msg):
    print(f"Mensagem recebida do tópico {topic}: {msg}")

# Função principal
def main():
    connect_wifi()  # Conectar-se à rede WiFi

    # Configura o cliente MQTT
    client = MQTTClient('espclient', MQTT_BROKER, '1883', MQTT_USER, MQTT_PASSWORD)
    client.set_callback(mqtt_callback)

    try:
        client.connect()
        print("Conectado ao broker MQTT")
        time.sleep(2)

        # Subscreve ao tópico
        client.subscribe(MQTT_TOPIC)
        print(f"Subscrito no tópico {MQTT_TOPIC}")
        
        
        pot_mqtt =0
        # Loop para verificar alteração de valor e publicar e checar mensagem
        while True:
              pot_value = adc.read()
              if pot_value != pot_mqtt:
                  pot_mqtt = pot_value
                  print("Valor do Potenciômetro:", pot_value)
                  client.publish(MQTT_TOPIC, str(pot_mqtt))
                  print("Mensagem publicada no tópico")
                  time.sleep(0.1)
            # Verifica se há mensagens novas sem bloquear o código
              
              client.check_msg() 
    except OSError as e:
        print("Erro de conexão:", e)
        print("Tentando reconectar...")
        time.sleep(5)
        main()
#Chamada do main    
main()