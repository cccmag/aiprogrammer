# 多模態模型評估

## 1. 多模態評估的獨特挑戰

多模態模型（如 GPT-4V、Gemini）同時處理文字與視覺輸入，評估需涵蓋跨模態理解、比對與推理能力。傳統單模態基準無法勝任。

## 2. MMMU 基準

MMMU（Massive Multi-discipline Multimodal Understanding）涵蓋六大領域 57 個科目，測試模型在圖表、示意圖與照片上的理解與推理能力。

```python
# MMMU 評估範例
def evaluate_mmmu(model, item):
    image = load_image(item["image"])
    question = item["question"]
    options = item["options"]
    prompt = f"請回答以下問題：{question}\n選項：{', '.join(options)}"
    response = model.generate(prompt, images=[image])
    return extract_answer(response)
```

## 3. 視覺問答評估

VQA 系列基準評估模型對影像內容的理解。進階版本如 VQA v2 平衡了語言偏誤，確保模型真正依賴視覺資訊作答。

## 4. 跨模態比對

需評估模型在文字-圖像檢索、圖像描述、視覺推理等任務的一致性。使用 CLIP Score、FID、CIDEr 等指標衡量生成品質。

```python
def cross_modal_score(text_emb, image_emb):
    similarity = cosine_similarity(text_emb, image_emb)
    return similarity.item()
```

## 5. 影片理解評估

Video-MME、EgoSchema 等基準擴展至時間維度，評估模型的影片理解、事件推理與時序定位能力。

## 6. 結語

多模態評估正快速從靜態圖像擴展至影片、音訊等多樣化場景。建立涵蓋跨模態推理與生成品質的評估框架，是推動多模態 AI 進步的關鍵基礎設施。

- https://www.google.com/search?q=MMMU+multimodal+benchmark
- https://www.google.com/search?q=VQA+visual+question+answering+evaluation
