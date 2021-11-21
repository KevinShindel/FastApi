

def write_notification(email: str, message="") -> None:
    from time import sleep
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        sleep(5)
        print(content)
        email_file.write(content)
