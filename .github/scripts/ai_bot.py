import os
import sys
from openai import OpenAI

# --- 配置区域 ---
API_KEY = os.environ.get("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"
MODEL_NAME = "deepseek-coder"

def clean_code_block(text):
    lines = text.strip().split('\n')
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines)

def ai_edit_code(file_path, instruction):
    client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    
    # === 关键修改：支持新建文件 ===
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"❌ 读取失败: {e}")
            return False
        status_msg = f"正在修改现有文件: {file_path}"
    else:
        # 如果文件不存在，视为空文件，准备新建
        content = "(New Empty File)"
        status_msg = f"⚠️ 文件不存在，正在创建新文件: {file_path}"
        # 自动创建目录（如果目录不存在）
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    print(f"🤖 {status_msg} ...")

    # 构造提示词
    prompt = f"""
    你是一个全能编程助手。请根据指令生成或修改文件内容。
    
    【目标文件】: {file_path}
    
    【原始内容】:
    ```
    {content}
    ```
    
    【修改指令】:
    {instruction}
    
    【输出规则】:
    1. 直接输出文件修改后的完整内容。
    2. 不要包含 ```markdown 或 ``` 标记，只输出内容本身。
    3. 如果是 Markdown 文件，请保持良好的 Markdown 格式。
    """

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Output ONLY the file content."},
                {"role": "user", "content": prompt},
            ],
            stream=False,
            temperature=0.1
        )
        new_code = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ API 调用失败: {e}")
        return False

    final_code = clean_code_block(new_code)

    # 写入文件
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(final_code)
        print(f"✅ 成功写入: {file_path}")
        return True
    except Exception as e:
        print(f"❌ 写入失败: {e}")
        return False

if __name__ == "__main__":
    comment_body = os.environ.get("COMMENT_BODY", "")
    trigger = "/bot update"
    
    if trigger in comment_body:
        try:
            command_part = comment_body.split(trigger)[1].strip()
            if ":" not in command_part:
                print("❌ 格式错误。正确格式: /bot update 文件名: 指令")
                sys.exit(1)

            target_file, instruction = command_part.split(":", 1)
            target_file = target_file.strip()
            instruction = instruction.strip()

            success = ai_edit_code(target_file, instruction)
            if not success:
                sys.exit(1)
        except Exception as e:
            print(f"❌ 执行出错: {e}")
            sys.exit(1)
    else:
        print("无有效指令")
