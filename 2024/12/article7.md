# 全端開發者技能地圖

## 2024 全端開發者必備技能

```javascript
// 全端開發者技能樹評估系統
class FullStackSkillTree {
  constructor() {
    this.categories = {
      frontend: {
        score: 0,
        skills: ['HTML/CSS', 'JavaScript', 'React/Vue', '效能優化', '可及性']
      },
      backend: {
        score: 0,
        skills: ['Node.js', 'API 設計', '資料庫', '快取策略', '認證授權']
      },
      devops: {
        score: 0,
        skills: ['Git', 'CI/CD', '容器化', '雲端服務', '監控']
      },
      ai: {
        score: 0,
        skills: ['Prompt Engineering', 'AI API 整合', '模型微調', 'RAG 架構']
      },
      soft: {
        score: 0,
        skills: ['溝通協作', '系統設計', '程式碼審查', '技術文件']
      }
    };
  }

  assess(category, skill, level) {
    const cat = this.categories[category];
    if (cat && cat.skills.includes(skill)) {
      cat.score = Math.min(100, cat.score + level * 20);
    }
    return this;
  }

  report() {
    const total = Object.values(this.categories)
      .reduce((sum, c) => sum + c.score, 0);
    const avg = total / Object.keys(this.categories).length;
    
    return {
      score: avg,
      level: avg >= 80 ? '專家' : avg >= 60 ? '進階' : avg >= 40 ? '中級' : '初級',
      details: this.categories
    };
  }
}

const dev = new FullStackSkillTree();
dev.assess('frontend', 'React/Vue', 5)
   .assess('backend', 'Node.js', 5)
   .assess('backend', '資料庫', 4)
   .assess('devops', 'CI/CD', 4)
   .assess('ai', 'AI API 整合', 3)
   .assess('soft', '系統設計', 4);

console.log(dev.report());
```

## 2024 年最受歡迎的技能組合

1. **React + Node.js + TypeScript**：經典全端組合
2. **Next.js + Vercel + Prisma**：現代全端棧
3. **React Native + Firebase**：行動全端
4. **Python + FastAPI + React**：AI 應用全端

## 學習資源

線上課程平台 Coursera、Udemy、Frontend Masters 持續提供最新課程。

## 證照與認證

2024 年雲端認證（AWS、GCP、Azure）需求強勁。

## 職涯建議

全端開發者應保持 T 型技能結構：廣泛了解各領域，深度精通其中 1-2 項。

> 參考：https://www.google.com/search?q=full+stack+developer+skill+map+2024
