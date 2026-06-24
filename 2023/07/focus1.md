# 密碼學歷史與古典密碼

## 密碼學的曙光

密碼學的歷史與人類書寫的歷史幾乎一樣悠久。早在四千年前，古埃及人就使用非標準的象形文字來傳遞訊息——這可能是最早的密碼學應用。古希臘人使用斯巴達密碼棒（Scytale），將羊皮紙纏繞在木棒上書寫，解開後文字變得無法辨識，只有使用相同直徑的木棒才能正確讀取。

## 凱薩密碼

凱薩密碼（Caesar Cipher）由羅馬帝國的凱薩大帝（Julius Caesar）在其軍事通信中使用。他將每個字母向後移動三個位置：

```
明文：A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
密文：D E F G H I J K L M N O P Q R S T U V W X Y Z A B C
```

例如，HELLO 加密後變成 KHOOR。凱薩密碼本質上是移位密碼的一個特例，移位量固定為 3。由於只有 25 種可能的金鑰（不考慮零位移），暴力破解極為容易。在現代的計算機面前，凱薩密碼可以在毫秒內被破解。

## 頻率分析

9 世紀的阿拉伯學者 Al-Kindi 在其著作《關於解密密碼訊息的手稿》中，首次系統性地描述了頻率分析技術。這種技術利用自然語言中字母出現頻率的不均勻性來破解替代密碼。

在英文中，最常見的字母依次是 E、T、A、O、I、N、S、H、R。通過統計密文中字母的出現頻率，可以推測出明文字母與密文字母的對應關係。頻率分析使得單表替代密碼——包括凱薩密碼——不再安全。

## 維吉尼亞密碼

16 世紀，義大利數學家 Giovan Battista Bellaso 提出了多表替代密碼的概念。後來，法國外交官 Blaise de Vigenère 完善了這一技術，被稱為維吉尼亞密碼（Vigenère Cipher）。

維吉尼亞密碼使用一個關鍵字來決定每個字母的偏移量：

```
關鍵字：KEYKEYKEYKEY
明文：  HELLOWORLD
密文：  RIJVSUDCPK
```

維吉尼亞密碼的關鍵在於，同一個明文字母可以加密成不同的密文字母，從而抵抗簡單的頻率分析。在 19 世紀以前，維吉尼亞密碼被認為是不可破解的。

## Kasiski 測試與破解

1863 年，普魯士軍官 Friedrich Kasiski 發表了破解維吉尼亞密碼的方法——Kasiski 測試。這個方法的核心觀察是：如果同一個字詞在明文中重複出現，且兩次出現的位置距離剛好是金鑰長度的整數倍，則它們的加密結果會相同。

Kasiski 測試的步驟：
1. 尋找密文中重複出現的字母序列
2. 計算重複序列之間的距離
3. 找出這些距離的最大公因數，即金鑰長度
4. 將密文按金鑰長度分組，每組使用頻率分析破解

## Enigma 機

第二次世界大戰中，德國使用了 Enigma 密碼機進行軍事通信。Enigma 是一種轉子機械加密裝置，使用多個旋轉轉子來實現複雜的多表替代。

Enigma 的核心組件：
- 鍵盤：輸入明文
- 轉子：3-5 個可更換的旋轉圓盤，每個轉子實現一個字母映射
- 反射器：將信號反射回轉子路徑
- 燈板：顯示加密結果

Enigma 的密鑰空間極為龐大，使得暴力破解在當時不切實際。然而，盟軍的密碼學家——特別是 Alan Turing 和他的團隊——在 Bletchley Park 設計了 Bombe 機器，利用 Enigma 的設計缺陷（如字母不可能加密成自身）進行破解。

Turing 的貢獻不僅幫助盟軍贏得了戰爭，更為現代計算機科學奠定了基礎。他在戰後設計的 Automatic Computing Engine（ACE）影響了後來計算機的發展方向。

## 從古典到現代

古典密碼學的教訓深刻地影響了現代密碼設計：

1. **金鑰空間**：足夠大的金鑰空間是安全性的基本要求
2. **混淆與擴散**：Shannon 提出的兩個原則，混淆使密文與金鑰的關係複雜化，擴散將明文結構擴散到密文中
3. **Kerckhoffs 原則**：密碼系統的安全性應僅依賴於金鑰的保密，而不是演算法的隱藏

這些原則至今仍是指導現代密碼設計的基石。

## 延伸閱讀

- [Caesar Cipher 歷史](https://www.google.com/search?q=Caesar+cipher+history+Julius+Caesar)
- [Vigenère Cipher](https://www.google.com/search?q=Vigen%C3%A8re+cipher+explanation)
- [Enigma Machine](https://www.google.com/search?q=Enigma+machine+how+it+worked)
- [Alan Turing Bletchley Park](https://www.google.com/search?q=Alan+Turing+Bletchley+Park+Enigma)

---

*本篇文章為「AI 程式人雜誌 2023 年 7 月號」密碼學基礎系列之一。*
