import tiktoken
import pandas as pd
import openai
from openai.embeddings_utils import cosine_similarity


openai.api_key = '키입력'

def search_functions(user_query, top_n = 3, pprint = True) :
    #csv 파일 불러와서 데이터프레임 형태로 변환
    texts_df = pd.read_csv('../docs/data_with_embeddings.csv')
    texts_df['text_embedding'] = texts_df['text_embedding'].apply(lambda x: eval(x))
    #print(texts_df.head(5))

    #총 토큰 개수 확인하기
    #sum=0
    #for i in texts_df['n_tokens'] :
    #    sum += i
    #print(sum)
    #print(len(texts_df))
    #print(texts_df) #데이터프레임 내용 확인 [343 rows x 3 columns]

    #코사인 유사도를 통해 질문과 학칙 사이의 거리 구하고, 내용과 값 추출하기
    embedding = openai.Embedding.create(input = user_query, model = 'text-embedding-ada-002')
    embedding = embedding['data'][0]['embedding']
    texts_df['similarities'] = texts_df['text_embedding'].apply(lambda x: cosine_similarity(x, embedding))
    
    res = texts_df.sort_values('similarities', ascending = False).head(top_n)

    if pprint :
        for r in res.iterrows() :
            print(f"cosine similarity = {round(r[1]['similarities'], 3)}")
            print(f"{r[1]['content']}")
            print('-' * 70)

    return res

#res = search_functions('근신이란 무엇인가?', top_n = 4)

def compare_encodings(example_string: str) -> None :
    print(f'\nExample string: "{example_string}"')

    for encoding_name in ["gpt2", "p50k_base", "cl100k_base"] :
        encoding = tiktoken.get_encoding(encoding_name)
        token_integers = encoding.encode(example_string)
        num_tokens = len(token_integers)
        token_bytes = [encoding.decode_single_token_bytes(token) for token in token_integers]

        print()
        print(f"{encoding_name}: {num_tokens} tokens")
        print(f"token integers: {token_integers}")
        print(f"token bytes: {token_bytes}")