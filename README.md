# tree-demo #
### 一个Python 实现对树操作的demo（一公司笔试题的实现）###


```
请用python实现一个接受命令行输入数据，存储并按要求返回结果的服务。请用最基本的库来完成，尽量不要使用第三方的库。

功能：
服务将维护内存中的一个树状结构的数据。
支持添加和删除节点，移动节点到一个新的位置，搜索。
每个节点有一个名称，一个ID，一个父节点ID。（都为字符串）
节点的ID全局唯一，节点的名称必须在其同层次的node中唯一。

输入输出：
该服务输入输出使用JSON。程序从标准输入接受请求消息，将结果返回给标准输出。
为了简化解析，
每次输入为一行，输出不一定为一行（根据要求，Json结构自己定义）
两次请求的中间不会收到其他请求（同步）
收到的json假定已经进行过验证，为合法的json结构。
当接收到EOF时，必须在标准输出打印退出的提示信息后再退出

接口：
################################
所有接口返回的结果示例:
Success response: {"re":true}
Failure response: {"re":false}
################################
Add Node：
功能: 添加一个新的Node

参数:
   - name      {string}: Node name
   - id        {string}: Node ID
   - parent_id {string}: 父节点ID; 如果为空即为root节点

验证:
   - 同级节点不可同名
   - ID 全局唯一
   - 只能有一个root 节点
   - 节点名称和ID必须指定
   - 如果有父节点ID，次节点必须存在

Example:  Add the root node

Request:  {"add_node":{"id":"1","name":"Root"}}
Response: {"re":true}

Example:  Add a child node

Request:  {"add_node":{"id":"4","name":"Child2","parent_id":"1"}}
Response: {"re":true}

Example:  Add a child node to nonexistent parent.

Request:  {"add_node":{"id":"4","name":"Child3","parent_id":"200"}}
Response: {"re":false}
################################
Delete Node

功能: 根据ID删除节点.

参数:
   - id {string}: 删除节点的ID 

验证:
   - ID必须指定.
   - Node必须存在.
   - Node不能有子节点.

Example:  Add root node and then delete it.

Request:  {"add_node":{"id":"1","name":"Root"}}
Response: {"re":true}
Request:  {"delete_node":{"id":"1"}}
Response: {"re":true}

Example:  Delete nonexistent node

Request:  {"delete_node":{"id":"1"}}
Response: {"re":false}
################################
Move Node

功能: 移动一个节点

参数:
   - id {string}:            ID of node 
   - new_parent_id {string}: ID of the new parent node

验证:
   - ID 和 parent_id必须指定.
   - 节点必须存在.
   - 被移动节点的名称不能够在移动对象的同层次中相同.
   - 移动不能够破坏存储的树状结构

Example:  

Request:  {"add_node":{"id":"1","name":"Root"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"1","id":"2","name":"A"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"1","id":"3","name":"B"}}
Response: {"re":true}
Request:  {"move_node":{"id":"2","new_parent_id":"3"}}
Response: {"re":true}

Example:  结构被破坏

Request:  {"add_node":{"id":"1","name":"Root"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"1","id":"2","name":"A"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"2","id":"3","name":"B"}}
Response: {"re":true}
Request:  {"move_node":{"id":"2","new_parent_id":"3"}}
Response: {"re":false}

################################
Query

功能: 返回满足条件的list

Params:
  - min_depth {integer}:     最小的深度. Default: none.
  - max_depth {integer}:     最大的深度. Default: none.
  - names {list of strings}: 如果指定，只返回名字匹配的节点
  - ids {list of ids}:       如果指定，只返回ID匹配的节点
  - root_ids {list of ids}:  从此ID开始搜索，如果ID不存在，忽略此请求.

所有参数都是可选. 如果参数都没指定，返回所有节点. 如果都不匹配，返回空。
查找不会返回false。

Example:  

Request:  {"add_node":{"id":"1","name":"Root"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"1","id":"2","name":"A"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"2","id":"3","name":"B"}}
Response: {"re":true}
Request:  {"query":{"max_depth":1}}
Response (json):
    {
       "nodes": [
          {
             "id": "1",
             "name": "Root",
             "parent_id": ""
          },
          {
             "name": "A",
             "id": "2",
             "parent_id": "1"
          }
       ]
    }


Example:  

Request:  {"add_node":{"id":"1","name":"Root"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"1","id":"2","name":"A"}}
Response: {"re":true}
Request:  {"add_node":{"parent_id":"2","id":"3","name":"B"}}
Response: {"re":true}
Request:  {"query":{"names":["B"]}}
Response :
    {
       "nodes": [
          {
             "id": "3",
             "parent_id": "2",
             "name": "B"
          }
       ]
    }

```


