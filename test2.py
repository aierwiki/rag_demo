def main():
    code = """
import datetime

def action() -> str:
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")
        """
    exec_globals = {}
    exec(code, exec_globals)
    result = exec_globals['action']()
    print(result)

if __name__ == "__main__":
    main()