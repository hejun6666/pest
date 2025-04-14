# 农作物病虫害检测预警系统API测试文档

本文档提供了使用Postman测试农作物病虫害检测预警系统后端API接口的详细指南。

## 目录

- [准备工作](#准备工作)
- [用户相关接口](#用户相关接口)
- [病虫害检测接口](#病虫害检测接口)
- [病虫害信息接口](#病虫害信息接口)
- [预警相关接口](#预警相关接口)
- [农技资讯接口](#农技资讯接口)
- [社区交流接口](#社区交流接口)
- [管理员接口](#管理员接口)
- [错误测试](#错误测试)
- [测试自动化](#测试自动化)

## 准备工作

### 安装与配置Postman

1. 下载并安装[Postman](https://www.postman.com/downloads/)
2. 创建新的工作空间：「农作物病虫害检测系统测试」
3. 导入环境变量设置：
   - 创建新环境变量：`开发环境`
   - 添加变量 `baseUrl`: `http://localhost:5000`
   - 添加变量 `userId`: 登录后获取的用户ID

### 创建请求集合

1. 在工作空间中创建一个新的集合：「农作物病虫害检测系统API测试」
2. 在集合中创建子文件夹，按照接口分类整理：
   - 用户接口
   - 病虫害检测
   - 病虫害信息
   - 预警管理
   - 农技资讯
   - 社区交流
   - 管理员接口

## 用户相关接口

### 1. 用户注册

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/user/register`
- **描述**：用户注册接口，创建新账号

**请求设置：**
- **Headers**：
  - Content-Type: application/json
- **Body**：选择 `raw` 并设置为 JSON 格式
```json
{
  "username": "test_user",
  "password": "123456",
  "nickname": "测试用户"
}
```

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/user/register`
3. 添加 Content-Type 请求头
4. 在 Body 选项卡中选择 `raw` 并选择 JSON 格式
5. 输入上述 JSON 数据
6. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "userId": 12345,
    "username": "test_user",
    "nickname": "测试用户"
  }
}
```

### 2. 用户登录

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/user/login`
- **描述**：用户登录接口，支持账号密码登录和微信小程序登录

**请求设置(账号密码登录)：**
- **Headers**：
  - Content-Type: application/json
- **Body**：选择 `raw` 并设置为 JSON 格式
```json
{
  "username": "test_user",
  "password": "123456"
}
```

**请求设置(微信小程序登录)：**
- **Headers**：
  - Content-Type: application/json
- **Body**：选择 `raw` 并设置为 JSON 格式
```json
{
  "code": "023vzn000JmXOL1SLr100apCOK0vzn0l",
  "nickname": "测试用户",
  "avatarUrl": "https://example.com/avatar.jpg"
}
```

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/user/login`
3. 添加 Content-Type 请求头
4. 在 Body 选项卡中选择 `raw` 并选择 JSON 格式
5. 输入上述 JSON 数据（根据登录方式选择）
6. 点击"发送"按钮

**预期结果(账号密码登录)：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "userId": 12345,
    "username": "test_user",
    "nickname": "测试用户",
    "avatarUrl": "",
    "userType": 0
  }
}
```

**预期结果(微信登录)：**
```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "userId": 12345,
    "nickname": "测试用户",
    "avatarUrl": "https://example.com/avatar.jpg",
    "userType": 0
  }
}
```

**后续操作：**
- 将返回的 `userId` 保存到环境变量中，以便后续请求使用：
```javascript
var jsonData = pm.response.json();
if (jsonData.code === 200 && jsonData.data && jsonData.data.userId) {
    pm.environment.set('userId', jsonData.data.userId);
}
```

### 3. 获取用户收藏列表

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/user/favorites?userId={{userId}}&page=1&size=10`
- **描述**：获取用户收藏的病虫害、防治措施等信息

**请求设置：**
- **参数**：
  - userId: {{userId}}
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/user/favorites`
3. 添加查询参数：userId、page、size
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取收藏列表成功",
  "data": {
    "total": 8,
    "list": [
      {
        "favoriteId": 123,
        "userId": 12345,
        "targetId": 56,
        "targetType": 2,
        "createTime": "2023-10-15 14:30:22",
        "target": {
          "name": "小麦条锈病",
          "image": "/uploads/pests/wheat_stripe_rust.jpg"
        }
      },
      // 更多收藏项...
    ],
    "page": 1,
    "size": 10
  }
}
```

### 4. 获取用户浏览历史

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/user/history?userId={{userId}}&page=1&size=10`
- **描述**：获取用户的浏览历史记录

**请求设置：**
- **参数**：
  - userId: {{userId}}
  - page: 1
  - size: 10
  - targetType: 2 (可选，按类型筛选，例如2表示病虫害)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/user/history`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取浏览历史成功",
  "data": {
    "total": 15,
    "list": [
      {
        "historyId": 456,
        "userId": 12345,
        "targetId": 78,
        "targetType": 2,
        "updateTime": "2023-10-18 09:45:12",
        "target": {
          "name": "水稻稻瘟病",
          "image": "/uploads/pests/rice_blast.jpg"
        }
      },
      // 更多历史记录...
    ],
    "page": 1,
    "size": 10
  }
}
```

## 病虫害检测接口

### 1. 病虫害图像识别

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/pest/detect`
- **描述**：上传图片进行病虫害识别

**请求设置：**
- **Headers**：无特殊要求
- **Body**：选择 `form-data`
  - Key: `file`，类型选择 `File`
  - Value: 选择一张农作物病虫害图片（JPG、PNG等格式）
  - Key: `userId`，值为 `{{userId}}`（可选，用于记录检测历史）

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/pest/detect`
3. 在 Body 选项卡中选择 `form-data`
4. 添加键值对：Key 为 `file`（类型选择 File），Value 选择一个本地图片文件
5. 添加键值对：Key 为 `userId`，Value 使用环境变量 `{{userId}}`
6. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "检测成功",
  "data": {
    "recordId": 789,
    "imageUrl": "/uploads/detect_images/20230418123045.jpg",
    "result": {
      "pestId": 42,
      "pestCode": "rice_blast",
      "name": "水稻稻瘟病",
      "confidence": 0.95,
      "description": "水稻稻瘟病是由稻瘟病菌引起的一种真菌性病害...",
      "symptoms": "初期在叶片上出现褐色小斑点...",
      "cropName": "水稻"
    },
    "similarResults": [
      {
        "pestId": 43,
        "name": "水稻白叶枯病",
        "confidence": 0.03
      },
      {
        "pestId": 45,
        "name": "水稻纹枯病",
        "confidence": 0.01
      }
    ],
    "detectTime": "2023-10-18 12:30:45"
  }
}
```

### 2. 获取用户检测记录

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/pest/records?userId={{userId}}&page=1&size=10`
- **描述**：获取用户的病虫害检测历史记录

**请求设置：**
- **参数**：
  - userId: {{userId}}
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/pest/records`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取识别记录成功",
  "data": {
    "total": 12,
    "list": [
      {
        "recordId": 789,
        "userId": 12345,
        "imageUrl": "/uploads/detect_images/20230418123045.jpg",
        "pestId": 42,
        "pestName": "水稻稻瘟病",
        "confidence": 0.95,
        "createTime": "2023-10-18 12:30:45"
      },
      // 更多记录...
    ],
    "page": 1,
    "size": 10
  }
}
```

## 病虫害信息接口

### 1. 获取病虫害列表

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/pest/list?page=1&size=10`
- **描述**：获取系统中的病虫害信息列表

**请求设置：**
- **参数**：
  - keyword: 水稻 (可选，搜索关键词)
  - cropId: 1 (可选，作物ID筛选)
  - typeId: 2 (可选，病虫害类型ID筛选)
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/pest/list`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取病虫害列表成功",
  "data": {
    "total": 53,
    "list": [
      {
        "pestId": 42,
        "pestCode": "rice_blast",
        "chineseName": "水稻稻瘟病",
        "englishName": "Rice Blast",
        "cropId": 1,
        "cropName": "水稻",
        "typeId": 1,
        "typeName": "真菌性病害",
        "imageUrl": "/uploads/pests/rice_blast.jpg",
        "shortDesc": "水稻上最常见的真菌性病害之一"
      },
      // 更多病虫害...
    ],
    "page": 1,
    "size": 10
  }
}
```

### 2. 获取病虫害详情

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/pest/detail/42?userId={{userId}}`
- **描述**：获取特定病虫害的详细信息

**请求设置：**
- **Path参数**：
  - pestId: 42 (病虫害ID)
- **Query参数**：
  - userId: {{userId}} (可选，用于记录浏览历史)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/pest/detail/42`
3. 添加查询参数 userId
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取病虫害详情成功",
  "data": {
    "pestId": 42,
    "pestCode": "rice_blast",
    "chineseName": "水稻稻瘟病",
    "englishName": "Rice Blast",
    "latinName": "Magnaporthe oryzae",
    "aliases": "稻热病、稻瘟病",
    "cropId": 1,
    "cropName": "水稻",
    "typeId": 1,
    "typeName": "真菌性病害",
    "symptoms": "初期在叶片上出现褐色小斑点，逐渐扩大为纺锤形病斑...",
    "causes": "由稻瘟病菌(Magnaporthe oryzae)引起，在高温高湿条件下易发生...",
    "lifecycle": "病菌以菌丝体或分生孢子在病株残体上越冬...",
    "imageUrl": "/uploads/pests/rice_blast.jpg",
    "moreImages": [
      "/uploads/pests/rice_blast_leaf.jpg",
      "/uploads/pests/rice_blast_neck.jpg"
    ],
    "controlMeasures": [
      {
        "measureId": 101,
        "title": "农业防治",
        "content": "选用抗病品种，合理密植，适量施肥..."
      },
      {
        "measureId": 102,
        "title": "化学防治",
        "content": "可用三环唑、嘧菌酯等杀菌剂进行防治..."
      }
    ],
    "isFavorite": false
  }
}
```

### 3. 获取防治措施详情

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/control/detail/101?userId={{userId}}`
- **描述**：获取特定防治措施的详细信息

**请求设置：**
- **Path参数**：
  - measureId: 101 (防治措施ID)
- **Query参数**：
  - userId: {{userId}} (可选，用于记录浏览历史)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/control/detail/101`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取防治措施详情成功",
  "data": {
    "measureId": 101,
    "title": "水稻稻瘟病农业防治方法",
    "pestId": 42,
    "pestName": "水稻稻瘟病",
    "type": 1,
    "typeName": "农业防治",
    "content": "1. 选用抗病品种：推荐种植抗稻瘟病的品种...\n2. 合理密植：控制合理的种植密度...\n3. 适量施肥：避免过量施用氮肥...",
    "notice": "注意事项：实施农业防治时应结合当地实际情况...",
    "images": [
      "/uploads/control/rice_blast_resistant.jpg",
      "/uploads/control/rice_proper_density.jpg"
    ],
    "isFavorite": false
  }
}
```

## 预警相关接口

### 1. 获取预警列表

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/alert/list?page=1&size=10`
- **描述**：获取病虫害预警信息列表

**请求设置：**
- **参数**：
  - region: 北京市 (可选，按地区筛选)
  - level: 3 (可选，按预警级别筛选，1-4级)
  - keyword: 稻瘟病 (可选，搜索关键词)
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/alert/list`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取预警列表成功",
  "data": {
    "total": 18,
    "list": [
      {
        "alertId": 56,
        "title": "水稻稻瘟病高发预警",
        "pestId": 42,
        "pestName": "水稻稻瘟病",
        "alertLevel": 3,
        "region": "湖南省长沙市",
        "startTime": "2023-06-15 00:00:00",
        "endTime": "2023-07-15 00:00:00",
        "shortContent": "近期湖南省长沙市气温升高，降雨频繁，预计水稻稻瘟病将大面积爆发...",
        "createTime": "2023-06-10 09:30:45"
      },
      // 更多预警...
    ],
    "page": 1,
    "size": 10
  }
}
```

### 2. 获取预警详情

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/alert/detail/56?userId={{userId}}`
- **描述**：获取特定预警的详细信息

**请求设置：**
- **Path参数**：
  - alertId: 56 (预警ID)
- **Query参数**：
  - userId: {{userId}} (可选，用于记录浏览历史)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/alert/detail/56`
3. 添加查询参数 userId
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取预警详情成功",
  "data": {
    "alertId": 56,
    "title": "水稻稻瘟病高发预警",
    "pestId": 42,
    "pestName": "水稻稻瘟病",
    "alertLevel": 3,
    "region": "湖南省长沙市",
    "startTime": "2023-06-15 00:00:00",
    "endTime": "2023-07-15 00:00:00",
    "alertContent": "近期湖南省长沙市气温升高，降雨频繁，空气湿度较大，为水稻稻瘟病的发生和蔓延创造了有利条件。预计在6月中旬至7月中旬，该地区水稻稻瘟病将呈现高发态势，可能对水稻产量造成严重影响。\n\n建议农户采取以下预防措施：\n1. 加强田间管理，保持通风透光\n2. 科学施肥，避免过量施用氮肥\n3. 适时喷施保护性杀菌剂\n4. 发现病株及时处理，减少传染源",
    "creatorId": 1,
    "creatorName": "系统管理员",
    "createTime": "2023-06-10 09:30:45",
    "pest": {
      "pestId": 42,
      "chineseName": "水稻稻瘟病",
      "imageUrl": "/uploads/pests/rice_blast.jpg",
      "shortDesc": "水稻上最常见的真菌性病害之一"
    },
    "isFavorite": false
  }
}
```

### 3. 获取最新预警

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/alert/latest?limit=5`
- **描述**：获取最新的预警信息

**请求设置：**
- **参数**：
  - limit: 5 (获取条数，默认5条)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/alert/latest`
3. 添加查询参数 limit
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取最新预警成功",
  "data": [
    {
      "alertId": 58,
      "title": "玉米螟虫害预警提醒",
      "pestId": 63,
      "pestName": "玉米螟",
      "alertLevel": 2,
      "region": "吉林省长春市",
      "startTime": "2023-07-01 00:00:00",
      "endTime": "2023-07-30 00:00:00",
      "shortContent": "近期吉林省长春市气温升高，预计玉米螟将进入繁殖期...",
      "createTime": "2023-06-25 14:20:35"
    },
    // 更多预警...
  ]
}
```

## 农技资讯接口

### 1. 获取农技资讯列表

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/news/list?page=1&size=10`
- **描述**：获取农技资讯文章列表

**请求设置：**
- **参数**：
  - keyword: 水稻 (可选，搜索关键词)
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/news/list`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取农技资讯列表成功",
  "data": {
    "total": 35,
    "list": [
      {
        "newsId": 12,
        "title": "水稻绿色高产栽培技术要点",
        "coverImage": "/uploads/news/rice_cultivation.jpg",
        "summary": "本文介绍了水稻绿色高产栽培的关键技术要点...",
        "author": "张农技",
        "source": "农业技术推广中心",
        "views": 1280,
        "isTop": 1,
        "createTime": "2023-05-12 10:15:30"
      },
      // 更多资讯...
    ],
    "page": 1,
    "size": 10
  }
}
```

### 2. 获取农技资讯详情

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/news/detail/12?userId={{userId}}`
- **描述**：获取特定农技资讯的详细内容

**请求设置：**
- **Path参数**：
  - newsId: 12 (资讯ID)
- **Query参数**：
  - userId: {{userId}} (可选，用于记录浏览历史)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/news/detail/12`
3. 添加查询参数 userId
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取农技资讯详情成功",
  "data": {
    "newsId": 12,
    "title": "水稻绿色高产栽培技术要点",
    "coverImage": "/uploads/news/rice_cultivation.jpg",
    "content": "<p>水稻是我国主要粮食作物之一，科学的栽培技术对提高水稻产量和质量至关重要。本文介绍水稻绿色高产栽培的关键技术要点。</p><h2>一、选择优良品种</h2><p>根据当地气候条件选择适宜的优质高产品种...</p><h2>二、科学育秧</h2><p>1. 适时播种：根据当地气候条件，合理安排播种时间...</p><p>2. 培育壮秧：使用营养钵育秧法或旱育稀植法...</p><h2>三、合理密植</h2><p>根据品种特性和土壤肥力状况，确定合理的种植密度...</p>",
    "author": "张农技",
    "source": "农业技术推广中心",
    "views": 1281,
    "isTop": 1,
    "createTime": "2023-05-12 10:15:30",
    "related": [
      {
        "newsId": 15,
        "title": "水稻病虫害综合防治技术",
        "coverImage": "/uploads/news/rice_pest_control.jpg"
      },
      {
        "newsId": 18,
        "title": "水稻机械化收获技术指南",
        "coverImage": "/uploads/news/rice_harvest.jpg"
      }
    ]
  }
}
```

## 社区交流接口

### 1. 获取帖子列表

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/forum/list?page=1&size=10`
- **描述**：获取社区交流帖子列表

**请求设置：**
- **参数**：
  - tab: recommend (可选，选项卡类型：recommend/latest/hot/question)
  - keyword: 水稻 (可选，搜索关键词)
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/forum/list`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取帖子列表成功",
  "data": {
    "total": 42,
    "list": [
      {
        "postId": 123,
        "userId": 10001,
        "nickname": "种田达人",
        "avatarUrl": "/uploads/avatars/user10001.jpg",
        "title": "水稻种植过程中有黄叶现象，求助！",
        "content": "我家水稻刚刚返青，但发现有不少叶片发黄...",
        "images": ["/uploads/forum/rice_yellow_leaves1.jpg", "/uploads/forum/rice_yellow_leaves2.jpg"],
        "tags": "水稻,病害,请教",
        "postType": 1,
        "isTop": 0,
        "isEssence": 0,
        "viewCount": 56,
        "likeCount": 12,
        "commentCount": 8,
        "createTime": "2023-05-20 15:30:42"
      },
      // 更多帖子...
    ],
    "page": 1,
    "size": 10
  }
}
```

### 2. 获取帖子详情

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/forum/detail/123?userId={{userId}}`
- **描述**：获取特定帖子的详细内容和评论

**请求设置：**
- **Path参数**：
  - postId: 123 (帖子ID)
- **Query参数**：
  - userId: {{userId}} (可选，用于记录浏览历史)

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/forum/detail/123`
3. 添加查询参数 userId
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取帖子详情成功",
  "data": {
    "postId": 123,
    "userId": 10001,
    "nickname": "种田达人",
    "avatarUrl": "/uploads/avatars/user10001.jpg",
    "title": "水稻种植过程中有黄叶现象，求助！",
    "content": "我家水稻刚刚返青，但发现有不少叶片发黄，主要是从叶尖开始向整个叶片蔓延，不知道是什么问题？是缺素症状还是病害？急需各位专家帮忙看看，该如何处理！",
    "images": ["/uploads/forum/rice_yellow_leaves1.jpg", "/uploads/forum/rice_yellow_leaves2.jpg"],
    "tags": "水稻,病害,请教",
    "postType": 1,
    "isTop": 0,
    "isEssence": 0,
    "viewCount": 57,
    "likeCount": 12,
    "commentCount": 8,
    "createTime": "2023-05-20 15:30:42",
    "comments": [
      {
        "commentId": 456,
        "userId": 10020,
        "nickname": "农技小王",
        "avatarUrl": "/uploads/avatars/user10020.jpg",
        "content": "从图片看，可能是缺铁导致的黄化，建议喷施硫酸亚铁溶液",
        "createTime": "2023-05-20 16:05:22",
        "likeCount": 5,
        "replies": [
          {
            "commentId": 457,
            "userId": 10001,
            "nickname": "种田达人",
            "avatarUrl": "/uploads/avatars/user10001.jpg",
            "content": "谢谢指导，我明天就试试",
            "createTime": "2023-05-20 16:10:45",
            "likeCount": 1,
            "parentId": 456
          }
        ]
      },
      // 更多评论...
    ],
    "expertAnswers": [
      {
        "answerId": 78,
        "userId": 10050,
        "nickname": "张教授",
        "avatarUrl": "/uploads/avatars/expert10050.jpg",
        "content": "根据图片显示的症状，这很可能是缺铁性黄化症。水稻缺铁时，首先从嫩叶开始发黄，且呈条纹状黄化。除了前面提到的硫酸亚铁喷施外，建议同时检查土壤pH值，若pH值过高会影响铁元素的吸收。可以适当施用硫酸亚铁或腐殖酸铁5-10公斤/亩，与基肥或追肥混合施用。",
        "images": ["/uploads/forum/expert_answer78.jpg"],
        "createTime": "2023-05-21 09:30:25",
        "likeCount": 15
      }
    ]
  }
}
```

### 3. 发布帖子

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/forum/publish`
- **描述**：发布新帖子

**请求设置：**
- **Headers**：无特殊要求
- **Body**：选择 `form-data`
  - Key: `userId`，值为 `{{userId}}`
  - Key: `title`，值为帖子标题
  - Key: `content`，值为帖子内容
  - Key: `tags`，值为标签（逗号分隔）
  - Key: `postType`，值为帖子类型（0普通/1问答）
  - Key: `images[]`，类型选择 `File`（可添加多个图片文件）

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/forum/publish`
3. 在 Body 选项卡中选择 `form-data`
4. 添加上述键值对，其中 `images[]` 可以选择一个或多个本地图片文件
5. 点击"发送"按钮

**示例数据：**
- userId: {{userId}}
- title: 玉米苗期管理问题求助
- content: 最近种的玉米刚出苗，想了解一下苗期应该如何管理？有什么需要特别注意的问题吗？
- tags: 玉米,种植技术,求助
- postType: 1
- images[]: (选择一张本地图片文件)

**预期结果：**
```json
{
  "code": 200,
  "message": "发布成功",
  "data": {
    "postId": 125
  }
}
```

### 4. 获取用户发布的帖子

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/forum/user/{{userId}}?page=1&size=10`
- **描述**：获取指定用户发布的帖子列表

**请求设置：**
- **Path参数**：
  - userId: {{userId}} (用户ID)
- **Query参数**：
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/forum/user/{{userId}}`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取用户帖子成功",
  "data": {
    "total": 5,
    "list": [
      {
        "postId": 125,
        "userId": 12345,
        "nickname": "测试用户",
        "avatarUrl": "https://example.com/avatar.jpg",
        "title": "玉米苗期管理问题求助",
        "content": "最近种的玉米刚出苗，想了解一下苗期应该如何管理？...",
        "images": ["/uploads/forum/corn_seedling.jpg"],
        "tags": "玉米,种植技术,求助",
        "postType": 1,
        "viewCount": 12,
        "likeCount": 3,
        "commentCount": 2,
        "createTime": "2023-06-01 09:45:30"
      },
      // 更多帖子...
    ],
    "page": 1,
    "size": 10
  }
}
```

## 管理员接口

### 1. 获取用户列表（管理员）

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/admin/users?userId={{userId}}&page=1&size=10`
- **描述**：获取系统用户列表（仅管理员可用）

**请求设置：**
- **参数**：
  - userId: {{userId}} (需为管理员账号ID)
  - keyword: 张 (可选，搜索关键词)
  - userType: 0 (可选，用户类型筛选：0普通用户/1专家/2管理员)
  - status: 1 (可选，状态筛选：0禁用/1正常)
  - page: 1
  - size: 10

**测试步骤：**
1. 创建新的 GET 请求
2. 输入 URL: `{{baseUrl}}/api/admin/users`
3. 添加查询参数
4. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "获取用户列表成功",
  "data": {
    "total": 156,
    "list": [
      {
        "userId": 12345,
        "openid": "oax5P5Ojt6tiVrB2hKnrYjt9L4Xs",
        "nickname": "张三",
        "avatarUrl": "https://example.com/avatar.jpg",
        "phone": "13800138000",
        "email": "zhangsan@example.com",
        "userType": 0,
        "status": 1,
        "createTime": "2023-05-10 15:30:20",
        "lastLoginTime": "2023-06-01 09:20:15"
      },
      // 更多用户...
    ],
    "page": 1,
    "size": 10
  }
}
```

### 2. 发布预警信息（管理员）

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/admin/alert/publish`
- **描述**：发布或编辑病虫害预警信息（仅管理员可用）

