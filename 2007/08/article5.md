# Apache Geronimo：Java EE 伺服器

Apache Geronimo 是 Apache 軟體基金會的 Java EE 應用伺服器，為企業級 Java 應用提供完整的執行環境。

## Geronimo 的特點

### 完整的 Java EE 支援

```java
// 部署描述符
<application xmlns="http://geronimo.apache.org/xml/ns/j2ee/application">
    <environment>
        <moduleId>
            <groupId>com.example</groupId>
            <artifactId>myapp</artifactId>
            <version>1.0</version>
        </moduleId>
    </environment>
</application>
```

### 整合元件

```bash
# Geronimo 內建
- Tomcat 或 Jetty servlet 容器
- OpenEJB (EJB 容器)
- OpenJPA (JPA 實現)
- ActiveMQ (訊息队列)
- Geronimo Management (JMX)
```

## 結語

Geronimo 為企業級 Java 應用提供了開放原始碼的選擇。

---

*延伸閱讀：[Geronimo 官方網站](https://developers.google.com/search/?q=apache+geronimo)*