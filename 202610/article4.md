# 網路驅動程式與 XDP — net_device_ops、NAPI、XDP hooks

## 1. 引言

網路驅動程式是 Linux 核心中最具挑戰性也最關鍵的驅動類型。它處在核心網路堆疊的最底層，直接與硬體互動，同時需要滿足極高的吞吐量和極低的延遲要求。Rust 的型別系統和零成本抽象特別適合這類場景——它讓開發者可以專注於網路邏輯，而不是擔心記憶體安全。

## 2. 網路驅動架構

Linux 網路驅動程式分為幾個層次：

```
使用者空間 (socket, AF_PACKET, XDP)
    │
核心網路堆疊 (TCP/IP, netfilter, TC)
    │
網路裝置層 (net_device, net_device_ops)
    │
硬體驅動層 (NAPI, TX/RX 佇列, DMA)
    │
實體層 (PHY, MAC, PCIe)
```

## 3. Rust 網路驅動程式範例

### 3.1 裝置結構

```rust
use kernel::net::{NetDevice, NetDeviceOps, NetTxReturn, SkBuff};
use kernel::net::napi::{Napi, NapiCallback};
use kernel::sync::{Mutex, SpinLock};
use kernel::pci::PciDevice;

struct MyNetDrv {
    dev: NetDevice,
    pci: PciDevice,
    rx_ring: SpinLock<RxRing>,
    tx_ring: SpinLock<TxRing>,
    stats: Mutex<NetStats>,
    napi: Napi,
}

struct NetStats {
    rx_packets: u64,
    tx_packets: u64,
    rx_bytes: u64,
    tx_bytes: u64,
    rx_dropped: u64,
}
```

### 3.2 net_device_ops

```rust
impl NetDeviceOps for MyNetDrv {
    fn open(net_dev: &NetDevice) -> Result<()> {
        let this = net_dev.private_data::<MyNetDrv>();
        pr_info!("net: opening device\n");

        // 分配 TX/RX 緩衝區
        this.rx_ring.lock().alloc(256)?;
        this.tx_ring.lock().alloc(256)?;

        // 啟用 NAPI
        this.napi.enable();

        // 啟用硬體中斷
        this.enable_hw_interrupts();

        // 啟動網路佇列
        net_dev.start_queue();
        Ok(())
    }

    fn stop(net_dev: &NetDevice) -> Result<()> {
        let this = net_dev.private_data::<MyNetDrv>();
        pr_info!("net: stopping device\n");

        // 停用中斷
        this.disable_hw_interrupts();

        // 停用 NAPI
        this.napi.disable();

        // 停止 TX 佇列
        net_dev.stop_queue();
        Ok(())
    }

    fn start_xmit(skb: SkBuff, net_dev: &NetDevice) -> NetTxReturn {
        let this = net_dev.private_data::<MyNetDrv>();
        let len = skb.len();
        let data = skb.data();

        let mut tx = this.tx_ring.lock();

        // 檢查 TX 環是否已滿
        if tx.is_full() {
            net_dev.stop_queue();
            return NetTxReturn::Busy;
        }

        // 將封包資料複製到 DMA 緩衝區
        match tx.transmit(data) {
            Ok(dma_addr) => {
                // 通知硬體開始傳送
                this.write_reg(TX_DESC_ADDR, dma_addr as u32);
                this.write_reg(TX_DESC_LEN, len as u32);
                this.write_reg(TX_START, 0x1);

                let mut stats = this.stats.lock();
                stats.tx_packets += 1;
                stats.tx_bytes += len as u64;

                NetTxReturn::Ok
            }
            Err(_) => NetTxReturn::Busy,
        }
    }

    fn get_stats(net_dev: &NetDevice) -> Option<NetStats> {
        let this = net_dev.private_data::<MyNetDrv>();
        Some(*this.stats.lock())
    }
}
```

### 3.3 NAPI 輪詢接收

NAPI 的核心是在高負載時使用輪詢（polling）代替中斷來減少 CPU 開銷：

```rust
impl NapiCallback for MyNetDrv {
    fn poll(napi: &Napi, budget: u32) -> u32 {
        let net_dev = napi.device();
        let this = net_dev.private_data::<MyNetDrv>();
        let mut work_done = 0u32;

        // 從 RX 環取出封包，直到達到預算或環為空
        while work_done < budget {
            let mut rx = this.rx_ring.lock();

            match rx.receive() {
                Some(rx_pkt) => {
                    // 建立 SKBuff 並送入協議層
                    let skb = match SkBuff::new(
                        rx_pkt.data(),
                        rx_pkt.len(),
                    ) {
                        Ok(skb) => skb,
                        Err(_) => {
                            // 無法分配 skb，丟棄封包
                            this.stats.lock().rx_dropped += 1;
                            work_done += 1;
                            continue;
                        }
                    };

                    // 硬體校驗和已驗證
                    skb.set_checksum_valid();

                    // 透過 NAPI 提交給核心網路堆疊
                    napi.gro_receive(skb);

                    let mut stats = this.stats.lock();
                    stats.rx_packets += 1;
                    stats.rx_bytes += rx_pkt.len() as u64;

                    work_done += 1;
                }
                None => break,
            }
        }

        // 如果未達到預算，表示封包已處理完，重新啟用中斷
        if work_done < budget {
            napi.complete();
            this.enable_hw_interrupts();
        }

        work_done
    }
}
```