**请求设置：**
- **Headers**：
  - Content-Type: application/json
- **Body**：选择 `raw` 并设置为 JSON 格式
```json
{
  "userId": {{userId}},
  "title": "小麦赤霉病预警通知",
  "pestId": 25,
  "alertLevel": 3,
  "alertContent": "近期我市降雨频繁，温度适宜，小麦进入抽穗扬花期，为赤霉病流行创造了有利条件。建议农户密切关注天气变化，加强田间巡视，及时喷施药剂进行预防。",
  "region": "河南省郑州市",
  "startTime": "2023-05-01 00:00:00",
  "endTime": "2023-05-31 00:00:00"
}
```

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/admin/alert/publish`
3. 添加 Content-Type 请求头
4. 在 Body 选项卡中选择 `raw` 并选择 JSON 格式
5. 输入上述 JSON 数据
6. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "发布预警成功",
  "data": {
    "alertId": 60
  }
}
```

### 3. 发布农技资讯（管理员）

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/admin/news/publish`
- **描述**：发布或编辑农技资讯文章（仅管理员可用）

**请求设置：**
- **Headers**：无特殊要求
- **Body**：选择 `form-data`
  - Key: `userId`，值为 `{{userId}}`
  - Key: `title`，值为文章标题
  - Key: `content`，值为文章内容（支持HTML）
  - Key: `author`，值为作者名称
  - Key: `source`，值为来源
  - Key: `isTop`，值为是否置顶（0/1）
  - Key: `coverImage`，类型选择 `File`（上传封面图片）

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/admin/news/publish`
3. 在 Body 选项卡中选择 `form-data`
4. 添加上述键值对
5. 点击"发送"按钮

