# ZAP Scanning Report

ZAP by [Checkmarx](https://checkmarx.com/).


## Summary of Alerts

| Risk Level | Number of Alerts |
| --- | --- |
| High | 0 |
| Medium | 1 |
| Low | 4 |
| Informational | 1 |




## Insights

| Level | Reason | Site | Description | Statistic |
| --- | --- | --- | --- | --- |
| Low | Warning |  | ZAP errors logged - see the zap.log file for details | 16    |
| Low | Exceeded High | http://backend:5000 | Percentage of responses with status code 4xx | 76 % |
| Info | Informational |  | Percentage of network failures | 1 % |
| Info | Informational | http://backend:5000 | Percentage of responses with status code 2xx | 23 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with content type application/json | 97 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with content type text/html | 2 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method DELETE | 10 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method GET | 50 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method POST | 28 % |
| Info | Informational | http://backend:5000 | Percentage of endpoints with method PUT | 10 % |
| Info | Informational | http://backend:5000 | Count of total endpoints | 38    |







## Alerts

| Name | Risk Level | Number of Instances |
| --- | --- | --- |
| Cross-Domain Misconfiguration | Medium | Systemic |
| A Server Error response code was returned by the server | Low | 1 |
| Server Leaks Version Information via "Server" HTTP Response Header Field | Low | Systemic |
| Unexpected Content-Type was returned | Low | 1 |
| X-Content-Type-Options Header Missing | Low | Systemic |
| A Client Error response code was returned by the server | Informational | 37 |




## Alert Detail



### [ Cross-Domain Misconfiguration ](https://www.zaproxy.org/docs/alerts/10098/)



##### Medium (Medium)

### Description

Web browser data loading may be possible, due to a Cross Origin Resource Sharing (CORS) misconfiguration on the web server.

* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title,description})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1 ()({title,description})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`
* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1 ()({title,order_index,completed})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Access-Control-Allow-Origin: *`
  * Other Info: `The CORS misconfiguration on the web server permits cross-domain read requests from arbitrary third party domains, using unauthenticated APIs on this domain. Web browser implementations do not permit arbitrary third parties to read the response from authenticated APIs, however. This reduces the risk somewhat. This misconfiguration could be used by an attacker to access data that is available in an unauthenticated manner, but which uses some other form of security, such as IP address white-listing.`

Instances: Systemic


### Solution

Ensure that sensitive data is not available in an unauthenticated manner (using IP address white-listing, for instance).
Configure the "Access-Control-Allow-Origin" HTTP header to a more restrictive set of domains, or remove all CORS headers entirely, to allow the web browser to enforce the Same Origin Policy (SOP) in a more restrictive manner.

### Reference


* [ https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy ](https://vulncat.fortify.com/en/detail?category=HTML5&subcategory=Overly%20Permissive%20CORS%20Policy)


#### CWE Id: [ 264 ](https://cwe.mitre.org/data/definitions/264.html)


#### WASC Id: 14

#### Source ID: 3

### [ A Server Error response code was returned by the server ](https://www.zaproxy.org/docs/alerts/100000/)



##### Low (High)

### Description

A response code of 500 was returned by the server.
This may indicate that the application is failing to handle unexpected input correctly.
Raised by the 'Alert on HTTP Response Code Error' script

* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title,description})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `500`
  * Other Info: ``


Instances: 1

### Solution



### Reference



#### CWE Id: [ 388 ](https://cwe.mitre.org/data/definitions/388.html)


#### WASC Id: 20

#### Source ID: 4

### [ Server Leaks Version Information via "Server" HTTP Response Header Field ](https://www.zaproxy.org/docs/alerts/10036/)



##### Low (High)

### Description

The web/application server is leaking version information via the "Server" HTTP response header. Access to such information may facilitate attackers identifying other vulnerabilities your web/application server is subject to.

* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1`
  * Method: `DELETE`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.12.15`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.12.15`
  * Other Info: ``
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title,description})`
  * Method: `POST`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.12.15`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1 ()({title,description})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.12.15`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/items/1
  * Node Name: `http://backend:5000/api/checklists/items/1 ()({title,order_index,completed})`
  * Method: `PUT`
  * Parameter: ``
  * Attack: ``
  * Evidence: `Werkzeug/3.1.9 Python/3.12.15`
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

