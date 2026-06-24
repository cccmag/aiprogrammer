# 神經機器翻譯的進展

機器翻譯從規則系統發展到神經網路，經歷了漫長的歷程。

## 1.  Seq2Seq 模型

Seq2Seq 是第一代神經機器翻譯模型：

```python
class Seq2Seq(nn.Module):
    def __init__(self, encoder, decoder):
        super().__init__()
        self.encoder = encoder
        self.decoder = decoder

    def forward(self, src, tgt):
        encoder_output = self.encoder(src)
        decoder_output = self.decoder(tgt, encoder_output)
        return decoder_output
```

## 2. 注意力機制

注意力讓翻譯模型能夠對齊源序列和目標序列。

## 3. Transformer 翻譯

Transformer 已成為機器翻譯的主流架構：
- 完全并行計算
- 更好的翻譯品質
- 更强的長距離依賴

## 4. 多語言翻譯

mBART 等模型支援多語言統一翻譯。

## 5. 結論

神經機器翻譯已經達到接近人類譯者的水平。

---

## 延伸閱讀

- [Google 翻譯技術](https://www.google.com/search?q=Google+neural+machine+translation+technology)
- [OpenNMT 工具](https://www.google.com/search?q=OpenNMT+neural+machine+translation)