**示例数据：**
- userId: {{userId}}
- title: 夏季蔬菜病虫害防治技术指南
- content: <h2>一、预防为主</h2><p>夏季高温高湿，蔬菜病虫害多发。预防措施包括...</p>...
- author: 李农技
- source: 市农业技术推广站
- isTop: 1
- coverImage: (选择一张本地图片文件)

**预期结果：**
```json
{
  "code": 200,
  "message": "发布成功",
  "data": {
    "newsId": 20
  }
}
```

### 4. 删除预警信息（管理员）

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/admin/alert/delete`
- **描述**：删除预警信息（仅管理员可用）

**请求设置：**
- **Headers**：
  - Content-Type: application/json
- **Body**：选择 `raw` 并设置为 JSON 格式
```json
{
  "userId": {{userId}},
  "alertId": 60
}
```

**测试步骤：**
1. 创建新的 POST 请求
2. 输入 URL: `{{baseUrl}}/api/admin/alert/delete`
3. 添加 Content-Type 请求头
4. 在 Body 选项卡中选择 `raw` 并选择 JSON 格式
5. 输入上述 JSON 数据
6. 点击"发送"按钮

**预期结果：**
```json
{
  "code": 200,
  "message": "删除预警成功"
}
```

## 错误测试

### 1. 无效的登录参数

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/user/login`
- **描述**：测试缺少必要参数时的登录接口响应

