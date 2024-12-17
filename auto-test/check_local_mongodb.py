from pymongo import MongoClient
import json


def check_local_mongodb():
    try:
        # Kết nối tới MongoDB local
        client = MongoClient('mongodb://localhost:27017/')

        # Liệt kê tất cả databases
        databases = client.list_database_names()
        print(f"\nDatabases found: {databases}")

        for db_name in databases:
            if db_name not in ['admin', 'config', 'local']:
                db = client[db_name]
                collections = db.list_collection_names()
                print(f"\nDatabase '{db_name}' collections:")

                for collection_name in collections:
                    count = db[collection_name].count_documents({})
                    print(f"- {collection_name}: {count} documents")

                    # Hiển thị một document mẫu
                    sample = db[collection_name].find_one()
                    if sample:
                        print(f"  Sample document structure:")
                        # Loại bỏ _id vì nó không serialize được
                        sample['_id'] = str(sample['_id'])
                        print(f"  {json.dumps(sample, indent=2)}")

        client.close()
        print("\nConnection test successful!")

    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    check_local_mongodb()