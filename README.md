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
ab -n 500 -c 10 -r http://localhost:8080/httptest/dir2/
```
Для 2 воркеров  
Server Software:        DZ5  
Server Hostname:        localhost  
Server Port:            8080  

Document Path:          /httptest/dir2/  
Document Length:        34 bytes  

Concurrency Level:      10  
Time taken for tests:   503.187 seconds  
Complete requests:      500  
Failed requests:        0  
Total transferred:      83500 bytes  
HTML transferred:       17000 bytes  
Requests per second:    0.99 [#/sec] (mean)  
Time per request:       10063.738 [ms] (mean)  
Time per request:       1006.374 [ms] (mean, across all concurrent requests)  
Transfer rate:          0.16 [Kbytes/sec] received  

Connection Times (ms)  
              min  mean[+/-sd] median   max  
Connect:        0    1   0.5      1       1  
Processing:  1008 9911 845.9  10017   10108  
Waiting:     1008 9910 845.9  10017   10107  
Total:       1008 9911 846.0  10017   10108  

Percentage of the requests served within a certain time (ms)  
  50%  10017  
  66%  10027  
  75%  10034  
  80%  10037  
  90%  10050  
  95%  10059  
  98%  10074  
  99%  10082  
 100%  10108 (longest request)  
Для 4 воркеров  
Server Software:        DZ5  
Server Hostname:        localhost  
Server Port:            8080  

Document Path:          /httptest/dir2/  
Document Length:        34 bytes  

Concurrency Level:      10  
Time taken for tests:   503.071 seconds  
Complete requests:      500  
Failed requests:        0  
Total transferred:      83500 bytes  
HTML transferred:       17000 bytes  
Requests per second:    0.99 [#/sec] (mean)  
Time per request:       10061.418 [ms] (mean)  
Time per request:       1006.142 [ms] (mean, across all concurrent requests)  
Transfer rate:          0.16 [Kbytes/sec] received  

Connection Times (ms)  
              min  mean[+/-sd] median   max  
Connect:        0    1   0.5      1       1  
Processing:  1033 9910 846.4  10017   10085  
Waiting:     1033 9909 846.4  10017   10085  
Total:       1033 9910 846.4  10017   10086  
  
Percentage of the requests served within a certain time (ms)  
  50%  10017  
  66%  10023  
  75%  10027  
  80%  10030  
  90%  10037  
  95%  10044  
  98%  10052  
  99%  10059  
 100%  10086 (longest request)   
 