### 3.4 XDP 掛鉤

XDP（eXpress Data Path）在驅動層面提供了一個高效能的封包處理掛鉤：

```rust
use kernel::net::xdp::{XdpProgram, XdpAction, XdpBuff};

impl MyNetDrv {
    fn xdp_handler(&self, xdp_buff: &XdpBuff) -> XdpAction {
        let data = xdp_buff.data();
        if data.len() < 14 {
            return XdpAction::Drop;
        }

        // 解析乙太網路標頭
        let eth_type = u16::from_be_bytes([data[12], data[13]]);

        match eth_type {
            0x0800 => {  // IPv4
                // 簡單的防火牆：阻擋特定來源 IP
                if data.len() >= 34 {
                    let src_ip = &data[26..30];
                    if src_ip == [192u8, 168, 1, 100] {
                        return XdpAction::Drop;
                    }
                }
                XdpAction::Pass
            }
            0x0806 => {  // ARP
                // ARP 封包重導向到 userspace
                XdpAction::Redirect
            }
            0x86DD => {  // IPv6 - 直接傳遞
                XdpAction::Pass
            }
            _ => XdpAction::Pass,
        }
    }
}
```

## 4. 硬體卸載功能

現代網路卡支援多種硬體卸載（Offload）功能，Rust 提供型別安全的配置介面：

```rust
impl MyNetDrv {
    fn configure_offloads(&self) -> Result<()> {
        let mut features = self.dev.features();

        // 基礎卸載
        features.enable(NetFeature::HwVlanCtag)?;  // VLAN 標籤卸載
        features.enable(NetFeature::HwChecksum)?;  // 校驗和卸載

        // 進階卸載
        features.enable(NetFeature::Tso)?;         // TCP Segmentation Offload
        features.enable(NetFeature::Gro)?;         // Generic Receive Offload
        features.enable(NetFeature::Lro)?;         // Large Receive Offload

        // 設定 RSS (Receive Side Scaling)
        let rss_key = [
            0x1d, 0xea, 0x82, 0x6f, 0xdb, 0x9c, 0x93, 0x0b,
            0x79, 0x63, 0x5e, 0x6f, 0xbc, 0x3b, 0x4e, 0x24,
            0x6f, 0x1d, 0xea, 0x82, 0x6f, 0xdb, 0x9c, 0x93,
            0x0b, 0x79, 0x63, 0x5e, 0x6f, 0xbc, 0x3b, 0x4e,
            0x24, 0x6f, 0x1d, 0xea, 0x82, 0x6f, 0xdb, 0x9c,
        ];
        self.dev.rss_set_key(&rss_key)?;

        let indirection = (0u8..16).collect::<Vec<_>>();
        self.dev.rss_set_indirection_table(&indirection)?;

        Ok(())
    }
}
```

## 5. 多佇列支援

現代 10G/25G/100G 網路卡支援多個 TX/RX 佇列，充分利用多核心 CPU：

```rust
impl MyNetDrv {
    fn setup_queues(&self, num_queues: u32) -> Result<()> {
        for i in 0..num_queues {
            let rx_q = RxQueue::new(i, 512)?;    // 512 個描述符
            let tx_q = TxQueue::new(i, 512)?;

            // 分配 RX 緩衝區
            for _ in 0..rx_q.capacity() {
                rx_q.add_buffer(Buffer::new(2048)?)?;
            }

            // 綁定到特定 CPU
            rx_q.set_cpu_affinity(i as usize)?;
            tx_q.set_cpu_affinity(i as usize)?;
        }
        self.dev.set_real_num_queues(num_queues)?;
        Ok(())
    }
}

fn irq_handler(dev: &MyNetDrv, queue: u32) -> irq::Return {
    // 觸發對應佇列的 NAPI 輪詢
    dev.napi_for_queue(queue).schedule();
    irq::Return::Handled
}
```

## 6. 結語

網路驅動程式是 Rust 在 Linux 核心中最有說服力的應用場景之一。高效能網路需要處理複雜的非同步事件、管理大量 DMA 緩衝區、並在極短的時間內做出封包處理決策——而這些正是 Rust 所有權模型和型別系統最能發揮優勢的地方。隨著 XDP 和 eBPF 技術的成熟，Rust 網路驅動程式的發展空間將更加廣闊。

---

## 延伸閱讀

- [Linux NAPI 文件](https://www.google.com/search?q=Linux+NAPI+documentation)
- [XDP 入門指南](https://www.google.com/search?q=XDP+tutorial+Linux)
- [Linux 網路設備驅動程式](https://www.google.com/search?q=Linux+network+device+driver)
- [RSS 與多佇列](https://www.google.com/search?q=RSS+Receive+Side+Scaling+Linux)
