# 主題五：網路驅動程式

## NAPI、net_device_ops 與 XDP

### 網路子系統的複雜性

網路驅動程式是核心中最具挑戰性的驅動程式類型之一。它需要處理中斷驅動的封包接收、多佇列負載平衡、校驗和卸載、TSO（TCP Segmentation Offload）等硬體功能，還需要與上層網路堆疊流暢互動。

### net_device_ops 的 Rust 抽象

Rust for Linux 的 `NetDeviceOps` trait 封裝了核心的 `net_device_ops`：

```rust
use kernel::net::{NetDevice, NetDeviceOps};

struct MyNetDev {
    net_dev: NetDevice,
    stats: Mutex<NetStats>,
}

impl NetDeviceOps for MyNetDev {
    fn open(dev: &NetDevice) -> Result<()> {
        pr_info!("net device opened\n");
        // 啟動 TX/RX 佇列
        dev.start_queue();
        Ok(())
    }

    fn stop(dev: &NetDevice) -> Result<()> {
        pr_info!("net device stopped\n");
        dev.stop_queue();
        Ok(())
    }

    fn start_xmit(skb: SkBuff, dev: &NetDevice) -> NetTxReturn {
        // 將封包傳送給硬體
        let this = dev.private_data::<MyNetDev>();
        let len = skb.len();
        // ... DMA 傳送邏輯
        this.stats.lock().unwrap().tx_packets += 1;
        NetTxReturn::Ok
    }
}
```

### NAPI（New API）輪詢機制

NAPI 是現代 Linux 網路驅動的核心機制，結合中斷與輪詢來達到高效能：

```rust
use kernel::net::napi::{Napi, NapiCallback};

impl NapiCallback for MyNetDev {
    fn poll(napi: &Napi, budget: u32) -> u32 {
        let mut work_done = 0u32;

        // 從硬體接收佇列中取出封包
        while work_done < budget {
            match rx_ring.next_packet() {
                Some(pkt) => {
                    // 將封包送入核心網路堆疊
                    let skb = SkBuff::new(pkt.data(), pkt.len());
                    napi.gro_receive(skb);
                    work_done += 1;
                }
                None => break,
            }
        }

        if work_done < budget {
            napi.complete();
            enable_interrupts();
        }

        work_done
    }
}

fn register_napi(dev: &MyNetDev) -> Result<()> {
    let napi = Napi::new(
        &dev.net_dev,
        Napi::default()
            .weight(64)
            .callback(dev),
    )?;
    napi.enable();
    Ok(())
}
```

### XDP（eXpress Data Path）

XDP 是 Linux 核心中革命性的高效能封包處理框架，在驅動程式層級掛鉤，在封包進入核心網路堆疊前進行處理：

```rust
use kernel::net::xdp::{XdpProgram, XdpAction};

impl XdpProgram for MyNetDev {
    fn run(skb: &SkBuff) -> XdpAction {
        let data = skb.data();

        // 簡單的防火牆規則
        if data.len() >= 14 {
            let eth_type = u16::from_be_bytes([data[12], data[13]]);
            match eth_type {
                0x0800 => {
                    // IPv4 封包
                    let proto = data[23];
                    if proto == 6 {
                        // TCP - 傳遞給上層
                        XdpAction::Pass
                    } else if proto == 17 {
                        // UDP - 丟棄
                        XdpAction::Drop
                    } else {
                        XdpAction::Pass
                    }
                }
                0x86DD => XdpAction::Pass,  // IPv6
                _ => XdpAction::Pass,
            }
        } else {
            XdpAction::Drop
        }
    }
}
```

### 硬體卸載功能

現代網路卡支援多種卸載功能，Rust 的抽象讓配置更加安全：

```rust
impl MyNetDev {
    fn configure_offloads(&self) -> Result<()> {
        let features = self.net_dev.features();

        // 啟用硬體校驗和卸載
        features.enable(NetFeature::HwChecksum)?;

        // 啟用 TSO 和 GRO
        features.enable(NetFeature::Tso | NetFeature::Gro)?;

        // 設定 RSS（Receive Side Scaling）
        let rss = RssConfig::new()
            .hash_key(&[0x6d, 0x65, 0x6f, 0x77])
            .indirection_table(&[0, 1, 0, 1, 2, 3, 2, 3])?;

        self.net_dev.set_rss(rss)?;
        Ok(())
    }
}
```

### 多佇列支援

現代網路驅動需要支援多個 TX/RX 佇列以充分發揮多核心 CPU 的效能：

```rust
fn setup_queues(dev: &MyNetDev, num_queues: u32) -> Result<()> {
    for i in 0..num_queues {
        let rx_queue = RxQueue::new(dev, i, 256)?;
        let tx_queue = TxQueue::new(dev, i, 256)?;

        // 每個佇列分配到不同的 CPU
        rx_queue.set_affinity(cpumask_for_cpu(i as usize))?;
    }
    Ok(())
}
```

---

**下一步**: [GPU 與 DRM 驅動程式](focus6.md)

## 延伸閱讀

- [Linux NAPI 文件](https://www.google.com/search?q=Linux+NAPI+documentation)
- [XDP 教學](https://www.google.com/search?q=XDP+eXpress+Data+Path+tutorial)
- [Rust XDP 範例](https://www.google.com/search?q=Rust+XDP+BPF+example)
