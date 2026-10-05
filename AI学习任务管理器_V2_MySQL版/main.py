from task_manager import TaskManager


def print_menu():
    print("\n========== AI学习任务管理器 V2 ==========")
    print("1. 添加学习任务")
    print("2. 查看全部任务")
    print("3. 搜索任务")
    print("4. 完成任务")
    print("5. 删除任务")
    print("0. 退出")
    print("========================================")


def add_task(manager):
    title = input("请输入任务名称：").strip()
    subject = input("请输入科目：").strip()
    minutes = int(input("请输入预计学习时间（分钟）："))
    priority = input("请输入优先级（高/中/低）：").strip()

    manager.add_task(title, subject, minutes, priority)
    print("✅ 任务添加成功！")


def show_tasks(manager, tasks=None):
    if tasks is None:
        tasks = manager.get_all_tasks()

    if not tasks:
        print("暂无任务。")
        return

    print("\n---------------- 学习任务 ----------------")
    for task in tasks:
        status = "✅ 已完成" if task["completed"] else "⬜ 未完成"
        print(
            f'ID:{task["id"]} | '
            f'[{status}] | '
            f'{task["title"]} | '
            f'科目:{task["subject"]} | '
            f'时间:{task["minutes"]}分钟 | '
            f'优先级:{task["priority"]}'
        )
    print("----------------------------------------")


def search_tasks(manager):
    keyword = input("请输入搜索关键词：").strip()
    tasks = manager.search_tasks(keyword)
    show_tasks(manager, tasks)


def complete_task(manager):
    task_id = int(input("请输入要完成的任务 ID："))
    if manager.complete_task(task_id):
        print("✅ 任务已完成！")
    else:
        print("❌ 没有找到该任务。")


def delete_task(manager):
    task_id = int(input("请输入要删除的任务 ID："))
    if manager.delete_task(task_id):
        print("✅ 任务删除成功！")
    else:
        print("❌ 没有找到该任务。")


def main():
    manager = TaskManager()

    try:
        while True:
            print_menu()
            choice = input("请选择操作：").strip()

            try:
                if choice == "1":
                    add_task(manager)
                elif choice == "2":
                    show_tasks(manager)
                elif choice == "3":
                    search_tasks(manager)
                elif choice == "4":
                    complete_task(manager)
                elif choice == "5":
                    delete_task(manager)
                elif choice == "0":
                    print("程序已退出，再见！")
                    break
                else:
                    print("❌ 请输入 0~5 之间的数字。")
            except ValueError:
                print("❌ 输入格式错误：学习时间和任务 ID 必须是数字。")
    finally:
        manager.close()


if __name__ == "__main__":
    main()
