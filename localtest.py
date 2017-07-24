from server import run
import client
'''
DRIVER PROGRAM FOR LOCAL TEST
'''


run('localhost',8999)
client.client()
client.close()