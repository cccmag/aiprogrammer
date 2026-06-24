# Article 5：資料處理中的常見陷阱與解決方案

## SettingWithCopyWarning

這是 pandas 最常見的警告之一。當你對切片操作後嘗試修改資料時，pandas 不確定你是要修改原資料還是創建新資料。解決方案：使用 `.copy()` 明確複製，或使用 `.loc[]` 進行標籤型索引。

## 記憶體持續飆升

處理大型 DataFrame 時，記憶體可能持續增長。這通常是因為鏈式賦值產生了很多臨時物件。解決方案：避免鏈式索引，用單一賦值語句完成所有操作。必要時調用 `del` 刪除不需要的中間變數。

## 字串和數字的混淆

pandas 中同樣的名字可能指涉不同的型別。`'1'` 是字串，`1` 是整數。比較時要注意型別轉換。`df['a'].astype(int)` 可轉換為數字。nullable integer 如 `Int64` 可避免 NaN 轉換問題。

## 日期時區處理

datetime 涉及時區時常常出問題。建議在進入系統時就轉換為 UTC，內部處理時保持 UTC，只在展示時轉換為本地時區。使用 `pd.to_datetime()` 時指定 `utc=True` 明確處理時區。

## 參考資源

- pandas Troubleshooting：https://www.google.com/search?q=pandas+common+mistakes
- SettingWithCopy Guide：https://www.google.com/search?q=pandas+settingwithcopy+warning+fix