from pymongo import MongoClient
from datetime import datetime
import logging
import os
import time
import sys


class MongoSync:
    def __init__(self, cloud_uri, local_uri):
        """
        Khởi tạo kết nối đến MongoDB Cloud và Local
        :param cloud_uri: URI kết nối MongoDB Cloud
        :param local_uri: URI kết nối MongoDB Local
        """
        self.cloud_uri = cloud_uri
        self.local_uri = local_uri
        self.setup_logging()

    def setup_logging(self):
        """Cấu hình logging"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('mongo_sync.log'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)

    def connect(self):
        """Thiết lập kết nối đến cả hai database"""
        try:
            self.cloud_client = MongoClient(self.cloud_uri)
            self.local_client = MongoClient(self.local_uri)
            self.logger.info("Successfully connected to both Cloud and Local MongoDB")
        except Exception as e:
            self.logger.error(f"Connection error: {str(e)}")
            raise

    def get_database_names(self):
        """Lấy danh sách các database từ cloud"""
        return self.cloud_client.list_database_names()

    def sync_collection(self, db_name, collection_name):
        """
        Đồng bộ một collection cụ thể
        """
        try:
            cloud_db = self.cloud_client[db_name]
            local_db = self.local_client[db_name]

            cloud_collection = cloud_db[collection_name]
            local_collection = local_db[collection_name]

            # Lấy số lượng documents
            cloud_count = cloud_collection.count_documents({})

            self.logger.info(f"Syncing collection {collection_name} ({cloud_count} documents)")

            # Lấy tất cả documents từ cloud
            cloud_docs = cloud_collection.find()

            # Tạo index giống như cloud
            cloud_indexes = cloud_collection.list_indexes()
            for index in cloud_indexes:
                if index['name'] != '_id_':  # Bỏ qua index mặc định
                    local_collection.create_index(
                        [(key, value) for key, value in index['key'].items()],
                        unique=index.get('unique', False)
                    )

            # Xử lý từng document
            for doc in cloud_docs:
                # Kiểm tra xem document đã tồn tại chưa
                existing_doc = local_collection.find_one({'_id': doc['_id']})

                if existing_doc:
                    # Cập nhật nếu document đã tồn tại
                    local_collection.replace_one({'_id': doc['_id']}, doc)
                else:
                    # Thêm mới nếu chưa tồn tại
                    local_collection.insert_one(doc)

            self.logger.info(f"Successfully synchronized collection {collection_name}")

        except Exception as e:
            self.logger.error(f"Error syncing collection {collection_name}: {str(e)}")
            raise

    def sync_database(self, db_name):
        """
        Đồng bộ toàn bộ database
        """
        try:
            cloud_db = self.cloud_client[db_name]
            collections = cloud_db.list_collection_names()

            self.logger.info(f"Starting synchronization of database {db_name}")

            for collection_name in collections:
                self.sync_collection(db_name, collection_name)

            self.logger.info(f"Completed synchronization of database {db_name}")

        except Exception as e:
            self.logger.error(f"Error syncing database {db_name}: {str(e)}")
            raise

    def sync_all(self):
        """
        Đồng bộ toàn bộ databases
        """
        try:
            self.connect()
            databases = self.get_database_names()

            # Bỏ qua các database hệ thống
            # system_dbs = ['admin', 'local', 'config']
            system_dbs = []
            databases = [db for db in databases if db not in system_dbs]

            self.logger.info(f"Starting synchronization of {len(databases)} databases")

            for db_name in databases:
                self.sync_database(db_name)

            self.logger.info("Completed synchronization of all databases")

        except Exception as e:
            self.logger.error(f"Error during synchronization process: {str(e)}")
        finally:
            self.cloud_client.close()
            self.local_client.close()


def main():
    # Cấu hình URI kết nối
    CLOUD_URI = "mongodb+srv://Admin:123456789Kha%40@cluster0.nmxwx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    LOCAL_URI = "mongodb://localhost:27017/"

    # Khởi tạo đối tượng sync
    syncer = MongoSync(CLOUD_URI, LOCAL_URI)

    # while True:
    #     try:
    #         # Thực hiện đồng bộ
    #         syncer.sync_all()
    #
    #         # Đợi 1 tiếng trước khi đồng bộ lại
    #         time.sleep(3600)  # 3600 giây = 1 tiếng
    #
    #     except KeyboardInterrupt:
    #         print("\nDừng quá trình đồng bộ...")
    #         break
    #     except Exception as e:
    #         print(f"Lỗi: {str(e)}")
    #         # Đợi 5 phút trước khi thử lại nếu có lỗi
    #         time.sleep(300)
    try:
        # Thực hiện đồng bộ
        syncer.sync_all()

        # Đợi 1 tiếng trước khi đồng bộ lại
        time.sleep(3600)  # 3600 giây = 1 tiếng

    except KeyboardInterrupt:
        print("\nStopping synchronization process...")
    except Exception as e:
        print(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