**请求设置：**
- **Headers**：
  - Content-Type: application/json
- **Body**：选择 `raw` 并设置为 JSON 格式
```json
{
  "nickname": "测试用户"
}
```

**预期结果：**
```json
{
  "code": 400,
  "message": "缺少必要参数"
}
```

### 2. 图片格式不正确

**请求信息：**
- **方法**：POST
- **URL**：`{{baseUrl}}/api/pest/detect`
- **描述**：测试上传错误格式文件时的检测接口响应

**请求设置：**
- **Body**：选择 `form-data`
  - Key: `file`，类型选择 `File`
  - Value: 选择一个文本文件（如 .txt 格式）
  - Key: `userId`，值为 `{{userId}}`

**预期结果：**
```json
{
  "code": 400,
  "message": "图片格式不支持，请上传jpg、jpeg或png格式的图片"
}
```

### 3. 非管理员访问管理接口

**请求信息：**
- **方法**：GET
- **URL**：`{{baseUrl}}/api/admin/users?userId=10001`
- **描述**：测试非管理员用户访问管理接口的响应（使用普通用户ID）

**预期结果：**
```json
{
  "code": 403,
  "message": "没有管理员权限"
}
```

## 测试自动化

Postman支持创建测试脚本和自动化运行测试。以下是几个示例测试脚本，可以添加到请求的Tests选项卡中：

