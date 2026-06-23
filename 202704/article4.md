# Rust 中的 ONNX 模型載入與推論

## 前言

ONNX（Open Neural Network Exchange）是深度學習模型的開放標準格式。它允許模型在不同框架之間遷移：PyTorch → ONNX → TensorRT / OpenVINO / CoreML。在 Rust 中載入 ONNX 模型並執行推論，是邊緣部署和後端服務的關鍵能力。

本文探討如何在 Rust 中解析 ONNX 協定緩衝區、構建計算圖，並執行模型推論。

## ONNX 格式解析

ONNX 使用 Protocol Buffers（protobuf）儲存模型。在 Rust 中，我們使用 `prost` 或 `protobuf` crate 來解析：

### 定義 Protobuf 訊息

```protobuf
// ONNX 核心類型（簡化版）
message TensorProto {
    repeated int64 dims = 1;
    int32 data_type = 2;
    // 資料儲存在多種格式中選一種
    repeated float float_data = 3;
    bytes raw_data = 4;
    string name = 5;
}

message NodeProto {
    repeated string input = 1;
    repeated string output = 2;
    string op_type = 3;    // "MatMul", "Relu", "Conv", etc.
    string name = 4;
    repeated AttributeProto attribute = 5;
}

message GraphProto {
    repeated TensorProto initializer = 1;  // 常數權重
    repeated NodeProto node = 2;            // 計算節點
    repeated ValueInfoProto input = 3;      // 模型輸入
    repeated ValueInfoProto output = 4;     // 模型輸出
    string name = 5;
}

message ModelProto {
    int64 ir_version = 1;
    OperatorSetIdProto opset_import = 2;
    GraphProto graph = 3;
}
```

### Rust 載入 ONNX

```rust
use prost::Message;
use std::fs;

// 使用 prost 編譯 ONNX protobuf 定義
include!(concat!(env!("OUT_DIR"), "/onnx.rs"));

fn load_onnx(path: &str) -> Result<ModelProto, Box<dyn std::error::Error>> {
    let bytes = fs::read(path)?;
    let model = ModelProto::decode(&bytes[..])?;
    Ok(model)
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let model = load_onnx("model.onnx")?;
    let graph = model.graph.unwrap();

    println!("Nodes: {}", graph.node.len());
    println!("Initializers: {}", graph.initializer.len());
    for node in &graph.node {
        println!("  {} -> {}", node.op_type, node.name);
    }
    Ok(())
}
```

## 構建計算圖

解析 ONNX 後，我們需要將其轉換為可執行的計算圖：

```rust
enum OpType {
    MatMul,
    Add,
    Relu,
    Conv2d {
        strides: Vec<i64>,
        pads: Vec<i64>,
        dilations: Vec<i64>,
        group: i64,
    },
    Reshape,
    Softmax,
    // ... 更多算子
}

struct ComputeNode {
    op: OpType,
    inputs: Vec<String>,
    output: String,
}

struct ComputeGraph {
    nodes: Vec<ComputeNode>,
    tensors: HashMap<String, TensorData>,  // 權重與中間結果
    input_names: Vec<String>,
    output_names: Vec<String>,
}

impl ComputeGraph {
    fn from_onnx(model: &ModelProto) -> Self {
        let graph = model.graph.as_ref().unwrap();

        // 收集常數權重
        let mut tensors = HashMap::new();
        for init in &graph.initializer {
            let name = init.name.clone();
            let data = TensorData::from_proto(init);
            tensors.insert(name, data);
        }

        // 轉換節點
        let mut nodes = vec![];
        for node in &graph.node {
            let op = parse_op_type(node);
            let inputs = node.input.iter().map(|s| s.clone()).collect();
            let output = node.output[0].clone();
            nodes.push(ComputeNode { op, inputs, output });
        }

        let input_names = graph.input.iter()
            .map(|v| v.name.clone()).collect();
        let output_names = graph.output.iter()
            .map(|v| v.name.clone()).collect();

        ComputeGraph { nodes, tensors, input_names, output_names }
    }
}
```

## 算子實作

每個 ONNX 算子都需要對應的 Rust 實作。以 MatMul 為例：

```rust
struct TensorData {
    data: Vec<f32>,
    shape: Vec<i64>,
}

// 簡化的 MatMul（完整版需包含 broadcast 等）
fn matmul(a: &TensorData, b: &TensorData) -> TensorData {
    assert_eq!(a.shape.len(), 2);
    assert_eq!(b.shape.len(), 2);
    let (m, k) = (a.shape[0] as usize, a.shape[1] as usize);
    let (k2, n) = (b.shape[0] as usize, b.shape[1] as usize);
    assert_eq!(k, k2);

    let mut result = vec![0.0f32; m * n];
    for i in 0..m {
        for j in 0..n {
            let mut sum = 0.0;
            for kk in 0..k {
                sum += a.data[i * k + kk] * b.data[kk * n + j];
            }
            result[i * n + j] = sum;
        }
    }
    TensorData { data: result, shape: vec![m as i64, n as i64] }
}

fn relu(t: &TensorData) -> TensorData {
    TensorData {
        data: t.data.iter().map(|&x| x.max(0.0)).collect(),
        shape: t.shape.clone(),
    }
}

fn softmax(t: &TensorData) -> TensorData {
    let n = t.data.len();
    let max_val = t.data.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
    let exps: Vec<f32> = t.data.iter().map(|x| (x - max_val).exp()).collect();
    let sum: f32 = exps.iter().sum();
    TensorData {
        data: exps.iter().map(|x| x / sum).collect(),
        shape: t.shape.clone(),
    }
}
```

