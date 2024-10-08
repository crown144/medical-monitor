import openai
import pymysql


class MedicalServiceManager:
    def __init__(self, api_key, conn_details):
        self.api_key = api_key
        self.conn_details = conn_details
        openai.api_key = self.api_key
        openai.api_base = "https://api.foureast.cn/v1"
        
        sql_file = """
    CREATE DATABASE medical;
    USE medical;
    CREATE TABLE medical_service(
        地方医疗服务项目代码 varchar(255) NOT NULL PRIMARY KEY,
        地方医疗服务项目名称 varchar(255),
        项目内涵 varchar(255),
        除外内容 varchar(255),
        计价单位 varchar(255),
        项目说明 varchar(255)
    );
    """

        # 定义各类的 prompt 模板
        self.extractor_prompt = (
            "请你从输入的文本中提取出医疗服务收费项目的名称，并将其转换为标准格式输出。\n"
            "输出格式如下：['医疗服务收费项目名称1', '医疗服务收费项目名称2', '医疗服务收费项目名称3',...]\n"
            "除要求的输出外，不要返回任何多余的内容"
            "无需输出```json```之类的字符" 
            #"例子：\n"
            #"输入：医院为脊柱滑脱患者行脊柱椎间融合器植入植骨融合术，收取“脊柱椎间融合器植入植骨融合术”“脊髓和神经根粘连松解术”费用。\n"
            #"输出：['脊柱椎间融合器植入植骨融合术', '脊髓和神经根粘连松解术']"
        )
        self.sql_prompt = (
            "你擅长使用数据库Mysql，接下来根据我给你数据库的DDL语句和提供的医疗服务收费项目名称，请你返回包含该医疗服务收费项目属性值的完整记录的查询语句，"+
            "不要返回任何多余的内容，你的回答必须是可执行的SQL语句。DDL语句为：" + sql_file+
            "例子：SELECT * FROM medical WHERE item = '特定收费项目';"
            "无需输出```sql```之类的字符" 
        )
        self.charge_check_prompt = (
            "你是一位医保控费管理人员，请你根据查询到的数据判断这些医疗服务收费项目之间的是否有包含关系，"
            "返回他们之间的关系。并通过他们之间的关系判断此次医疗服务收费有无违规问题，返回判断结果和判断依据。"
            "注意：若存在查询数据为空，仅代表该项收费不包含其他收费，但该项目收费，请依照其他有查询结果的项目进行判断，若判断出有违规，直接输出结果和依据，若项目内涵中明确指出包含关系，可以直接判断为违规"
        )

    def extract_service_names(self, text):
        prompt = f"{self.extractor_prompt}\n输入：{text}\n输出："
        print(prompt)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "你是一位擅长提取文本信息的助手。"},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            response_text = response.choices[0].message.content
            # 将返回的字符串转换为列表
            service_names_list = eval(response_text)  # 使用 eval 将字符串转换为列表
            return service_names_list
        except Exception as e:
            print(f"Error extracting service names: {e}")
            return None

    def generate_sql_queries(self, service_names):
        sql_queries = []
        for name in service_names:
            prompt = f"{self.sql_prompt}\n输入：{name}\n输出："
            print(prompt)
            try:
                response = openai.ChatCompletion.create(
                model="gpt-4",
                 messages=[
            #{"role": "system", "content": "你是一位擅长提取文本信息的助手。"},
            {"role": "user", "content": prompt},
            ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
                sql_query = response.choices[0].message.content
                sql_queries.append(sql_query)
            except Exception as e:
                print(f"Error generating SQL for {name}: {e}")
                continue
        return sql_queries

    def execute_sql_queries(self, sql_queries):
        results = []
        conn = None
        try:
            # 连接到数据库
            conn = pymysql.connect(**self.conn_details)
            with conn.cursor() as cursor:
                for query in sql_queries:
                    try:
                        # 执行 SQL 查询
                        cursor.execute(query)
                        # 获取列名
                        column_names = [desc[0] for desc in cursor.description]
                        query_results = cursor.fetchall()
                        formatted_results = []
                        for row in query_results:
                            formatted_row = ", ".join(f"{name}是{value}" for name, value in zip(column_names, row))
                            formatted_results.append(formatted_row)
                        results.append(formatted_results)
                    except pymysql.MySQLError as e:
                        print(f"Error executing query '{query}': {e}")
                        results.append(None)
            conn.commit()
        except pymysql.MySQLError as e:
            print(f"Database connection error: {e}")
        finally:
            if conn:
                conn.close()
        return results

    def check_charge_compliance(self, query_data,charge_data):
        input_str = "输入："
        for i in range(len(query_data)):
            input_str += f"医疗服务项目代码{charge_data[i]}查询到的数据是：{query_data[i]};"
    
        # 移除最后的分号
        input_str = input_str.rstrip(';')
    
        # 构造完整的prompt字符串
        prompt1 = f"{input_str}\n输出："
        prompt = self.charge_check_prompt+prompt1
        print(prompt)
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                 messages=[
            # {"role": "system", "content": "你是一位擅长提取文本信息的助手。"},
            {"role": "user", "content": prompt},
            ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error checking charge compliance: {e}")
            return None

# 使用示例
if __name__ == "__main__":
    api_key = "sk-JpP5E3J1fIIpqfuf82A362E05e724067995b51Df399e035d"
    
    conn_details = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "1234567890Wyx",
        "database": "medical",
    }

    # 实例化类
    manager = MedicalServiceManager(api_key, conn_details)
    
    # Step 1: 提取医疗服务收费项目名称
    input_text = "医院为脊柱滑脱患者行脊柱椎间融合器植入植骨融合术，收取“脊柱椎间融合器植入植骨融合术”“脊髓和神经根粘连松解术”费用。"
    service_names = manager.extract_service_names(input_text)
    print(service_names)
    
    # Step 2: 生成并执行 SQL 查询
    #if service_names:
    #    sql_queries = manager.generate_sql_queries(service_names)
    #    query_results = manager.execute_sql_queries(sql_queries)
    
        # Step 3: 检查收费合规性
    #    if query_results:
    #        for result in query_results:
    #            charge_compliance = manager.check_charge_compliance(result)
    #            print(charge_compliance)
