import openai
import pymysql

class MedicalServiceExtractor:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        openai.api_base = "https://api.foureast.cn/v1"
        self.prompt_template = (
            "请你从输入的文本中提取出医疗服务收费项目的名称，并将其转换为标准格式输出。\n"
            "输出格式如下：['医疗服务收费项目名称1', '医疗服务收费项目名称2', '医疗服务收费项目名称3',...]\n"
            "例子：\n"
            "输入：医院为脊柱滑脱患者行脊柱椎间融合器植入植骨融合术，收取“脊柱椎间融合器植入植骨融合术”“脊髓和神经根粘连松解术”费用。\n"
            "输出：['脊柱椎间融合器植入植骨融合术', '脊髓和神经根粘连松解术']"
        )
    
    def extract_service_names(self, text):
        prompt = f"{self.prompt_template}\n输入：{text}\n输出："
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一位擅长提取文本信息的助手。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error: {e}")
            return None

# 使用示例
if __name__ == "__main__":
    api_key = "sk-JpP5E3J1fIIpqfuf82A362E05e724067995b51Df399e035d"
    extractor = MedicalServiceExtractor(api_key)
    input_text = "医院为脊柱滑脱患者行脊柱椎间融合器植入植骨融合术，收取“脊柱椎间融合器植入植骨融合术”“脊髓和神经根粘连松解术”费用。"
    
    result = extractor.extract_service_names(input_text)
    print(result)


class MedicalServiceSQLGenerator:
    def __init__(self, api_key, conn_details):
        self.api_key = api_key
        self.conn_details = conn_details
        openai.api_key = self.api_key
        openai.api_base = "https://api.foureast.cn/v1"
        self.prompt_template = (
            "你擅长使用数据库Mysql，接下来根据提供的医疗服务收费项目名称，请你返回包含该医疗服务收费项目属性值的完整记录的查询语句，"
            "不要返回任何多余的内容，你的回答必须是可执行的SQL语句。SQL语句为："
            "SELECT * FROM medical WHERE item = '特定收费项目';"
        )

    def generate_sql_queries(self, service_names):
        sql_queries = []
        for name in service_names:
            prompt = f"{self.prompt_template}\n输入：{name}\n输出："
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "你是一位数据库专家。"},
                        {"role": "user", "content": prompt}
                    ],
                    max_tokens=150,
                    n=1,
                    stop=None,
                    temperature=0.7,
                )
                sql_query = response['choices'][0]['message']['content'].strip()
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
                        # 获取查询结果
                        result = cursor.fetchall()
                        results.append(result)
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

# 使用示例
if __name__ == "__main__":
    api_key = "sk-JpP5E3J1fIIpqfuf82A362E05e724067995b51Df399e035d"
    conn_details = {
        "host": "localhost",
        "port": 3306,
        "user": "root",
        "password": "your-database-password",
        "database": "medical",
    }

    service_names = ["脊柱椎间融合器植入植骨融合术", "脊髓和神经根粘连松解术"]

    # 实例化类
    sql_generator = MedicalServiceSQLGenerator(api_key, conn_details)

    # 生成 SQL 查询语句
    sql_queries = sql_generator.generate_sql_queries(service_names)
    
    # 执行 SQL 查询并获取结果
    query_results = sql_generator.execute_sql_queries(sql_queries)
    
    # 输出查询结果
    for result in query_results:
        print(result)


class MedicalServiceChargeChecker:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = self.api_key
        openai.api_base = "https://api.foureast.cn/v1"
        self.prompt_template = (
            "你是一位医保控费管理人员，请你根据查询到的数据判断这些医疗服务收费项目之间的是否有包含关系，"
            "返回他们之间的关系。并通过他们之间的关系判断此次医疗服务收费有无违规问题，返回判断结果和判断依据。"
        )
    
    def check_charge(self, medical_data):
        # 构造 prompt
        prompt = f"{self.prompt_template}\n输入：查询到的数据：{medical_data}\n输出："
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "你是一位医保控费专家。"},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                n=1,
                stop=None,
                temperature=0.7,
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Error in charge check: {e}")
            return None

# 使用示例
if __name__ == "__main__":
    api_key = "sk-JpP5E3J1fIIpqfuf82A362E05e724067995b51Df399e035d"
    
    # 查询到的医疗服务收费项目数据
    medical_data = "脊柱椎间融合器植入植骨融合术项目内涵：含脊髓神经根松解、椎板切除减压、脊髓探查、骨折切开复位。"

    # 实例化类
    charge_checker = MedicalServiceChargeChecker(api_key)

    # 检查收费合规性
    charge_result = charge_checker.check_charge(medical_data)
    
    # 输出判断结果
    print(charge_result)