## 推論引擎

### 拓撲排序執行

ONNX 計算圖是有向無環圖（DAG）。我們需要按拓撲順序執行節點：

```rust
impl ComputeGraph {
    fn infer(&mut self, inputs: HashMap<String, TensorData>)
        -> HashMap<String, TensorData>
    {
        // 將輸入放入 tensors
        for (name, tensor) in inputs {
            self.tensors.insert(name, tensor);
        }

        // 按順序執行節點
        for node in &self.nodes {
            let input_tensors: Vec<&TensorData> = node.inputs
                .iter()
                .map(|name| self.tensors.get(name).unwrap())
                .collect();

            let output = match &node.op {
                OpType::MatMul => matmul(input_tensors[0], input_tensors[1]),
                OpType::Add => add(input_tensors[0], input_tensors[1]),
                OpType::Relu => relu(input_tensors[0]),
                OpType::Softmax => softmax(input_tensors[0]),
                // ... 其他算子
            };

            self.tensors.insert(node.output.clone(), output);
        }

        // 收集輸出
        self.output_names.iter()
            .map(|name| (name.clone(), self.tensors.remove(name).unwrap()))
            .collect()
    }
}
```

## 使用 tract 運行 ONNX

自行實作完整 ONNX runtime 的工作量巨大。在生產環境中，建議使用 `tract` —— 這是最成熟的 Rust ONNX 推論引擎：

```rust
use tract_onnx::prelude::*;

fn infer_with_tract() -> TractResult<()> {
    // 載入 ONNX 模型
    let model = onnx()
        .model_for_path("model.onnx")?
        .with_input_fact(0, InferenceFact::dt_shape(f32::datum_type(), tvec!(1, 3, 224, 224)))?
        .into_optimized()?  // 常數摺疊與圖優化
        .into_runnable()?;  // 編譯為可執行狀態

    // 準備輸入
    let input = Tensor::from_shape(&[1, 3, 224, 224])?
        .into_tensor();

    // 執行推論
    let result = model.run(tvec!(input))?;
    let output = result[0].to_array_view::<f32>()?;

    println!("Output shape: {:?}", output.shape());
    Ok(())
}
```

tract 內建了以下優化：

| 優化 | 說明 | 效果 |
|------|------|------|
| 常數摺疊（Constant Folding） | 編譯期計算常數子圖 | 減少執行期計算 |
| 形狀推斷（Shape Inference） | 靜態推斷所有中間張量的形狀 | 記憶體預先分配 |
| 算子融合（Operator Fusion） | 將相鄰算子合併為一個 kernel | 減少記憶體往返 |
| 記憶體規劃（Memory Planning） | 重複使用中間緩衝區 | 減少峰值記憶體 |

## 模型優化

### 常數摺疊實作

```rust
fn constant_folding(graph: &mut ComputeGraph) {
    let mut changed = true;
    while changed {
        changed = false;
        let mut to_remove = vec![];

        for (i, node) in graph.nodes.iter().enumerate() {
            let all_const = node.inputs.iter()
                .all(|name| graph.initializers.contains_key(name));

            if all_const {
                // 編譯期執行此節點
                let output = execute_node(node, &graph.initializers);
                graph.initializers.insert(node.output.clone(), output);
                to_remove.push(i);
                changed = true;
            }
        }

        // 移除已摺疊的節點
        for &i in to_remove.iter().rev() {
            graph.nodes.remove(i);
        }
    }
}
```

### 形狀推斷

```rust
fn infer_shapes(graph: &mut ComputeGraph) {
    for node in &graph.nodes {
        let input_shapes: Vec<&[i64]> = node.inputs.iter()
            .map(|name| graph.tensors.get(name).unwrap().shape.as_slice())
            .collect();

        let output_shape = match &node.op {
            OpType::MatMul => {
                let (m, _) = (input_shapes[0][0], input_shapes[0][1]);
                let (_, n) = (input_shapes[1][0], input_shapes[1][1]);
                vec![m, n]
            }
            OpType::Relu => input_shapes[0].to_vec(),
            // ...
        };

        // 預先分配輸出張量
        let size: usize = output_shape.iter().product::<i64>() as usize;
        graph.tensors.insert(node.output.clone(), TensorData {
            data: vec![0.0; size],
            shape: output_shape,
        });
    }
}
```

## 比較：自行實作 vs tract

| 考量 | 自行實作 | tract |
|------|---------|-------|
| 支援算子數量 | 數十個 | 150+ |
| ONNX opset 版本 | 需自行跟上 | 持續更新 |
| 效能 | 基礎 | 高度最佳化 |
| 二進位體積 | 數百 KB | 數 MB |
| 控制權 | 完全控制 | 抽象層級較高 |

## 總結

在 Rust 中載入 ONNX 模型的標準路徑是使用 `tract` 函式庫，它覆蓋了 150+ 算子、內建圖優化、且支援跨平台編譯。對於需要深度客製化的場景，可以自行實作 ONNX 解析與簡化推論引擎，但要追上 tract 的算子覆蓋率和最佳化程度需要大量投入。

---

**參考資料**

- https://www.google.com/search?q=ONNX+protobuf+Rust+prost
- https://www.google.com/search?q=tract+ONNX+Rust+inference
- https://www.google.com/search?q=constant+folding+ONNX+graph+optimization
- https://www.google.com/search?q=Rust+ONNX+runtime+implementation
- https://www.google.com/search?q=ONNX+opset+operator+list
