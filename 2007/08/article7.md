# 機器人作業系統：Player/Stage 計畫

Player/Stage 是機器人研究的開源模擬器和軟體平台，廣泛用於學術研究和教育。

## Player/Stage 架構

```cpp
// Player 客戶端範例
#include <libplayerc/playerc.h>

int main() {
    playerc_client_t* client = playerc_client_create(NULL, 6665);
    playerc_client_connect(client);

    playerc_position2d_t* position = playerc_position2d_create(client, 0);
    playerc_position2d_subscribe(position, PLAYERC_OPEN_MODE);

    // 控制機器人移動
    playerc_position2d_set_cmd_pose(position, 1.0, 0.0, 0.0, 1);

    playerc_client_disconnect(client);
    return 0;
}
```

## Stage 模擬器

```bash
# Stage 設定檔案 (.world)
world (
    interval 100
    resolution 0.02

    robot (
        pose [0 0 0]
        rtk_pose_max_rnage 8.0
        rtk_pose_noise 0.02
    )

    range laser (
        pose [0.2 0 0]
        fov 180.0
        range [0 8.0]
        samples 180
    )
)
```

## 結語

Player/Stage 為機器人研究提供了免費且功能強大的模擬環境。

---

*延伸閱讀：[Player/Stage 官方網站](https://developers.google.com/search/?q=player+stage+robotics)*