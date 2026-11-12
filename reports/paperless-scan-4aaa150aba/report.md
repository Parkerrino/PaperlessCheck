# ZAP Scanning Report

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 0 |
| Low | 1 |
| Informational | 1 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Medium | Exceeded High | http://backend:5000 | Percentage of responses with status code 4xx | 68 % |
| Low | Warning |  | ZAP errors logged - see the zap.log file for details | 16    |
| Info | Informational |  | Percentage of network failures | 1 % |
| Info | Informational | http://backend:5000 | Percentage of responses with status code 2xx | 31 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with content type application/json | 100 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method DELETE | 15 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method GET | 39 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method POST | 34 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method PUT | 10 % |
| Info | Informational | http://backend:5000 | Count of total endpoints | 38    |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Server Leaks Version Information via "Server" HTTP Response Header Field | Low | Systemic |
| A Client Error response code was returned by the server | Informational | 38 |




## Alert Detail



### [ Server Leaks Version Information via "Server" HTTP Response Header Field ](https://www.zaproxy.org/docs/alerts/10036/)



##### Low (High)

### Description

The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.

* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.14.9`
  * Other Info: ``
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.14.9`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/items
  * Node Name: `http://backend:5000/api/checklists/1/items ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.14.9`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1 ()({title,description})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.14.9`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1 ()({title,order_index,completed})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.14.9`
  * Other Info: ``

Instances: Systemic


### Solution

Ensure that your web server, application server, load balancer, etc. is configured to suppress the "Server" header or provide generic details.

### Reference


* [ https://httpd.apache.org/docs/current/mod/core.html#servertokens ](https://httpd.apache.org/docs/current/mod/core.html#servertokens)
* [ https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648552(v=pandp.10) ](https://learn.microsoft.com/en-us/previous-versions/msp-n-p/ff648552(v=pandp.10))
* [ https://www.troyhunt.com/shhh-dont-let-your-response-headers/ ](https://www.troyhunt.com/shhh-dont-let-your-response-headers/)


#### CWE Id: [ 497 ](https://cwe.mitre.org/data/definitions/497.html)


#### WASC Id: 13

#### Source ID: 3

### [ A Client Error response code was returned by the server ](https://www.zaproxy.org/docs/alerts/100000/)



##### Informational (High)

### Description

A response code of 404 was returned by the server.
This may indicate that the application is failing to handle unexpected input correctly.
Raised by the 'Alert on HTTP Response Code Error' script

* URL: http://backend:5000/api/checklists/1/
  * Node Name: `http://backend:5000/api/checklists/1/`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/4/
  * Node Name: `http://backend:5000/api/checklists/4/`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1/
  * Node Name: `http://backend:5000/api/checklists/items/1/`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000
  * Node Name: `http://backend:5000`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/
  * Node Name: `http://backend:5000/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/4936018203565244272
  * Node Name: `http://backend:5000/4936018203565244272`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api
  * Node Name: `http://backend:5000/api`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/
  * Node Name: `http://backend:5000/api/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/4934553741291248655
  * Node Name: `http://backend:5000/api/4934553741291248655`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/
  * Node Name: `http://backend:5000/api/checklists/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/
  * Node Name: `http://backend:5000/api/checklists/1/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/2774548590836278374
  * Node Name: `http://backend:5000/api/checklists/1/2774548590836278374`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/actuator/health
  * Node Name: `http://backend:5000/api/checklists/1/actuator/health`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1387021555475166554
  * Node Name: `http://backend:5000/api/checklists/1387021555475166554`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items
  * Node Name: `http://backend:5000/api/checklists/items`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/
  * Node Name: `http://backend:5000/api/checklists/items/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/4075856196793890164
  * Node Name: `http://backend:5000/api/checklists/items/4075856196793890164`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `405`
  * Other Info: ``
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title,description})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `400`
  * Other Info: ``
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `400`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/
  * Node Name: `http://backend:5000/api/checklists/ ()({title,description})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/
  * Node Name: `http://backend:5000/api/checklists/ ()({title})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/items
  * Node Name: `http://backend:5000/api/checklists/1/items ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `400`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/items
  * Node Name: `http://backend:5000/api/checklists/1/items ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/items/
  * Node Name: `http://backend:5000/api/checklists/1/items/ ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/computeMetadata/v1/
  * Node Name: `http://backend:5000/computeMetadata/v1/ ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/latest/meta-data/
  * Node Name: `http://backend:5000/latest/meta-data/ ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/metadata/instance
  * Node Name: `http://backend:5000/metadata/instance ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/metadata/v1
  * Node Name: `http://backend:5000/metadata/v1 ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/opc/v1/instance/
  * Node Name: `http://backend:5000/opc/v1/instance/ ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/opc/v2/instance/
  * Node Name: `http://backend:5000/opc/v2/instance/ ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/openstack/latest/meta_data.json
  * Node Name: `http://backend:5000/openstack/latest/meta_data.json ()({title,order_index,completed})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1 ()({title,description})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `400`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1 ()({title,description})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1/
  * Node Name: `http://backend:5000/api/checklists/1/ ()({title,description})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1 ()({title,order_index,completed})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `400`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1 ()({title,order_index,completed})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1/
  * Node Name: `http://backend:5000/api/checklists/items/1/ ()({title,order_index,completed})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``


Instances: 38

### Solution



### Reference



#### CWE Id: [ 388 ](https://cwe.mitre.org/data/definitions/388.html)


#### WASC Id: 20

#### Source ID: 4


