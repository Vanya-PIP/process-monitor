# process-monitor (Veeam Software Test assignment part 1)

Based on [hardware_monitor](https://github.com/Vanya-PIP/hardware_monitor)

## The test assignment text

Написать программу, которая будет запускать процесс и с указанным интервалом времени собирать о нём следующую статистику:

- Загрузка CPU (в процентах);
- Потребление памяти: Working Set и Private Bytes (для Windows-систем) или Resident Set Size и Virtual Memory Size (для Linux-систем);
- Количество открытых хендлов (для Windows-систем) или файловых дескрипторов (для Linux-систем).

Сбор статистики должен осуществляться всё время работы запущенного процесса. Путь к файлу, который необходимо запустить, и интервал сбора статистики должны указываться пользователем. Собранную статистику необходимо сохранить на диске. Представление данных должно в дальнейшем позволять использовать эту статистику для автоматизированного построения графиков потребления ресурсов.

## Usage

```
usage: python -m process_monitor [-h] (--pid PID | --name NAME) [-s SECS] [-m MINS] [-hr HOURS] [-d DIR]

Log process info at specified interval (default: 1 sec)

options:
  -h, --help            show this help message and exit
  --pid PID
  --name NAME
  -s SECS, --secs SECS
  -m MINS, --mins MINS
  -hr HOURS, --hours HOURS
  -d DIR, --dir DIR     logs directory (default: cwd)
```

## Requirements

- Python 3.9+
- [`psutil`](https://pypi.org/project/psutil/)
