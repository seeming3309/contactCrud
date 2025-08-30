import argparse, json, sys, requests
BASE = "/api"
HOST = "http://127.0.0.1:8000"
def url(path): return f"{HOST}{BASE}{path}"

def list_contacts():
    r = requests.get(url("/contacts"))
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))

def get_contact(cid):
    r = requests.get(url(f"/contacts/{cid}"))
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))

def add_contact(name, phone):
    r = requests.post(url("/contacts"), json={"name": name, "phone": phone})
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))

def put_contact(cid, name, phone):
    r = requests.put(url(f"/contacts/{cid}"), json={"name": name, "phone": phone})
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))

def patch_contact(cid, name=None, phone=None):
    payload = {}
    if name is not None: payload["name"] = name
    if phone is not None: payload["phone"] = phone
    r = requests.patch(url(f"/contacts/{cid}"), json=payload)
    print(json.dumps(r.json(), ensure_ascii=False, indent=2))

def delete_contact(cid):
    r = requests.delete(url(f"/contacts/{cid}"))
    print(r.status_code, "(204 means deleted)")

def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list")
    g = sub.add_parser("get"); g.add_argument("id", type=int)
    a = sub.add_parser("add"); a.add_argument("name"); a.add_argument("phone")
    u = sub.add_parser("put"); u.add_argument("id", type=int); u.add_argument("name"); u.add_argument("phone")
    t = sub.add_parser("patch"); t.add_argument("id", type=int); t.add_argument("--name"); t.add_argument("--phone")
    d = sub.add_parser("del"); d.add_argument("id", type=int)

    args = p.parse_args()
    if args.cmd == "list": list_contacts()
    elif args.cmd == "get": get_contact(args.id)
    elif args.cmd == "add": add_contact(args.name, args.phone)
    elif args.cmd == "put": put_contact(args.id, args.name, args.phone)
    elif args.cmd == "patch": patch_contact(args.id, args.name, args.phone)
    elif args.cmd == "del": delete_contact(args.id)

if __name__ == "__main__":
    try:
        import requests
    except ImportError:
        print("pip install requests", file=sys.stderr); sys.exit(1)
    main()
