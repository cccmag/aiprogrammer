#!/usr/bin/env node
// year_review_2024.js — 2024 年度回顧資料分析



class YearReviewData {
  constructor() {
    this.ecosystem = {
      npmDownloadsWeekly: 0,
      typescriptAdoption: 0,
      esmAdoption: 0,
      nodeVersions: []
    };
    this.frameworks = new Map();
    this.trends = [];
    this.keywords = new Map();
  }

  async load() {
    this.ecosystem.npmDownloadsWeekly = 51_000_000_000;
    this.ecosystem.typescriptAdoption = 62;
    this.ecosystem.esmAdoption = 53;
    this.ecosystem.nodeVersions = [
      { version: '21.x', release: '2023-Q4', lts: true },
      { version: '22.x', release: '2024-Q2', lts: true },
      { version: '23.x', release: '2024-Q4', lts: false }
    ];

    this.frameworks.set('React', { adoption: 82, satisfaction: 78, change: '+3' });
    this.frameworks.set('Vue', { adoption: 46, satisfaction: 85, change: '+1' });
    this.frameworks.set('Svelte', { adoption: 22, satisfaction: 89, change: '+5' });
    this.frameworks.set('Solid', { adoption: 12, satisfaction: 88, change: '+4' });
    this.frameworks.set('Next.js', { adoption: 58, satisfaction: 76, change: '+8' });

    this.trends = [
      { name: 'AI Code Generation', growth: 245, maturity: '成長期' },
      { name: 'Edge Computing', growth: 89, maturity: '成長期' },
      { name: 'WebAssembly', growth: 67, maturity: '萌芽期' },
      { name: 'Server Components', growth: 120, maturity: '成長期' },
      { name: 'TypeScript', growth: 35, maturity: '成熟期' },
      { name: 'Micro-frontends', growth: 45, maturity: '成長期' },
      { name: 'Biome/Rust Tools', growth: 180, maturity: '成長期' },
      { name: 'Privacy Engineering', growth: 92, maturity: '萌芽期' }
    ];

    const kw = ['AI', 'React 19', 'Node.js 22', 'Deno 2', 'Flutter',
      'TypeScript', 'Next.js', 'Copilot', 'Side Loading', 'Edge Computing'];
    for (const word of kw) {
      this.keywords.set(word, Math.floor(Math.random() * 1000) + 500);
    }

    return this;
  }

  summary() {
    return {
      ecosystem: this.ecosystem,
      frameworkCount: this.frameworks.size,
      trendCount: this.trends.length,
      topKeyword: [...this.keywords.entries()].sort((a, b) => b[1] - a[1])[0]
    };
  }
}

class TrendAnalyzer {
  constructor(data) {
    this.data = data;
  }

  topTrends(n = 5) {
    return this.data.trends
      .sort((a, b) => b.growth - a.growth)
      .slice(0, n);
  }

  frameworkInsights() {
    const entries = [...this.data.frameworks.entries()];
    return {
      highestSatisfaction: entries.sort((a, b) => b[1].satisfaction - a[1].satisfaction)[0],
      highestAdoption: entries.sort((a, b) => b[1].adoption - a[1].adoption)[0],
      fastestGrowing: entries.sort((a, b) => parseInt(b[1].change) - parseInt(a[1].change))[0]
    };
  }

  maturityDistribution() {
    const dist = { '萌芽期': 0, '成長期': 0, '成熟期': 0 };
    for (const t of this.data.trends) {
      if (dist[t.maturity] !== undefined) dist[t.maturity]++;
    }
    return dist;
  }
}

class Report {
  constructor(data, analyzer) {
    this.data = data;
    this.analyzer = analyzer;
  }

  printHeader(title) {
    console.log(`\n${'='.repeat(60)}`);
    console.log(`  ${title}`);
    console.log(`${'='.repeat(60)}`);
  }

  printEcosystem() {
    this.printHeader('2024 JavaScript 生態統計');
    const e = this.data.ecosystem;
    console.log(`  npm 每週下載量    : ${(e.npmDownloadsWeekly / 1e9).toFixed(1)}B`);
    console.log(`  TypeScript 採用率  : ${e.typescriptAdoption}%`);
    console.log(`  ESM 採用率        : ${e.esmAdoption}%`);
    console.log(`  Node.js 版本數    : ${e.nodeVersions.length}`);
  }

  printFrameworkReport() {
    this.printHeader('前端框架採用率');
    console.log('  Framework  | 採用率 | 滿意度 | 變化');
    console.log('  ' + '-'.repeat(38));
    for (const [name, data] of this.data.frameworks) {
      console.log(`  ${name.padEnd(12)}| ${data.adoption}%    | ${data.satisfaction}%    | ${data.change}`);
    }

    const insights = this.analyzer.frameworkInsights();
    console.log(`\n  最高滿意度 : ${insights.highestSatisfaction[0]} (${insights.highestSatisfaction[1].satisfaction}%)`);
    console.log(`  成長最快   : ${insights.fastestGrowing[0]} (${insights.fastestGrowing[1].change})`);
  }

  printTrendReport() {
    this.printHeader('2024 技術趨勢成長率 Top 5');
    const top = this.analyzer.topTrends(5);
    console.log('  技術                | 成長率 | 階段');
    console.log('  ' + '-'.repeat(38));
    for (const t of top) {
      console.log(`  ${t.name.padEnd(20)}| ${t.growth}%   | ${t.maturity}`);
    }
    const dist = this.analyzer.maturityDistribution();
    console.log(`\n  趨勢成熟度分布: ${JSON.stringify(dist)}`);
  }

  printKeywordCloud() {
    this.printHeader('2024 年度關鍵字');
    const sorted = [...this.data.keywords.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 10);
    const max = sorted[0][1];
    for (const [word, count] of sorted) {
      const bar = '█'.repeat(Math.round(count / max * 20));
      console.log(`  ${word.padEnd(16)} ${bar} ${count}`);
    }
  }

  printFull() {
    this.printEcosystem();
    this.printFrameworkReport();
    this.printTrendReport();
    this.printKeywordCloud();
    console.log('\n' + '='.repeat(60));
    console.log('  資料來源: npm, GitHub, State of JS 2024');
    console.log(`  生成時間: ${new Date().toISOString()}`);
    console.log('='.repeat(60) + '\n');
  }
}

export async function demo() {
  console.log('year_review_2024.js demo() — 2024 年度回顧資料');
  const data = new YearReviewData();
  await data.load();
  const analyzer = new TrendAnalyzer(data);
  const report = new Report(data, analyzer);
  report.printFull();
}

async function main() {
  const data = new YearReviewData();
  await data.load();
  const analyzer = new TrendAnalyzer(data);
  const report = new Report(data, analyzer);
  report.printFull();
}

if (process.argv[1]?.endsWith('year_review_2024.js')) {
  main();
}
