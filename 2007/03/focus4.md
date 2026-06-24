# Java 與 JVM 平台的演進

## 前言

2007 年的 Java 继续保持企業級市場的主導地位，同時 JVM 平台開始支援更多語言。

## Java SE 6 的改進

```java
// Java SE 6 新特性
public class Java6Features {
    // 1. Scripting API
    public String executeScript(String script) {
        ScriptEngineManager manager = new ScriptEngineManager();
        ScriptEngine engine = manager.getEngineByName("JavaScript");
        return engine.eval(script).toString();
    }
}
```

## JVM 語言的繁榮

```
┌────────────────────────────────────────────────────────┐
│              JVM 上的語言                              │
├────────────────────────────────────────────────────────┤
│                                                        │
│  JRuby：Ruby on JVM                                   │
│  Groovy：動態腳本語言                                  │
│  Scala：函數式+物件導向                                │
│  Clojure：Lisp 方言                                   │
│  Kotlin：後來加入（2011）                             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## 結論

Java 在 2007 年仍是企業應用的首選，JVM 平台的多語言支援預示了未來的發展方向。

---

*本篇文章為「AI 程式人雜誌 2007 年 3 月號」本期焦點系列文章。*