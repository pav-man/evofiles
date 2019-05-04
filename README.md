Description
Файловый хостинг для удаленного хранения файлов.

Installation
python3.6
nginx
supervisor

Проект реализован на aiohttp, база данных aiosqlite.
По линке https://evofiles.club/d9d60eeb, полученную при загрузке, показывается статистику файла и
link на download https://evofiles.club/files/d9d60eeb/pxiByp8kv8JHgFVrLDz8Z1xlFQ.woff2
Отдача контента через nginx.
Удаление файлов и очищение базы, от проэкспайриных файлов реализованно модулем через middleware.




