import pyautogui
import pyperclip
import keyboard
import time
import sys
import threading

# 全局变量用于控制输入进程
typing_active = False
stop_event = threading.Event()

# 添加输入法自动切换开关，默认为False（不自动切换）
AUTO_SWITCH_INPUT_METHOD = True

def show_instructions():
    """显示使用说明"""
    print(
        """
 /$$     /$$                                               
|  $$   /$$/                                               
 \  $$ /$$//$$$$$$   /$$$$$$$  /$$$$$$  /$$   /$$  /$$$$$$ 
  \  $$$$//$$__  $$ /$$_____/ /$$__  $$| $$  | $$ |____  $$
   \  $$/| $$  \ $$|  $$$$$$ | $$$$$$$$| $$  | $$  /$$$$$$$
    | $$ | $$  | $$ \____  $$| $$_____/| $$  | $$ /$$__  $$
    | $$ |  $$$$$$/ /$$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$
    |__/  \______/ |_______/  \_______/ \____  $$ \_______/
                                        /$$  | $$          
                                       |  $$$$$$/          
                                        \______/                
"""
    )
    # print("=" * 40)
    print("欢迎使用 自动打字机1.0")
    print("使用步骤：")
    print("1. 将需要输入的文本内容复制到剪贴板")
    print("2. 将光标放到想输入的输入框内")
    print("3. 按下 Ctrl+Alt+V 开始自动输入")
    print("——" * 20)
    if AUTO_SWITCH_INPUT_METHOD:
        print("注意：请确保输入法为英文模式")
        # print("注意：程序会尝试自动切换到英文输入法")
    else:
        print("注意：请手动确保输入法为英文模式")
    print("输入过程中按 Esc 键可随时停止")
    print("=" * 40)


def switch_to_english_input():
    """
    切换到英文输入法
    注意：此方法在不同操作系统上可能有所不同
    """
    try:
        # Windows系统切换到英文输入法
        # 使用Alt+Shift组合来切换输入法（更安全的方式）
        pyautogui.hotkey("alt", "shift")
        time.sleep(0.5)
    except Exception as e:
        print(f"切换输入法时出错: {e}")


def type_text(text):
    """
    模拟人工打字输入文本

    Args:
        text (str): 要输入的文本
    """
    global typing_active

    # 设置打字速度参数
    pyautogui.PAUSE = 0.01  # 基础停顿时间
    print(f"开始输入...")

    # 逐字符输入文本
    for i, char in enumerate(text):
        # 检查是否需要停止
        if stop_event.is_set():
            print("\n输入已停止")
            typing_active = False
            return
        # 输入当前字符
        pyautogui.write(char)
    print("输入完成！\n")
    typing_active = False


def start_typing():
    """开始打字流程"""
    global typing_active

    if typing_active:
        print("已经在输入中，请勿重复启动")
        return

    # 获取剪贴板内容
    try:
        clipboard_content = pyperclip.paste()
    except Exception as e:
        print(f"读取剪贴板失败: {e}")
        return

    if not clipboard_content:
        print("剪贴板为空，请先复制要输入的文本")
        return

    # 只保留文字内容
    text_to_type = "".join(
        char for char in clipboard_content if char.isprintable() or char.isspace()
    )

    if not text_to_type.strip():
        print("剪贴板中没有有效的文本内容")
        return

    print(f"准备输入文本...")
    print(f"(共{len(text_to_type)}个字符)")
    print("——" * 20)
    print(text_to_type[:100] + ("..." if len(text_to_type) > 100 else ""))
    print("——" * 20)

    # 根据配置决定是否切换到英文输入法
    if AUTO_SWITCH_INPUT_METHOD:
        # print("正在切换到英文输入法...")
        switch_to_english_input()
    else:
        print("请确保已手动切换到英文输入法")

    # 启动打字线程
    typing_active = True
    stop_event.clear()
    typing_thread = threading.Thread(target=type_text, args=(text_to_type,))
    typing_thread.daemon = True
    typing_thread.start()


def stop_typing():
    """停止打字"""
    global typing_active
    if typing_active:
        print("\n正在停止输入...")
        stop_event.set()
        typing_active = False
    else:
        print("当前没有正在进行的输入任务")


def main():
    """主函数"""
    show_instructions()

    # 注册快捷键
    keyboard.add_hotkey("ctrl+alt+v", start_typing)
    keyboard.add_hotkey("esc", stop_typing)

    print("程序已启动，等待快捷键命令...")
    print("按 Ctrl+C 退出程序")

    # 保持程序运行
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("\n程序已退出")


if __name__ == "__main__":
    main()
