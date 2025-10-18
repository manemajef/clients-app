from app.database import get_sqlmodel_schema

def main():
    for name, table in get_sqlmodel_schema():
        print(f"\n## Table: {name}\n")
        print("| name | type | primary key |")
        print("| ---- | ---- | ---- | ---- |")
        for col in table.columns:
            name = col.name
            type = col.type
            pk = col.primary_key
            nullable = col.nullable
            print(f"| {name} | {type} |{nullable} | {pk} |")


if __name__ == "__main__":
    main()
