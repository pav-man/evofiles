Description
Файловый хостинг для удаленного хранения файлов.

Installation
python3.6
nginx
supervisor

Проект реализован на aiohttp, база данных aiosqlite.
Nginx с проксированием через unix.socks на aiohttp.
Запуск через suprevisor 4 процесса, настройки в server.conf/supervisor

По линке загруженного файла https://evofiles.club/ebaf6e20, показывается статистика файла
и link на download https://evofiles.club/files/ebaf6e20/pxiByp8kv8JHgFVrLDz8Z1xlFQ.woff2,
для возможности отдать напряму через nginx,

Зарегистрированный пользователь может видить список своих загруженных файлов.

Удаление файлов и очищение базы, от проэкспайриных файлов реализованно модулем через middleware.





