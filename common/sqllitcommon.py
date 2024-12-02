#-*- coding:utf-8 -*-

import sqlite3


class SQLiteDB:
    def __init__(self, db_name,log):
        """初始化数据库连接"""
        self.conn = None
        self.cursor = None
        self.log = log
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            self.log.error('连接数据库时出错')

    def execute(self, sql, params=None):
        """执行SQL查询
        参数:
            sql: SQL语句
            params: SQL参数，用于参数化查询
        返回:
            执行成功返回True，失败返回False
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            self.log.error('执行查询时出错')
            return False

    # 创建表
    def create_table(self, table_name, fields):
        """创建数据表
        参数:
            table_name: 表名
            fields: 字段定义列表，每个元素是一个元组 (字段名, 类型定义)
        返回:
            执行成功返回True，失败返回False
        """
        try:
            fields_str = ', '.join([f"{name} {definition}" for name, definition in fields])
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({fields_str})"
            return self.execute(sql)
        except sqlite3.Error as e:

            self.log.error('创建表时出错')
            return False

    # 插入##########################################
    def insert(self, table_name, fields, values):
        """插入数据
        参数:
            table_name: 表名
            fields: 字段名列表，例如 ['name', 'age']
            values: 值列表，例如 ('张三', 25)
        返回:
            执行成功返回True，失败返回False
        """
        try:
            # 构建SQL语句
            placeholders = ','.join(['?' for _ in fields])
            fields_str = ','.join(fields)
            sql = "INSERT INTO {table_name} ({fields_str}) VALUES({placeholders})".format(table_name=table_name,fields_str=fields_str,placeholders=placeholders)
            return self.execute(sql, values)
        except sqlite3.Error as e:
            self.log.error('创建表时出错')
            print(f"插入数据时出错: {e}")
            self.conn.rollback()  # 发生错误时回滚
            return False

    # 批量插入1
    def batch_insert(self, table_name, fields, values_list):
        """批量插入数据
        参数:
            table_name: 表名
            fields: 字段名列表，例如 ['name', 'age']
            values_list: 值列表，每个元素是一个元组，例如 [('张三', 25), ('李四', 30)]
        返回:
            执行成功返回True，失败返回False
        """
        try:
            # 构建SQL语句
            placeholders = ','.join(['?' for _ in fields])
            fields_str = ','.join(fields)
            sql = f"INSERT INTO {table_name} ({fields_str}) VALUES ({placeholders})"

            # 执行批量插入
            self.cursor.executemany(sql, values_list)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"批量插入数据时出错: {e}")
            self.log.error('创建表时出错')
            self.conn.rollback()  # 发生错误时回滚
            return False

    # 批量插入2
    def insert_many_dict(self, table_name, dict_list):
        """使用字典列表批量插入数据
        参数:
            table_name: 表名
            dict_list: 字典列表，每个字典代表一行数据，例如：
                     [{'name': '张三', 'age': 25}, {'name': '李四', 'age': 30}]
        返回:
            执行成功返回True，失败返回False
        """
        if not dict_list:
            return False
        try:
            # 从第一个字典获取字段名
            fields = list(dict_list[0].keys())
            # 转换字典列表为值列表
            values_list = [tuple(d.values()) for d in dict_list]
            return self.batch_insert(table_name, fields, values_list)
        except Exception as e:
            self.log.error('创建表时出错')
            print(f"处理字典数据时出错: {e}")
            return False

    ############################################################

    # 删除###########################################
    def delete(self, table_name, condition, params=None):
        """删除数据
        参数:
            table_name: 表名
            condition: WHERE条件语句，例如 "age > ?" 或 "name = ?"
            params: 条件参数，例如 (20,) 或 ('张三',)
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        try:
            sql = f"DELETE FROM {table_name} WHERE {condition}"
            self.cursor.execute(sql, params or ())
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            self.log.error('创建表时出错')
            print(f"删除数据时出错: {e}")
            self.conn.rollback()
            return -1

    def delete_by_id(self, table_name, id_value, id_field='id'):
        """根据ID删除数据
        参数:
            table_name: 表名
            id_value: ID值
            id_field: ID字段名，默认为'id'
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        return self.delete(table_name, f"{id_field} = ?", (id_value,))

    def delete_many(self, table_name, id_list, id_field='id'):
        """批量删除数据
        参数:
            table_name: 表名
            id_list: ID列表
            id_field: ID字段名，默认为'id'
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        try:
            placeholders = ','.join(['?' for _ in id_list])
            sql = f"DELETE FROM {table_name} WHERE {id_field} IN ({placeholders})"
            self.cursor.execute(sql, id_list)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"批量删除数据时出错: {e}")
            self.conn.rollback()
            return -1

    def truncate_table(self, table_name):
        """清空表数据
        参数:
            table_name: 表名
        返回:
            执行成功返回True，失败返回False
        """
        try:
            self.cursor.execute(f"DELETE FROM {table_name}")
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"清空表数据时出错: {e}")
            self.conn.rollback()
            return False

    ############################################################

    # 更新###########################################
    def update(self, table_name, fields, values, condition, condition_params=None):
        """更新数据
        参数:
            table_name: 表名
            fields: 要更新的字段列表，例如 ['name', 'age']
            values: 新的值列表，例如 ('张三', 25)
            condition: WHERE条件语句，例如 "id = ?"
            condition_params: 条件参数，例如 (1,)
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        try:
            # 构建SET子句
            set_clause = ','.join([f"{field} = ?" for field in fields])
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"

            # 合并values和condition_params
            params = list(values)
            if condition_params:
                params.extend(condition_params)

            self.cursor.execute(sql, params)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"更新数据时出错: {e}")
            self.conn.rollback()
            return -1

    def update_by_id(self, table_name, fields, values, id_value, id_field='id'):
        """根据ID更新数据
        参数:
            table_name: 表名
            fields: 要更新的字段列表，例如 ['name', 'age']
            values: 新的值列表，例如 ('张三', 25)
            id_value: ID值
            id_field: ID字段名，默认为'id'
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        return self.update(table_name, fields, values, f"{id_field} = ?", (id_value,))

    def update_dict(self, table_name, update_dict, condition, condition_params=None):
        """使用字典更新数据
        参数:
            table_name: 表名
            update_dict: 要更新的字段和值的字典，例如 {'name': '张三', 'age': 25}
            condition: WHERE条件语句，例如 "id = ?"
            condition_params: 条件参数，例如 (1,)
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        fields = list(update_dict.keys())
        values = list(update_dict.values())
        return self.update(table_name, fields, values, condition, condition_params)

    def batch_update_dict(self, table_name, dict_list, id_field='id'):
        """使用字典列表批量更新数据
        参数:
            table_name: 表名
            dict_list: 字典列表，每个字典必须包含id_field字段，例如：
                     [{'id': 1, 'name': '张三', 'age': 25},
                      {'id': 2, 'name': '李四', 'age': 30}]
            id_field: ID字段名，默认为'id'
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        if not dict_list:
            return 0
        try:
            # 从第一个字典获取所有字段名（排除ID字段）
            fields = [f for f in dict_list[0].keys() if f != id_field]

            # 转换字典列表为值列表
            values_list = []
            for d in dict_list:
                # 确保字典中包含ID字段
                if id_field not in d:
                    raise ValueError(f"字典中缺少 {id_field} 字段")
                # 构建值元组：先添加要更新的字段值，最后添加ID值
                values = tuple(d[f] for f in fields)
                values += (d[id_field],)
                values_list.append(values)

            return self.batch_update(table_name, fields, values_list, id_field)

        except Exception as e:
            print(f"批量更新字典数据时出错: {e}")
            return -1

    def batch_update(self, table_name, fields, values_list, id_field='id'):
        """批量更新数据
        参数:
            table_name: 表名
            fields: 要更新的字段列表，例如 ['name', 'age']
            values_list: 值列表，每个元素是一个元组，包含新值和ID，例如 [('张三', 25, 1), ('李四', 30, 2)]
            id_field: ID字段名，默认为'id'
        返回:
            执行成功返回受影响的行数，失败返回-1
        """
        try:
            # 构建SET子句
            set_clause = ','.join([f"{field} = ?" for field in fields])
            sql = f"UPDATE {table_name} SET {set_clause} WHERE {id_field} = ?"

            self.cursor.executemany(sql, values_list)
            self.conn.commit()
            return self.cursor.rowcount
        except sqlite3.Error as e:
            print(f"批量更新数据时出错: {e}")
            self.conn.rollback()
            return -1

    ############################################################
    # 查询
    def fetch_all(self, sql, params=None):
        """获取所有查询结果
        参数:
            sql: SQL查询语句
            params: SQL参数，用于参数化查询
        返回:
            查询结果列表，失败返回空列表
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"获取数据时出错: {e}")
            return []

    # 分页查询
    def fetch_page(self, sql, page_num, page_size, params=None):
        page_sql = f" limit {(page_num - 1) * page_size},{page_size}"
        print(sql + page_sql)
        return self.fetch_all(sql + page_sql, params)

    def fetch_one(self, sql, params=None):
        """获取单条查询结果

        参数:
            sql: SQL查询语句
            params: SQL参数，用于参数化查询
        返回:
            单条查询结果，失败返回None
        """
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"获取数据时出错: {e}")
            return None

    ############################################################

    # 销毁对象时关闭数据库连接
    def __del__(self):
        try:
            self.execute("VACUUM;")
            """关闭数据库连接"""
            if self.conn:
                self.cursor.close()
                self.conn.close()
        except sqlite3.Error as e:
            pass
