# Article 9：雲端訓練平台選擇指南

## 主流平台比較

主要雲端 GPU 提供商：
- AWS：EC2 P4d（ A100）、多種執行個體類型、生態成熟
- Google Cloud：TPU 支援、强大的網路基礎設施
- Azure：與 Microsoft 生態深度整合、好的 Windows 支援
- Lambda Labs：專注於 ML、性價比高

## 成本考量

GPU 小時費用差異大：
- .spot/low-priority 實例可節省 60-90%
- 長期承諾有折扣
- 考慮網路和儲存成本

## 網路頻寬

對於多節點訓練，節點間網路頻寬至關重要：
- AWS P4d 提供 400 Gbps
- Google Cloud TPU 提供高速互聯
- 確認網路拓撲滿足訓練需求

## 使用者體驗

1. 影像和框架支援是否齐備
2. 文件和社群是否活躍
3. 工具和平臺的整合度

## 建議的選擇流程

1. 評估模型和資料規模
2. 確定需要的 GPU 數量和類型
3. 比較成本（小心隱藏費用）
4. 考虑易用性和支援

## 參考資源

- Cloud GPU Comparison：https://www.google.com/search?q=cloud+GPU+comparison+A100+2021
- Lambda Labs Pricing：https://www.google.com/search?q=Lambda+labs+GPU+pricing