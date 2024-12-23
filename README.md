# Load Balancer - Python

## How To ?
1. Start the loadbalancer by running the file `lb.py`
```python3 lb.py```
![image](https://github.com/user-attachments/assets/d1850814-6b11-4ea1-be90-0ec535d5b03a)

2. Start the backend servers by running the file `be.py`
```python3 be.py <port>```
![image](https://github.com/user-attachments/assets/9f2fd4f2-986a-47c8-a037-e9b28af4ad37)

3. You can start multiple instances of the server by running it on different ports
4. Make a request to the loadbalancer
   
![image](https://github.com/user-attachments/assets/72f331df-4418-4826-8522-dd2bf2ac1821)



## Docs
- `lb.py` contains the loadbalancer that runs a TCPServer and forwards the requests to the list of healthy servers
- `be.py` contains a demo backend server that again starts a TCPServer at the specified port and responds to requests with a generic message
- `health.py` contains the health check loop that checks the health of the available servers every x seconds
- `strategy` Contains the `ServerSelectionStrategy` base class to choose the next server from the list of availabe ones
  
