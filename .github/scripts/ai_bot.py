import os
import sys
from openai import OpenAI
from github import Github

# 配置部分
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"  # 如果用智谱，改成 https://open.bigmodel.cn/api/paas/v4/
MODEL_NAME = "deepseek-coder"          # 如果用智谱，改成 glm-4

def ai_edit_code(file_path, instruction):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    # 1. 读取原文件内容
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ 找不到文件: {file_path}")
        return False

    # 2. 构造提示词
    prompt = f"""
    你是一个 Python 代码专家。请根据以下要求修改代码。
    
    【原文件 {file_path}】:
    ```python
    {content}
    ```
    
    【修改要求】:
    {instruction}
    
    【输出规则】:
    请只输出修改后的完整代码，不要包含 ```python 或 ``` 标记，不要包含任何解释性文字。直接输出代码即可。
    """

    print(f"🤖 正在思考如何修改 {file_path} ...")
    
    # 3. 调用 DeepSeek
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a helpful code assistant."},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        temperature=0.1
    )
    
    new_code = response.choices[0].message.content.strip()
    
    # 清理可能存在的 markdown 标记
    if new_code.startswith("```"):
        lines = new_code.split('\n')
        if lines[0].startswith("```"): lines = lines[1:]
        if lines[-1].startswith("```"): lines = lines[:-1]
        new_code = "\n".join(lines)

    # 4. 写入文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_code)
    
    print(f"✅ 文件 {file_path} 已更新！")
    return True

if __name__ == "__main__":
    # 获取评论内容
    comment_body = os.environ.get("COMMENT_BODY", "")
    
    # 解析指令，格式必须是：/bot update 文件名: 修改要求
    # 例如：/bot update hello.py: 把变量名改成蛇形命名法
    if "/bot update" in comment_body:
        try:
            # 简单的文本解析
            parts = comment_body.split("/bot update")[1].strip().split(":", 1)
            target_file = parts[0].strip()
            instruction = parts[1].strip()
            
            success = ai_edit_code(target_file, instruction)
            if not success:
                sys.exit(1)
        except Exception as e:
            print(f"❌ 解析指令失败: {e}")
            print("正确格式示例: /bot update hello.py: 修改要求")
            sys.exit(1)
    else:
        print("未检测到 /bot update 指令，跳过执行。")