### [ Unexpected Content-Type was returned ](https://www.zaproxy.org/docs/alerts/100001/)



##### Low (High)

### Description

A Content-Type of text/html was returned by the server.
This is not one of the types expected to be returned by an API.
Raised by the 'Alert on Unexpected Content Types' script

* URL: http://backend:5000/api/checklists/items/8681606605048168875
  * Node Name: `http://backend:5000/api/checklists/items/8681606605048168875`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `text/html`
  * Other Info: ``


Instances: 1

### Solution



### Reference




#### Source ID: 4

### [ X-Content-Type-Options Header Missing ](https://www.zaproxy.org/docs/alerts/10021/)



##### Low (Medium)

### Description

The Anti-MIME-Sniffing header X-Content-Type-Options was not set to 'nosniff'. This allows older versions of Internet Explorer and Chrome to perform MIME-sniffing on the response body, potentially causing the response body to be interpreted and displayed as a content type other than the declared content type. Current (early 2014) and legacy versions of Firefox will use the declared content type (if one is set), rather than performing MIME-sniffing.

* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1`
  * Method: `GET`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`
* URL: http://backend:5000/api/checklists/health
  * Node Name: `http://backend:5000/api/checklists/health`
  * Method: `GET`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`
* URL: http://backend:5000/health
  * Node Name: `http://backend:5000/health`
  * Method: `GET`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title,description})`
  * Method: `POST`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`
* URL: http://backend:5000/api/checklists/1
  * Node Name: `http://backend:5000/api/checklists/1 ()({title,description})`
  * Method: `PUT`
  * Parameter: `x-content-type-options`
  * Attack: ``
  * Evidence: ``
  * Other Info: `This issue still applies to error type pages (401, 403, 500, etc.) as those pages are often still affected by injection issues, in which case there is still concern for browsers sniffing pages away from their actual content type.
At "High" threshold this scan rule will not alert on client or server error responses.`

Instances: Systemic


### Solution

Ensure that the application/web server sets the Content-Type header appropriately, and that it sets the X-Content-Type-Options header to 'nosniff' for all web pages.
If possible, ensure that the end user uses a standards-compliant and modern web browser that does not perform MIME-sniffing at all, or that can be directed by the web application/web server to not perform MIME-sniffing.

### Reference


* [ https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/compatibility/gg622941(v=vs.85) ](https://learn.microsoft.com/en-us/previous-versions/windows/internet-explorer/ie-developer/compatibility/gg622941(v=vs.85))
* [ https://owasp.org/www-community/Security_Headers ](https://owasp.org/www-community/Security_Headers)


#### CWE Id: [ 693 ](https://cwe.mitre.org/data/definitions/693.html)


#### WASC Id: 15

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
* URL: http://backend:5000/5421841485097980337
  * Node Name: `http://backend:5000/5421841485097980337`
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
* URL: http://backend:5000/api/1775197079102001349
  * Node Name: `http://backend:5000/api/1775197079102001349`
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
* URL: http://backend:5000/api/checklists/1/4129573498279717550
  * Node Name: `http://backend:5000/api/checklists/1/4129573498279717550`
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
* URL: http://backend:5000/api/checklists/1772320597145798372
  * Node Name: `http://backend:5000/api/checklists/1772320597145798372`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists/health/
  * Node Name: `http://backend:5000/api/checklists/health/`
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
* URL: http://backend:5000/api/checklists/items/8681606605048168875
  * Node Name: `http://backend:5000/api/checklists/items/8681606605048168875`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `405`
  * Other Info: ``
* URL: http://backend:5000/health/
  * Node Name: `http://backend:5000/health/`
  * Method: `GET`
  * Parameter: ``
  * Attack: ``
  * Evidence: `404`
  * Other Info: ``
* URL: http://backend:5000/api/checklists
  * Node Name: `http://backend:5000/api/checklists ()({title,description})`
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


Instances: 37

### Solution



### Reference



#### CWE Id: [ 388 ](https://cwe.mitre.org/data/definitions/388.html)


#### WASC Id: 20

#### Source ID: 4


