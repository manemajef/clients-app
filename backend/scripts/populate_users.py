import requests 

def cap(name:str)->str:
    return name[0].upper()+name[1:]

def main():
    names = ["rotem", "shani", "adva", "shaked", "orly", "omri", "george", "jeff", "john"]
    for name in names:
        email = name 
        full_name = cap(name)
        password = name 
        print("requesting")
        payload = {"email": email, "full_name": full_name, "password": password}
        res = requests.post("http://localhost:8000/auth/register", json = payload )
        print(res)
    # pass 
    
if __name__ == "__main__":
    main()

