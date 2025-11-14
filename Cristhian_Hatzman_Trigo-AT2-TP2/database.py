from pymongo import MongoClient

def conectar_db():
    
    try:
        client = MongoClient('mongodb://localhost:27017/')
        
        client.admin.command('ismaster')
        print("Conexão com MongoDB estabelecida com sucesso!")
        
        
        db = client['Cristhian_Hatzman_Trigo_AT2_TP2']
        return db
    except Exception as e:
        print(f"Erro ao conectar com o MongoDB: {e}")
        return None


if __name__ == "__main__":
    db = conectar_db()
    if db:
        print(f"Coleções existentes: {db.list_collection_names()}")