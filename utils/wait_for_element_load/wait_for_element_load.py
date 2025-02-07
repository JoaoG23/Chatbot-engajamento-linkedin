from time import sleep


def wait_for_element_load(element, name_elemento):
    while len(element) < 1:
        print(f"element {name_elemento} loading....")
        sleep(2)
    print(f"{name_elemento} element found.")