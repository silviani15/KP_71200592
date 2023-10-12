import os, re, unicodedata, nltk
from nltk.tokenize import PunktSentenceTokenizer
from nltk.tokenize import sent_tokenize
import pandas as pd
import csv
import streamlit as st

class SearchEngine:
    def __init__(self):
        self.corpus = []
        self.content = dict()

    def detail_document(self, id_document, query):
        content = self.content[id_document]
        content = content.lower()
        split_query = query.split(' ')

        kalimat = sent_tokenize(content)
        return kalimat

    def search(self, query):
        results = []
        query = query.lower()
        
        for doc_id, content in self.content.items():
            content = content.lower()
            sentences = sent_tokenize(content)
            
            for sentence_id, sentence in enumerate(sentences):
                if query in sentence:
                    results.append({
                        'document_id': doc_id,
                        'sentence_id': sentence_id,
                        'sentence_text': sentence
                    })
        
        return results

if __name__ == '__main__':
    search_engine = SearchEngine()
    paths="D:\\2. Semester 6\\Pra KP\\Coba dulu\\corpus"
    id_folder = 'ID'
    en_folder = 'EN'
    sentences = []
    sentence2 = []
    header = ['textId' ,'docId','sentenceId']

    file_path = os.path.join(paths, id_folder)
    fnames = os.listdir(file_path)
 
    id_dokumen = []
    for i in range(len(fnames)):
        id_dokumen.append(str(fnames[i]).replace(".txt",""))
    
    for index, fname in enumerate (fnames):
        filedir = os.path.join(file_path, fname)
        with open(filedir, 'r', encoding='utf-8') as fh:
            fcontent = fh.read()
            fcontent = fcontent.lower()
            kalimats = sent_tokenize(fcontent)
            for kalimat_index, kalimat in enumerate(kalimats): 
                sentence2.append([kalimat, id_dokumen[index], kalimat_index])

    csv_filename = 'kalimat_sentences_coba_ID.csv'

    with open(csv_filename,'w',encoding='utf-8') as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        for sente in sentence2:
            # print(sente)
            writer.writerow(sente)

#looping ya or tidak
    title = st.text_input('Textual Similarity Detection', placeholder="Masukkan kalimat...")
    # Membaca konten dokumen dan menyimpannya dalam self.content
    for index, fname in enumerate(fnames):
        filedir = os.path.join(file_path, fname)
        with open(filedir, 'r', encoding='utf-8') as fh:
            fcontent = fh.read()
            search_engine.content[id_dokumen[index]] = fcontent

    if title != "":
        results = search_engine.search(title)
        
        # Menampilkan hasil pencarian
        if results:
            print("Hasil pencarian:")
            df = pd.DataFrame(results)
            df.rename(columns={'document_id': "Dokumen", 'sentence_id' : "Kalimat", 'sentence_text' : "Hasil"},inplace=True)
            st.table(df)
        else:
            st.info("Tidak ditemukan hasil pencarian.")
            print("Tidak ditemukan hasil pencarian.")