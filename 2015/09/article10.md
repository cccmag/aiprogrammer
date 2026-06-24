# 軟體定義網路 (SDN)

## 前言

軟體定義網路（Software Defined Networking，SDN）代表了網路架構的重大轉變。

---

## 傳統網路 vs SDN

### 傳統網路

```
路由器/交換機 ──> 控制平面（嵌入在設備）
                      │
              分散式管理
                      │
              資料平面（轉發）
```

### SDN

```
         ┌──────────────┐
         │ 控制器       │  ← 集中式控制平面
         │ (北向 API)   │
         └──────┬───────┘
                │
    ┌───────────┼───────────┐
    │           │           │
┌───┴───┐ ┌───┴───┐ ┌───┴───┐  ← 資料平面（純轉發）
│ Switch │ │ Switch │ │ Switch │
└───────┘ └───────┘ └───────┘
         (南向 API，如 OpenFlow)
```

---

## SDN 優點

### 1. 集中管理

- 單一控制點
- 更容易配置
- 統一策略

### 2. 彈性

- 動態調整網路
- 快速部署
- 易于擴展

### 3. 程式化

- 可編程網路
- 自動化
- 與雲端整合

### 4. 成本效益

- 使用商用硬體
- 減少專用設備
- 簡化管理

---

## OpenFlow

最流行的 SDN 南向介面。

### 流程

```python
# Ryu 控制器範例
from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet

class SimpleSwitch(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, MAIN_DISPATCHER)
    def switch_features_handler(self, ev):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        self.add_flow(datapath, 0, match, actions)

    def add_flow(self, datapath, priority, match, actions):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                match=match, instructions=inst)
        datapath.send_msg(mod)
```

---

## SDN 控制器

### 開源控制器

| 控制器 | 語言 | 特點 |
|--------|------|------|
| OpenDaylight | Java | 企業級、功能豐富 |
| Ryu | Python | 輕量、容易學習 |
| ONOS | Java | 電信級、高可用 |
| Floodlight | Java | 簡單易用 |

### Ryu 範例

```bash
# 安裝
pip install ryu

# 執行
ryu-manager simple_switch.py
```

---

## 網路功能虛擬化 (NFV)

### 傳統 vs NFV

```
傳統：                      NFV：
硬體防火牆 ──> VM 上的防火牆
硬體負載平衡 ──> VM 上的負載平衡
硬體路由器 ──> VM 上的路由器
```

### 優勢

- 彈性調整資源
- 快速部署
- 降低成本

---

## 應用場景

### 資料中心網路

```python
# 自動化網路配置
# 快速擴展
# 流量工程
```

### 雲端網路

```python
# 網路即服務
# 多租戶隔離
# 動態配置
```

### 校園網路

```python
# 訪客網路隔離
# 政策執行
# 網路監控
```

---

## 安全性考量

### SDN 安全優勢

- 集中式監控
- 快速回應威脅
- 一致性策略

### SDN 安全風險

- 控制器單點故障
- 控制通道攻擊
- 應用程式漏洞

### 防護措施

```bash
# 控制器認證
# 控制通道加密
# 最小權限原則
# 持續監控
```

[搜尋 SDN security challenges](https://www.google.com/search?q=SDN+security+challenges+2015)

---

## 未來趨勢

### 2015 年趨勢

- **OpenStack Neutron**：整合 SDN 和雲端
- **WhiteBox 交換機**：裸機交換機
- **CORD**：資料中心重構

### 發展方向

- 網路功能自動化（Network Function Orchestration）
- 意圖驅動網路（Intent-Based Networking）
- 整合 AI/ML 的網路優化

---

## 小結

SDN 代表了網路的未來，了解其原理和應用對網路工程師越來越重要。

---

*作者：AI 程式人團隊*

*延伸閱讀：*
- [Open Networking Foundation](https://www.google.com/search?q=Open+Networking+Foundation)
- [OpenFlow 規格](https://www.google.com/search?q=OpenFlow+specification)