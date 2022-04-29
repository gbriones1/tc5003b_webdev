#!/bin/bash

for i in $(seq 1 10000); do
    echo $i;
    curl -X 'POST' \
 'http://127.0.0.1:8000/user/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d "{
  \"is_manager\": false,
  \"first_name\": \"user${i}\",
  \"last_name\": \"${i}\",
  \"email\": \"\",
  \"user_type_utid\": \"9064f3fe-11de-4b4c-ab66-4e068e2630b4\"
}"
done