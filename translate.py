import argparse
import os
import pandas as pd
import torch
import wandb
import re
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, BitsAndBytesConfig
from tqdm.auto import tqdm
import gdown
# === 🔧 CONFIGURATION DU MODÈLE ===
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type='nf4',
)
model_name = "google/madlad400-7b-mt"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name, quantization_config=bnb_config, device_map="auto")

# === 🧼 FONCTION DE NETTOYAGE ===
def clean_sentence(sentence: str) -> str:
    sentence = re.sub(r'http\S+|www\S+', '', sentence)
    sentence = re.sub(r'\(.*?\)|\[.*?\]', '', sentence)
    sentence = sentence.replace('_', ' ')
    sentence = re.sub(r'-{2,}', ' ', sentence)
    sentence = sentence.replace('"', '')
    sentence = re.sub(r'\s+', ' ', sentence).strip()
    return sentence

# === 🌐 TRADUCTION PAR BATCH AVEC INDICES ===
def translate_to_malagasy(sentences, batch_size=16, run=None, start_index=0):
    translated_sentences = []
    total = len(sentences)

    for i in tqdm(range(0, total, batch_size)):
        batch_start = start_index + i
        batch_end = start_index + min(i + batch_size - 1, total - 1)

        print(f"[INFO] Traduction des lignes {batch_start} à {batch_end}")
        if run:
            run.log({"batch_start": batch_start, "batch_end": batch_end})

        batch_sentences = sentences[i:i + batch_size]
        inputs = tokenizer(
            [f"<2mg> {s}" for s in batch_sentences],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        ).to(device)

        with torch.no_grad():
            outputs = model.generate(
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_new_tokens=256
            )

        batch_translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        translated_sentences.extend(batch_translated)
        torch.cuda.empty_cache()

    return translated_sentences

# === 🧩 TRAITEMENT D’UNE PLAGE DANS UN DATASET ===
def process_dataset(df,batch_size, start_index, end_index, run, dataset_name):
    print(f"[INFO] 🔍 Traduction des lignes {start_index} à {end_index - 1} du dataset {dataset_name}")

    sub_df = df.iloc[start_index:end_index].copy()
    sub_df["clean"] = sub_df["text"].astype(str).apply(clean_sentence)
    sub_df["translated_clean"] = translate_to_malagasy(sub_df["text"].tolist(),batch_size, run=run, start_index=start_index)

    output = f"translated_{dataset_name}_{start_index}_{end_index}.csv"
    sub_df.to_csv(output, index=False, encoding="utf-8")
    print(f"[INFO] ✅ Fichier local : {output}")

    # 📦 Upload en tant qu'artifact W&B
    artifact = wandb.Artifact(
        name=f"{dataset_name}_{start_index}_{end_index}_output",
        type="translated-csv",
        description=f"Traduction partielle : lignes {start_index} à {end_index - 1}",
    )
    artifact.add_file(output)
    run.log_artifact(artifact)

# === 🎯 POINT D’ENTRÉE DU SCRIPT ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Traduction en lot avec indices")
    parser.add_argument("--file", type=str, required=True, help="Nom du fichier CSV")
    parser.add_argument("--link", type=str, required=True, help="url")
    parser.add_argument("--start_index", type=int, required=True, help="Indice de début (inclus)")
    parser.add_argument("--end_index", type=int, required=True, help="Indice de fin (exclusif)")
    parser.add_argument("--batch_size", type=int, default=16, help="Taille des batchs de traduction")
    args = parser.parse_args()
    url = args.link
    output_path = args.file
    gdown.download(url, output_path, quiet=False,fuzzy=True)
    df = pd.read_csv(output_path)
    wandb.login(key="78b2f42b1fa7c098b98eca0f29726270d192ba5d")
    dataset_name = os.path.splitext(os.path.basename(args.file))[0]
    # ✅ UN SEUL run par dataset
    run = wandb.init(
        project="TRADUCTION_PARALLELE",
        name=output_path,
        config={
            "dataset": output_path,
            "column": "text"
        }
    )

    process_dataset(df,args.batch_size, args.start_index, args.end_index, run, dataset_name)
    run.finish()
