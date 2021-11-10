## videoReceiver

基于socket通信的传输视频文件服务端

### 配置文件

## 数据格式定义

****

#### 获取文件夹信息

get_dirs 获取服务器上的所有视频文件夹信息

#### Request

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
  "command": "getDirs",
  "code": 0
}
```

#### Response

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
  "command": "getDirs",
  "code": 200,
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

#### 获取文件信息

get_videos 获取一个文件夹内的所有文件信息

#### Request

- head

```json
{
  "command": "getVideos",
  "code": 1,
  "msgSize": 0
}
```

- body

```json
{
  "command": "getVideos",
  "code": 1,
  "dirNumber": 0,
  "dirName": [
    "dirName"
  ]
}
```

#### Response

- head

```json
{
  "command": "getVideos",
  "code": 200,
  "msgSize": 0
}
```

- body

```json
{
  "command": "getVideos",
  "code": 200,
  "dirNumber": 0,
  "dirs": {
    "videos": {
      "videoNumber": 0,
      "video1": {
        "videoName": "",
        "videoImage": ""
      },
      "video2": {
        "videoName": "",
        "videoImage": ""
      }
    }
  }
}
```

#### 下载视频文件

下载单个视频文件

#### Request

- head

```json
{
  "command": "download",
  "code": 2,
  "msgSize": 0
}
```

- body

```json
{
  "command": "download",
  "code": 2,
  "videoDir": "",
  "videoName": ""
}
```

#### Response

- head

```json
{
  "command": "download",
  "code": 200,
  "msgSize": 0
}
```

- body

```json
{
  "videoNumber": 0,
  "videos": {
    "video1": {
      "name": "",
      "size": ""
    },
    "video2": {
      "name": "",
      "size": ""
    }
  }
}
```
