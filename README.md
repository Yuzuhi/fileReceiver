# fileReceiver
- 利用tkinter模块编写Python语言的GUI程序，通过tcp通信的方式来接收文件

# 数据格式定义

## Request

****

### get_files

- head

```json
{
  "command": "getFiles",
  "code": 1,
  "msgSize": 0
}
```

- body

```json
{
  "dirPath": ""
}
```

### get_dirs

- head

```json
{
  "command": "getDirs",
  "code": 0,
  "msgSize": 0
}
```

- body

```json
{
  "basePath": ""
}
```

****

#### single_download

- head

```json
{
  "command": "singleDownload",
  "code": 2,
  "msgSize": 0
}
```

- body

```json
{
  "animePath": "",
  "animeName": ""
}
```

****

#### multi_download

- head

```json
{
  "command": "multiDownload",
  "code": 3,
  "msgSize": 0
}
```

- body

```json
{
  "animeNumber": 0,
  "animes": {
    "anime1": {
      "name": ""
    },
    "anime2": {
      "name": ""
    }
  }
}
```

****

## Response

### get_files

- head

```json
{
  "command": "getFiles",
  "code": 1,
  "msgSize": 0
}
```

- body

```json
{
  "fileNumber": 0,
  "files": {
    "file1": {
      "fileName": "",
      "fileImage": ""
    },
    "file2": {
      "fileName": "",
      "fileImage": ""
    }
  }
}
```

****

### get_dirs

- head

```json
{
  "command": "getDirs",
  "code": 0,
  "msgSize": 0
}
```

- body

```json
{
  "dirNumbers": 0,
  "dirs": {
    "dir1": {
      "dirName": "",
      "dirImage": ""
    },
    "dir2": {
      "dirName": "",
      "dirImage": ""
    }
  }
}

```

****

#### single_download

- head

```json
{
  "command": "singleDownload",
  "code": 2,
  "msgSize": 0
}
```

- body

```json
{
  "name": "",
  "size": 0
}
```

****

#### multi_download

- head

```json
{
  "command": "multiDownload",
  "code": 3,
  "msgSize": 0
}
```

- body

```json
{
  "animeNumber": 0,
  "animes": {
    "anime1": {
      "name": "",
      "size": ""
    },
    "anime2": {
      "name": "",
      "size": ""
    }
  }
}
```
