#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

OK_MSG = json.dumps({"re": True})
ERROR_MSG = "Response:" + json.dumps({"re": False})


class Node(object):
    def __init__(self, id=None, name=None, parent_id=None):
        self.id = id
        self.name = name
        self.parent_id = parent_id
        self.children_ids = []
        self.children_names = []

    def is_root(self):
        if self.parent_id:
            return False
        else:
            return True

    def get_parent_id(self):
        return self.parent_id

    def update_parent_id(self, pid):
        self.parent_id = pid

    @property
    def get_node_id(self):
        return self.id

    @property
    def get_node_name(self):
        return self.name

    def get_children_ids(self):
        return self.children_ids

    def get_children_names(self):
        return self.children_names

    def has_children(self):
        if len(self.children_ids) == 0:
            return False
        return True

    def add_children(self, cid, cname):
        if cname in self.children_names:
            # TODO 同级节点不可同名
            return False
        self.children_ids.append(cid)
        self.children_names.append(cname)
        return True

    def delete_children(self, cid, cname):
        if cid in self.children_ids:
            self.children_ids.remove(cid)
            self.children_names.remove(cname)


class NodeHandler(object):
    def __init__(self):
        # {"id":Node_object}
        self._nodes = {}
        self.root = None

    def check_node_by_add(self, node):
        """添加新节点是监测是否满足要求"""
        if not node.id:
            # ID 必须存在
            return False
        if not node.name:
            # 用户名必须存在
            return False
        if node.id in self._nodes:
            # ID 唯一
            return False
        return True

    def add_root(self, node):
        """添加root节点"""
        if self.root:
            return False
        self.root = node.id
        self._nodes.update({node.id: node})
        return True

    def add_node(self, node):
        """添加子节点"""
        if not self.check_node_by_add(node):
            return False
        if not node.parent_id:
            # 添加root 节点
            is_ok = self.add_root(node)
            if is_ok:
                return True
            return False
        else:
            # 添加子节点
            if node.parent_id not in self._nodes:
                # 父节点不存在
                return False
            # 父节点添加子节点 会判断同名的
            is_ok = self._nodes[node.parent_id].add_children(node.id, node.name)
            if not is_ok:
                return False
            self._nodes.update({node.id: node})
            return True

    def delete(self, nid):
        """删除节点"""
        if nid not in self._nodes:
            # 节点不存在
            return False
        if self._nodes[nid].has_children():
            # 不能有子节点
            return False
        if self.root != nid:
            # nid 节点不是root 删除他父节点下他的信息
            pid = self._nodes[nid].get_parent_id()
            self._nodes[pid].delete_children(nid, self._nodes[nid].get_node_name)
        del self._nodes[nid]
        return True

    def _get_children_ids(self, pid):
        """获取直接关联的子节点ID"""
        return self._nodes[pid].get_children_ids()


    def move(self, nid, parent_id):
        """移动节点"""
        if nid not in self._nodes:
            return False
        if parent_id not in self._nodes:
            return False
        # 被移动节点的名称不能够在移动对象的同层次中相同
        nname = self._nodes[nid].get_node_name
        if nname in self._nodes[parent_id].get_children_names():
            return False
        # 移动不能够破坏存储的树状结构=》父子颠倒
        if nid in self.get_parents(parent_id):
            return False
        # if nid in self._nodes[parent_id].get_children_ids():
        #     return False

        # 更改父节点
        self._nodes[nid].update_parent_id(parent_id)
        return True

    def get_parents(self, nid):
        '''获取直系父辈之上关系'''
        pids = []

        def inner(id):
            if id:
                pids.append(id)
                inner(self._nodes[id].get_parent_id())

        inner(nid)
        return pids

    def query(self, nid):
        """查询节点信息"""
        return self._query(nid)

    def _query_filter(self, max_depth=None, min_depth=None, names=None, ids=None, root_ids=None):
        pass

    def _query(self, nid):
        """
        {'name':"xx", "id":"yy", "parent_id":"jj", "childres":[{}]}
        """
        nname = self._nodes[nid].get_node_name
        nparent_id = self._nodes[nid].get_parent_id()
        t = {"name": nname, "parent_id": nparent_id, nid: {"childres": []}}
        cids = self._nodes[nid].get_children_ids()
        for j in cids:
            t[nid]["childres"].append(self._query(j))
        return t

    def query_info(self, nid):
        """
        [(id, name, parent_id, depth)], bool
        """
        depth = 0
        info = []
        if nid not in self._nodes:
            return [], False

        def inner(_id, _depth):
            nname = self._nodes[_id].get_node_name
            cids = self._nodes[_id].get_children_ids()
            nparent_id = self._nodes[_id].get_parent_id()
            info.append((_id, nname, nparent_id, _depth))
            for i, v in enumerate(cids):
                if i == 0:
                    _depth += 1
                inner(v, _depth)

        inner(nid, depth)
        return info, True



