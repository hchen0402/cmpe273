"""
Question:
Pick one IP from each region',' find network latency from via the below code snippet
(ping 3 times)',' and finally sort the average latency by region.
http://ec2-reachability.amazonaws.com/
Expected Output for all 15 regions:
1. us-west-1 [50.18.56.1] - 100ms (Smallest average latency)
2. xx-xxxx-x [xx.xx.xx.xx] - 200ms
3. xx-xxxx-x [xx.xx.xx.xx] - 300ms
...
15. xx-xxxx-x [xx.xx.xx.xx] - 1000ms (Largest average latency)
"""
import subprocess

hosts = {'us-east-1': '23.23.255.255', 'us-east-2': '13.58.0.253', 'us-west-1': '13.56.63.251', 'us-west-2': '34.208.63.251', 'us-gov-west-1': '52.61.0.254', 'ca-central-1': '35.182.0.251', 'eu-west-1':'34.240.0.253', 'eu-central-1': '18.194.0.252', 'eu-west-2': '35.176.0.252', 'ap-northeast-1': '13.112.63.251', 'ap-northeast-2': '13.124.63.251', 'ap-southeast-1': '13.228.0.251', 'ap-southeast-2':'13.54.63.252', 'ap-south-1':'13.126.0.252', 'sa-east-1':'18.231.0.252'}
result = {}

for region in list(hosts.keys()):
	host = hosts[region]
	ping = subprocess.Popen(
	    ["ping", "-c", "3", host],
	    stdout = subprocess.PIPE,
	    stderr = subprocess.PIPE
	)
	
	out, error = ping.communicate()
	avg_value = out.split("/")
	result[float(avg_value[4])] = region

avgs = sorted(result.keys())

count = 1
for avg in avgs:
	print str(count) + ". " + result[avg] + " [" + hosts[result[avg]] + "] - " + str(avg) + "ms"
	count += 1

"""
Output:
1. us-west-1 [13.56.63.251] - 4.129ms
2. us-west-2 [34.208.63.251] - 27.141ms
3. us-gov-west-1 [52.61.0.254] - 27.281ms
4. us-east-2 [13.58.0.253] - 52.806ms
5. us-east-1 [23.23.255.255] - 70.328ms
6. ca-central-1 [35.182.0.251] - 82.628ms
7. ap-northeast-1 [13.112.63.251] - 103.235ms
8. ap-northeast-2 [13.124.63.251] - 139.751ms
9. eu-west-2 [35.176.0.252] - 148.466ms
10. eu-central-1 [18.194.0.252] - 158.043ms
11. eu-west-1 [34.240.0.253] - 169.154ms
12. sa-east-1 [18.231.0.252] - 175.835ms
13. ap-south-1 [13.126.0.252] - 310.695ms
14. ap-southeast-2 [13.54.63.252] - 315.196ms
15. ap-southeast-1 [13.228.0.251] - 330.135ms
"""