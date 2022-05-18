docker run -d --name sonarqube -e SONAR_ES_BOOTSTRAP_CHECKS_DISABLE=true -p 9000:9000 sonarqube:latest

docker run \
    --rm \
    --link sonarqube \
    -e SONAR_HOST_URL="http://${SONARQUBE_URL}" \
    -e SONAR_LOGIN="6d4a4e95b06e8626379c4e833423d41b11f244e6" \
    -v "/Users/pierre/+code/biggie:/usr/src" \
    sonarsource/sonar-scanner-cli

sonar-scanner -X \
  -Dsonar.python.version=3 \
  -Dsonar.projectKey=biggie_key \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=b4ed8d8df1e8fb927398fb72aac8202d41c98c64

sonar-scanner \
  -Dsonar.projectKey=biggie \
  -Dsonar.sources=. \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=6d4a4e95b06e8626379c4e833423d41b11f244e6