def check_params(param, c_id=False, c_name=False, c_parent_id=False, c_new_parent_id=False):
    """"""
    id = param.get("id", "")
    name = param.get("name", "")
    parent_id = param.get("parent_id", "")
    c_new_parent_id = param.get("c_new_parent_id", "")
    if c_id:
        if not isinstance(id, unicode) and len(id) < 1:
            return False
    if c_name:
        if not isinstance(name, unicode) and len(name) < 1:
            return False
    if c_parent_id:
        if not isinstance(parent_id, unicode) and len(parent_id) < 1:
            return False
    if c_new_parent_id:
        if not isinstance(new_parent_id, unicode) and len(new_parent_id) < 1:
            return False
    return True


def show_tree(data):
    """[id, name, parent, depth]"""
    tree_dict = []
    ids = []
    for i in data:
        d = dict()
        if i[0] in ids:
            continue
        ids.append(i[0])
        d["id"] = i[0]
        d["name"] = i[1]
        d["parent_id"] = i[2]
        tree_dict.append(d)
    return {"nodes": tree_dict}


if __name__ == "__main__":

    print "输入 Ctrl + D 退出"
    nhandler = NodeHandler()
    while 1:
        try:
            enter = raw_input('Request:  ')
            handler = json.loads(enter)
            # 增加节点
            if "add_node" in handler:
                """
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

                """
                # 参数判断
                is_ok = check_params(handler["add_node"], c_id=True, c_name=True)
                if not is_ok:
                    print ERROR_MSG
                    continue
                if "parent_id" not in handler["add_node"]:
                    handler["add_node"]["parent_id"] = ""
                else:
                    if not isinstance(handler["add_node"]["parent_id"], unicode):
                        print ERROR_MSG
                        continue
                node = Node(**handler["add_node"])
                if not node.parent_id:
                    if nhandler.add_root(node):
                        print OK_MSG
                    else:
                        print ERROR_MSG
                else:
                    if nhandler.add_node(node):
                        print OK_MSG
                    else:
                        print ERROR_MSG
                # print nhandler.query()
                # print "info =====", nhandler.query_info("1")

            # 节点删除
            elif "delete_node" in handler:
                """
                功能: 根据ID删除节点.

                参数:
                   - id {string}: 删除节点的ID

                验证:
                   - ID必须指定.
                   - Node必须存在.
                   - Node不能有子节点.
                """
                # 参数判断
                is_ok = check_params(handler["delete_node"], c_id=True)
                if not is_ok:
                    print ERROR_MSG
                    continue
                nid = handler["delete_node"]["id"]
                if nhandler.delete(nid):
                    print OK_MSG
                else:
                    print ERROR_MSG
                # print nhandler.query()

            # 节点移动
            elif "move_node" in handler:
                """
                功能:  移动一个节点.

                参数:
                   - id {string}:            ID of node
                   - new_parent_id {string}: ID of the new parent node

                验证:
                   - ID 和 parent_id必须指定.
                   - 节点必须存在.
                   - 被移动节点的名称不能够在移动对象的同层次中相同.
                   - 移动不能够破坏存储的树状结构

                """
                is_ok = check_params(handler["move_node"], c_id=True, c_new_parent_id=True)
                if not is_ok:
                    print ERROR_MSG
                    continue
                nid = handler["move_node"]['id']
                new_parent_id = handler["move_node"]['new_parent_id']
                if nhandler.move(nid, new_parent_id):
                    print OK_MSG
                else:
                    print ERROR_MSG
                # print nhandler.query()
            # 节点查询
            elif "query" in handler:
                """
                  - min_depth {integer}:     最小的深度. Default: none.
                  - max_depth {integer}:     最大的深度. Default: none.
                  - names {list of strings}: 如果指定，只返回名字匹配的节点
                  - ids {list of ids}:       如果指定，只返回ID匹配的节点
                  - root_ids {list of ids}:  从此ID开始搜索，如果ID不存在，忽略此请求.

                所有参数都是可选. 如果参数都没指定，返回所有节点. 如果都不匹配，返回空。
                查找不会返回false。

                """
                # {"query":{"max_depth":1,"max_depth":2, "names":[],"ids":[],"root_ids":[]}}
                if not handler["query"]:
                    nodes, _ = nhandler.query_info(nhandler.root)
                    tree_dict = show_tree(nodes)
                    print tree_dict
                elif "root_ids" in handler["query"]:
                    nodes = []
                    for i in handler["query"]["root_ids"]:
                        _info, is_ok = nhandler.query_info(i)
                        if is_ok:
                            continue
                        else:
                            nodes.extend(_info)
                    if "names" in handler["query"]:
                        names = handler["query"]["names"]
                        nodes = filter(lambda x: x[1] in names, nodes)
                    if "ids" in handler["query"]:
                        ids = handler["query"]["ids"]
                        nodes = filter(lambda x: x[0] in ids, nodes)
                    if "min_depth" in handler["query"]:
                        min_depth = handler["query"]["min_depth"]
                        nodes = filter(lambda x: x[3] >= min_depth, nodes)
                    if "max_depth" in handler["query"]:
                        min_depth = handler["query"]["max_depth"]
                        nodes = filter(lambda x: x[3] <= min_depth, nodes)
                    tree_dict = show_tree(nodes)
                    print tree_dict
                elif "ids" in handler["query"]:
                    nodes, _ = nhandler.query_info(nhandler.root)
                    ids = handler["query"]["ids"]
                    nodes = filter(lambda x: x[0] in ids, nodes)
                    if "names" in handler["query"]:
                        names = handler["query"]["names"]
                        nodes = filter(lambda x: x[1] in names, nodes)
                    if "min_depth" in handler["query"]:
                        min_depth = handler["query"]["min_depth"]
                        nodes = filter(lambda x: x[3] >= min_depth, nodes)
                    if "max_depth" in handler["query"]:
                        min_depth = handler["query"]["max_depth"]
                        nodes = filter(lambda x: x[3] <= min_depth, nodes)
                    tree_dict = show_tree(nodes)
                    print tree_dict
                elif "names" in handler["query"]:
                    nodes, _ = nhandler.query_info(nhandler.root)
                    names = handler["query"]["names"]
                    nodes = filter(lambda x: x[1] in names, nodes)
                    if "min_depth" in handler["query"]:
                        min_depth = handler["query"]["min_depth"]
                        nodes = filter(lambda x: x[3] >= min_depth, nodes)
                    if "max_depth" in handler["query"]:
                        min_depth = handler["query"]["max_depth"]
                        nodes = filter(lambda x: x[3] <= min_depth, nodes)
                    tree_dict = show_tree(nodes)
                    print tree_dict
                elif "min_depth" in handler["query"]:
                    nodes, _ = nhandler.query_info(nhandler.root)
                    min_depth = handler["query"]["min_depth"]
                    nodes = filter(lambda x: x[3] >= min_depth, nodes)
                    if "max_depth" in handler["query"]:
                        min_depth = handler["query"]["max_depth"]
                        nodes = filter(lambda x: x[3] <= min_depth, nodes)
                    tree_dict = show_tree(nodes)
                    print tree_dict
                elif "max_depth" in handler["query"]:
                    nodes, _ = nhandler.query_info(nhandler.root)
                    min_depth = handler["query"]["max_depth"]
                    nodes = filter(lambda x: x[3] <= min_depth, nodes)
                    tree_dict = show_tree(nodes)
                    print tree_dict
                else:
                    tree_dict = show_tree([])
                    print tree_dict
                # print nhandler.query()
            else:
                print ERROR_MSG
        except EOFError:
            print "收到退出请求， 退出中。。。。。。。。"
            break
        except:
            continue
