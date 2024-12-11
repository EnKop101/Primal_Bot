from rcon.source import Client

with Client('168.119.3.226', 27022, passwd='h#iamchaos213') as client:
    response = client.run('getchat')

print(response)