### 1. 登录接口测试脚本

```javascript
// 检查状态码
pm.test("状态码为 200", function () {
    pm.response.to.have.status(200);
});

// 验证返回数据结构
pm.test("响应包含预期字段", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('code');
    pm.expect(jsonData).to.have.property('message');
    pm.expect(jsonData.data).to.have.property('userId');
});

// 验证业务逻辑
pm.test("登录成功", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.code).to.eql(200);
    pm.expect(jsonData.message).to.eql("登录成功");
    
    // 保存用户ID到环境变量
    if (jsonData.data && jsonData.data.userId) {
        pm.environment.set('userId', jsonData.data.userId);
        console.log("用户ID已保存：" + jsonData.data.userId);
    }
});
```

### 2. 病虫害检测接口测试脚本

```javascript
// 检查状态码
pm.test("状态码为 200", function () {
    pm.response.to.have.status(200);
});

// 验证返回数据结构
pm.test("响应包含检测结果", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData.code).to.eql(200);
    pm.expect(jsonData.data).to.have.property('result');
    pm.expect(jsonData.data.result).to.have.property('name');
    pm.expect(jsonData.data.result).to.have.property('confidence');
});

// 保存recordId供后续测试使用
pm.test("保存检测记录ID", function () {
    var jsonData = pm.response.json();
    if (jsonData.data && jsonData.data.recordId) {
        pm.environment.set('lastRecordId', jsonData.data.recordId);
    }
});
```

### 3. 创建集合运行器

测试完所有接口后，可以创建一个集合运行器，按特定顺序自动化运行所有测试：

1. 点击集合右侧的"..."按钮，选择"Run collection"
2. 在打开的窗口中，选择要运行的请求和顺序
3. 配置环境变量和其他运行参数
4. 点击"Run 农作物病虫害检测系统API测试"按钮开始测试
5. 查看测试结果报告，了解接口的健康状况

## 总结

本文档提供了对农作物病虫害检测预警系统后端接口的全面测试方案。通过使用Postman工具，可以有效地测试系统的各个功能模块，确保系统的稳定性和可靠性。

测试内容覆盖了以下几个方面：
- 用户管理：登录、收藏、浏览历史等
- 病虫害检测：图像识别、检测记录等
- 病虫害信息：病虫害列表、详情、防治措施等
- 预警管理：预警列表、详情、最新预警等
- 农技资讯：资讯列表、详情等
- 社区交流：帖子列表、详情、发帖等
- 管理员功能：用户管理、内容发布等
- 错误处理：参数验证、权限控制等

定期运行这些测试，可以及时发现系统的潜在问题，确保系统的正常运行。通过集成到CI/CD流程中，可以实现自动化测试和质量保证。 