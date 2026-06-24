#!/usr/bin/env node

/**
 * devops_demo.js — DevOps 自動化流程模擬
 * 
 * 模擬 Docker 構建、CI 管線、部署策略
 */

function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function printHeader(title) {
  console.log(`\n=== ${title} ===\n`);
}

// Docker 構建流程模擬
async function simulateDockerBuild(imageName) {
  console.log(`🔨 構建映像: ${imageName}`);
  await delay(600);
  console.log(`✅ 構建完成`);
  console.log(`🏷️  標記映像: ${imageName}:latest`);
  await delay(200);
  console.log(`📤 推送映像到倉庫...`);
  await delay(400);
  console.log(`✅ 推送完成`);
  return { image: imageName, tag: 'latest', size: '245MB' };
}

// CI 管線階段
async function lint() {
  console.log('🔍 Lint...');
  await delay(300);
  console.log('✅ Lint 通過');
  return { success: true, stage: 'lint' };
}

async function unitTest() {
  console.log('🧪 Unit Tests...');
  await delay(500);
  console.log('✅ 通過 (42/42)');
  return { success: true, stage: 'unit', passed: 42, total: 42 };
}

async function build() {
  console.log('📦 Build...');
  await delay(600);
  console.log('✅ 構建完成');
  return { success: true, stage: 'build' };
}

async function integrationTest() {
  console.log('🔗 Integration Tests...');
  await delay(400);
  console.log('✅ 通過');
  return { success: true, stage: 'integration' };
}

async function deploy(version) {
  console.log(`🚀 Deploy... v${version}`);
  await delay(500);
  console.log(`✅ 部署完成 (v${version})`);
  return { success: true, stage: 'deploy', version };
}

// CI/CD 管線
async function runPipeline(version) {
  printHeader('CI 管線');

  const stages = [
    { name: 'Lint', fn: () => lint() },
    { name: 'Unit Tests', fn: () => unitTest() },
    { name: 'Build', fn: () => build() },
    { name: 'Integration Tests', fn: () => integrationTest() },
    { name: 'Deploy', fn: () => deploy(version) }
  ];

  const results = [];
  for (const stage of stages) {
    const result = await stage.fn();
    results.push(result);
    if (!result.success) {
      console.error(`❌ ${stage.name} 失敗，管線中斷`);
      return { success: false, results };
    }
  }
  return { success: true, results };
}

// 藍綠部署
async function blueGreenDeploy(version) {
  printHeader('部署策略 - 藍綠部署');
  console.log(`🟦 部署藍色環境 v${version}...`);
  await delay(600);
  console.log(`🔄 切換流量到藍色環境...`);
  await delay(400);
  if (version > 1) {
    console.log(`🟩 關閉綠色環境 v${version - 1}...`);
    await delay(300);
  }
  console.log('✅ 藍綠部署完成');
  return { strategy: 'blue-green', version, active: 'blue' };
}

// 滾動更新
async function rollingUpdate(version, instances) {
  printHeader('部署策略 - 滾動更新');
  for (let i = 1; i <= instances; i++) {
    console.log(`📦 更新實例 ${i}/${instances} 到 v${version}`);
    await delay(300);
  }
  console.log('✅ 滾動更新完成');
  return { strategy: 'rolling', version, instances };
}

// 主函數
async function demo() {
  console.log('╔══════════════════════════════════╗');
  console.log('║   DevOps 自動化流程模擬          ║');
  console.log('╚══════════════════════════════════╝');

  printHeader('Docker 構建流程');
  const imageResult = await simulateDockerBuild('myapp');
  console.log(`   映像: ${imageResult.image}:${imageResult.tag}`);
  console.log(`   大小: ${imageResult.size}`);

  const pipelineResult = await runPipeline('2.3.1');
  if (!pipelineResult.success) {
    console.error('管線執行失敗');
    process.exit(1);
  }
  console.log(`\n📊 管線摘要:`);
  console.log(`   階段數: ${pipelineResult.results.length}`);
  console.log(`   狀態: ✅ 全部通過`);

  await blueGreenDeploy(2);
  await rollingUpdate(2, 4);

  printHeader('完成');
  console.log('所有 DevOps 流程模擬成功 ✅');
}

// 偵測是否直接執行
if (require.main === module) {
  demo().catch(err => {
    console.error('執行失敗:', err.message);
    process.exit(1);
  });
}

module.exports = { demo, simulateDockerBuild, runPipeline, blueGreenDeploy, rollingUpdate };
