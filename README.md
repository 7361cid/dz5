## Архитектура
Используется thread pool
## запуск сервера 
```
python httpd.py -r [path_to_data_dir]  -w [workers_count] -p [port]
```
## запуск тестов
```
python tests.py
```
## результаты нагрузочного тестирование
Параметры запуска
```
ab -n 500 -c 100 -r http://localhost:8080/
```
Для 2 воркеров
Concurrency Level:      100  
Time taken for tests:   505.643 seconds  
Complete requests:      500  
Failed requests:        0  
Non-2xx responses:      500  
Total transferred:      59500 bytes  
HTML transferred:       0 bytes  
Requests per second:    0.99 [#/sec] (mean)  
Time per request:       101128.530 [ms] (mean)  
Time per request:       1011.285 [ms] (mean, across all concurrent requests)  
Transfer rate:          0.11 [Kbytes/sec] received  

Connection Times (ms)  
              min  mean[+/-sd] median   max  
Connect:        0    1   0.5      1       1  
Processing:  1017 90717 24172.4 100874  101050  
Waiting:     1016 90716 24172.8 100874  101049  
Total:       1017 90717 24172.5 100874  101051  

Percentage of the requests served within a certain time (ms) 
  50%  100874  
  66%  100905  
  75%  100927  
  80%  100941  
  90%  100974  
  95%  100995  
  98%  101012  
  99%  101031  
 100%  101051 (longest request)  
Для 4 воркеров
Concurrency Level:      100  
Time taken for tests:   505.908 seconds  
Complete requests:      500  
Failed requests:        0  
Non-2xx responses:      500  
Total transferred:      59500 bytes  
HTML transferred:       0 bytes  
Requests per second:    0.99 [#/sec] (mean)  
Time per request:       101181.586 [ms] (mean)  
Time per request:       1011.816 [ms] (mean, across all concurrent requests)  
Transfer rate:          0.11 [Kbytes/sec] received  

Connection Times (ms)  
              min  mean[+/-sd] median   max  
Connect:        0    1   0.5      1       1  
Processing:  1006 90754 24174.3 100920  101036  
Waiting:     1006 90753 24174.7 100919  101036  
Total:       1007 90754 24174.3 100920  101036  

Percentage of the requests served within a certain time (ms)  
  50%  100920  
  66%  100944  
  75%  100956  
  80%  100961  
  90%  100978  
  95%  100991  
  98%  101011  
  99%  101023  
 100%  101036 (longest request)  
 
