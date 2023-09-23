import _ingest_data


def create_vectorstore(storeName) :
    try :
        filePath = "../docs/" + storeName
        vectorstore = _ingest_data.ingest_data()
        vectorstore.save_local(folder_path = filePath)

        print(f"Success to save FAISS index as {storeName}")
    
    except Exception as e :
        print(f'Error : {e}')
        raise ValueError("Failed to save FAISS index")
    

#if __name__ == '__main__' :
#    create_vectorstore('')